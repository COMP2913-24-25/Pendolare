import { useState } from "react";
import { View, TouchableOpacity, Alert } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import UpcomingRideDetailsModal from "./Modals/UpcomingRideDetailsModal";
import { approveBooking, BookingDetails } from "@/services/bookingService";
import { toHumanReadable } from "@/utils/cronTools";
import OneClickRebook from "./OneClickRebook";

interface DriverRideCardProps {
  booking: BookingDetails; // Only accept BookingDetails
  journeyView?: boolean;
  approveBookingCallback?: () => void;
  isCommuter?: boolean;
}

/*
    DriverRideCard
    Card for a ride from the perspective of the driver
*/
const DriverRideCard = ({ booking, journeyView = false, approveBookingCallback, isCommuter = false }: DriverRideCardProps) => {
  const { isDarkMode } = useTheme();
  const [showDetails, setShowDetails] = useState(false);
  
  // Extract needed data from the booking
  const { Journey: journey, Booking: rideDetails, BookingStatus: status } = booking;
  
  // If no data is available, show a placeholder
  if (!journey || !rideDetails || !status) {
    return (
      <TouchableOpacity
        className={`p-4 rounded-lg shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"} mb-4`}
        disabled={true}
      >
        <Text className="text-red-500">Error: No ride data available</Text>
      </TouchableOpacity>
    );
  }
  
  // Ensure RideTime is a Date object
  let rideTime: Date;
  try {
    if (typeof rideDetails.RideTime === 'string') {
      rideTime = new Date(rideDetails.RideTime);
    } else if (rideDetails.RideTime instanceof Date) {
      rideTime = rideDetails.RideTime;
    } else {
      rideTime = new Date();
    }
  } catch (e) {
    rideTime = new Date();
  }
  
  // Check if this is an expired commuter journey that can be rebooked
  const isExpiredCommuter = isCommuter && 
    journey.RepeatUntil && 
    new Date(journey.RepeatUntil) < new Date() &&
    status.Status !== "Cancelled";

  const handleApproveBooking = async () => {
    try {
      if (!approveBookingCallback) return;
      
      const bookingId = rideDetails.BookingId;
      const response = await approveBooking(bookingId);
      
      if (response.success) {
        Alert.alert("Success", "Booking approved successfully");
        approveBookingCallback();
      } else {
        if (response.message?.includes("has booking amendments")) {
          Alert.alert(
            "Cannot Approve",
            "This booking has pending amendments. Please resolve them first."
          );
        } else {
          Alert.alert("Error", response.message || "Failed to approve booking");
        }
      }
    } catch (error) {
      console.error("Error approving booking:", error);
      Alert.alert("Error", "Failed to approve booking");
    }
  };

  return (
    <TouchableOpacity
      className={`p-4 rounded-lg shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"} mb-4`}
      onPress={() => setShowDetails(true)}
    >
      <View className="flex-row justify-between items-center mb-2">
        <Text className="text-lg font-JakartaBold flex-1">
          {journeyView ? "Your Journey" : status.Status === "Pending" ? "Pending Booking" : "Upcoming Ride"}
        </Text>
        <Text className="text-blue-600 font-JakartaBold">
          {typeof journey.Price === "number"
            ? `£${journey.Price.toFixed(2)}`
            : "N/A"}
        </Text>
      </View>

      {/* Add commuter journey badge */}
      <View className="flex-row flex-wrap">
        {isCommuter && (
          <View className="mb-2 mr-2 bg-blue-100 self-start rounded-full px-2 py-1">
            <Text className="text-blue-800 text-xs">Commuter Journey</Text>
          </View>
        )}
        
        {/* Add expired badge if applicable */}
        {isExpiredCommuter && (
          <View className="mb-2 bg-amber-100 self-start rounded-full px-2 py-1">
            <Text className="text-amber-800 text-xs">Expired</Text>
          </View>
        )}
      </View>

      <View className="mb-2">
        <Text className={`${isDarkMode ? "text-gray-300" : "text-gray-600"}`}>
          {rideTime.toLocaleString()}
        </Text>
      </View>

      {/* Show recurrence information if this is a commuter journey */}
      {isCommuter && journey.Recurrance && (
        <View className="mb-2 py-1 px-2 bg-gray-100 rounded-md">
          <Text className="text-sm text-gray-700">
            {toHumanReadable(journey.Recurrance)}
          </Text>
          {journey.RepeatUntil && (
            <Text className="text-xs text-gray-500">
              Until {new Date(journey.RepeatUntil).toLocaleDateString()}
            </Text>
          )}
        </View>
      )}

      <View className="mb-1">
        <Text className={`${isDarkMode ? "text-gray-300" : "text-gray-600"}`}>
          From: {journey.StartName}
        </Text>
        <Text className={`${isDarkMode ? "text-gray-300" : "text-gray-600"}`}>
          To: {journey.EndName}
        </Text>
      </View>

      {/* Show rebook button for expired commuter journeys */}
      {isExpiredCommuter && journeyView && (
        <OneClickRebook 
          journeyId={journey.JourneyId}
          originalDuration={
            journey.RepeatUntil && journey.StartDate ? 
            Math.ceil((new Date(journey.RepeatUntil).getTime() - new Date(journey.StartDate).getTime()) / (1000 * 60 * 60 * 24)) : 
            undefined
          }
          onSuccess={approveBookingCallback}
        />
      )}

      {/* Only show passenger details if this isn't a journey view */}
      {!journeyView && (
        <View className="flex-row justify-between items-center mt-2">
          <Text
            className={`${isDarkMode ? "text-gray-300" : "text-gray-600"} flex-1`}
          >
            Passenger: {rideDetails.User?.Name || "Pending"}
          </Text>
          <View
            className={`px-2 py-1 rounded-full ${
              status.Status === "Pending"
                ? "bg-yellow-500"
                : status.Status === "Confirmed"
                ? "bg-green-500"
                : status.Status === "Cancelled"
                ? "bg-red-500"
                : "bg-blue-500"
            }`}
          >
            <Text className="text-white text-xs font-JakartaMedium">
              {status.Status}
            </Text>
          </View>
        </View>
      )}

      {/* Details Modal */}
      <UpcomingRideDetailsModal
        booking={booking}
        visible={showDetails}
        onClose={() => setShowDetails(false)}
        onContactDriver={() => {}}
        onCancel={() => {}}
        onComplete={() => {}}
        isPastRide={false}
        driverView={true}
        journeyView={journeyView}
        onApproveJourney={status.Status === "Pending" ? handleApproveBooking : undefined}
        showRebookOption={isExpiredCommuter}
      />
    </TouchableOpacity>
  );
};

export default DriverRideCard;