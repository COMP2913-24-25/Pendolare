import { View, TouchableOpacity, ActivityIndicator } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import { BookingDetails } from "@/services/bookingService";
import StatusBadge from "./StatusBadge";
import CronVisualizer from "./CronVisualiser";
import { getNextCronDates } from "@/utils/cronTools";
import OneClickRebook from "./OneClickRebook";
import CheckoutModal from "./Modals/CheckoutModal";

interface UpcomingRideCardProps {
  booking?: BookingDetails;
  onPress: () => void;
}

/*
    UpcomingRideCard
    Card for upcoming ride in ride view
*/
const UpcomingRideCard = ({ booking, onPress }: UpcomingRideCardProps) => {
  const { isDarkMode } = useTheme();
  
  // Log the booking data to see its structure
  console.log("UpcomingRideCard received booking:", booking);
  
  // Super minimal validation - just check if we have something to show
  const isValidBooking = !!booking && 
                       typeof booking === 'object' &&
                       (!!booking.Journey || !!booking.Booking);
  
  if (!isValidBooking) {
    console.log("Invalid booking data for card:", booking);
    return (
      <TouchableOpacity
        className={`p-4 rounded-lg shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"} items-center`}
        onPress={onPress}
        disabled={true}
      >
        <ActivityIndicator size="small" color="#2563EB" className="mb-2" />
        <Text className="text-gray-500">Loading ride details...</Text>
      </TouchableOpacity>
    );
  }
  
  // Safely extract data with fallbacks for everything
  const journey = booking.Journey || {};
  const rideDetails = booking.Booking || {};
  const status = booking.BookingStatus || { Status: "Unknown" };
  
  // Handle missing properties with fallbacks
  const endName = journey.EndName || 'Destination';
  const price = journey.Price || 0;
  
  // Safely get driver name
  let driverName = 'Driver';
  if (journey.User) {
    const user = journey.User;
    if (typeof user === 'object') {
      if (user.Name) driverName = user.Name;
      else if (user.FullName) driverName = user.FullName;
      else if (user.FirstName) driverName = user.FirstName;
    }
  }

  if (booking.Journey.Recurrance) {
    // get next date from cron
    
    const startDate = rideDetails.RideTime < new Date() ? new Date() : rideDetails.RideTime;

    const endDate = new Date(Date.now() + (1000 * 60 * 60 * 24 * 30));

    const cron = booking.Journey.Recurrance;
    const nextDate = getNextCronDates(cron, startDate, endDate, 1)[0];
    if (nextDate) {
      rideDetails.RideTime = nextDate;
    }
  }
  
  // Safe date conversion
  let rideTime = new Date();
  try {
    if (rideDetails.RideTime) {
      if (typeof rideDetails.RideTime === 'string') {
        rideTime = new Date(rideDetails.RideTime);
      } else if (rideDetails.RideTime instanceof Date) {
        rideTime = rideDetails.RideTime;
      }
    }
  } catch (e) {
    console.error("Error parsing ride time:", e);
  }

  return (
    <TouchableOpacity
      className={`p-4 rounded-lg shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
      onPress={onPress}
    >
      <View className="flex-row justify-between items-center mb-2">
        <Text
          className="text-lg font-JakartaBold flex-1"
          numberOfLines={3}
          adjustsFontSizeToFit
          minimumFontScale={1}
        >
          {endName}
        </Text>
        <Text className="text-blue-600 font-JakartaBold ml-2">
          £{price.toFixed(2)}
        </Text>
      </View>
      <View className="flex-row justify-between items-center mb-2">
        <Text className="text-gray-500">{rideTime.toUTCString()}</Text>
        <Text className="text-gray-800 font-JakartaSemiBold">With {driverName}</Text>
      </View>
      <StatusBadge statusText={status.Status} />
      {(booking.Journey.Recurrance &&     
      <View className="mt-2">
        <CronVisualizer
          cron={booking.Journey.Recurrance}
          endDate={rideTime}
          isDarkMode={isDarkMode}
          />
            <View>
              <OneClickRebook onRebook={() => console.log("Rebook clicked")} />
              {/*<CheckoutModal*/}
            </View>
      </View>)}
    </TouchableOpacity>
  );
};

export default UpcomingRideCard;
