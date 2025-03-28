import React, { useState, useEffect } from "react";
import { FontAwesome5 } from "@expo/vector-icons";
import { View, TouchableOpacity, Modal, Alert, ActivityIndicator } from "react-native";
import { router } from "expo-router";

import Map from "../../Map/Map";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText";
import StatusBadge from "../StatusBadge";
import CronVisualizer from "../CronVisualiser";
import CommuterScheduleAmendmentModal from "./CommuterScheduleAmendmentModal";
import { BookingDetails } from "@/services/bookingService";
import { getUserConversations } from "@/services/messageService";

interface UpcomingRideDetailsModalProps {
  booking?: BookingDetails;
  visible: boolean;
  onClose: () => void;
  onContactDriver: () => void;
  onCancel: () => void;
  onComplete: () => void;
  onApproveJourney?: () => void;
  isPastRide: boolean;
  driverView?: boolean;
  journeyView?: boolean;
  children?: React.ReactNode;
}

/*
    UpcomingRideDetailsModal
    Modal component for viewing upcoming ride details.
*/
const UpcomingRideDetailsModal = ({
  booking,
  visible,
  onClose,
  onContactDriver,
  onCancel,
  onComplete,
  isPastRide,
  driverView = false,
  journeyView = false,
  onApproveJourney = () => {},
  children,
}: UpcomingRideDetailsModalProps) => {
  const { isDarkMode } = useTheme();
  const [showScheduleAmendmentModal, setShowScheduleAmendmentModal] = useState(false);

  useEffect(() => {
    if (booking) {
      console.log("Booking structure:", {
        hasJourney: !!booking.Journey,
        journeyType: typeof booking.Journey,
        journeyKeys: booking.Journey ? Object.keys(booking.Journey) : [],
        hasBooking: !!booking.Booking,
        hasStatus: !!booking.BookingStatus
      });

      console.log("Booking details:", booking.Journey.Recurrance);
      
      // If Journey exists but is empty, log that specifically
      if (booking.Journey && Object.keys(booking.Journey).length === 0) {
        console.log("Journey object exists but is empty!");
      }
    }
  }, [booking]);

  // Most minimal validation possible - just check if booking exists
  const isValidBooking = !!booking;
  
  // Extract journey data with proper typing
  let journey: Partial<BookingDetails['Journey']> = {};
  let rideDetails: Partial<BookingDetails['Booking']> = {};
  let status: Partial<BookingDetails['BookingStatus']> = { Status: "Unknown" };
  
  if (isValidBooking) {
    // Check if Journey is an actual object with properties
    if (booking.Journey && typeof booking.Journey === 'object') {
      journey = booking.Journey;
      
      // Log any journey properties that are undefined
      console.log("Journey property check:", {
        startName: journey.StartName ?? "undefined",
        endName: journey.EndName ?? "undefined",
        price: journey.Price ?? "undefined",
        startLat: journey.StartLat ?? "undefined",
        endLat: journey.EndLat ?? "undefined"
      });
    }
    
    if (booking.Booking && typeof booking.Booking === 'object') {
      rideDetails = booking.Booking;
    }
    
    if (booking.BookingStatus && typeof booking.BookingStatus === 'object') {
      status = booking.BookingStatus;
    }
  }

  // Check if booking is a past ride 
  let rideTime = new Date();
  let pickup = null;
  let dropoff = null;
  let isCommuterJourney = false;

  if (isValidBooking) {
    // Try to convert ride time safely
    try {
      if (rideDetails.RideTime) {
        rideTime = typeof rideDetails.RideTime === 'string' 
          ? new Date(rideDetails.RideTime) 
          : rideDetails.RideTime;
      }
    } catch (error) {
      console.error("Error parsing ride time:", error);
    }

    // Create pickup object with more specific property checks
    const startName = journey.StartName || null;
    const startLat = journey.StartLat !== undefined ? journey.StartLat : null;
    const startLong = journey.StartLong !== undefined ? journey.StartLong : null;
    
    if (startName && startLat !== null && startLong !== null) {
      pickup = {
        name: startName,
        latitude: startLat,
        longitude: startLong
      };
    }

    // Create dropoff object with more specific property checks
    const endName = journey.EndName || null;
    const endLat = journey.EndLat !== undefined ? journey.EndLat : null;
    const endLong = journey.EndLong !== undefined ? journey.EndLong : null;
    
    if (endName && endLat !== null && endLong !== null) {
      dropoff = {
        name: endName,
        latitude: endLat,
        longitude: endLong
      };
    }

    // Check for commuter journey
    isCommuterJourney = !!journey.Recurrance;
  }

  // Function to handle contacting the driver or passenger
  const handleContactPerson = async () => {
    if (!booking || !booking.Journey?.User?.UserId) {
      // Call the original callback if booking is not valid
      onContactDriver();
      return;
    }
    
    // Get the ID of the person to contact (driver or passenger depending on view)
    const personId = driverView 
      ? booking.Booking?.User?.UserId 
      : booking.Journey?.User?.UserId;
    
    const personName = driverView
      ? booking.Booking?.User?.Name || "Passenger"
      : booking.Journey?.User?.Name || "Driver";
    
    if (!personId) {
      console.error("Could not find user ID for contact");
      onContactDriver(); // Fallback to original handler
      return;
    }
    
    try {
      // Find existing conversation first
      const existingConversations = await getUserConversations();
      
      // Navigate to existing conversation if found
      router.push({
        pathname: '/home/chat/[id]',
        params: { 
          id: personId,
          name: personName,
          // Don't include an initial message to prevent auto-conversation creation
        }
      });
      
      // Close the modal after navigating
      onClose();
    } catch (error) {
      console.error("Error navigating to chat:", error);
      onContactDriver(); // Fallback to original handler
    }
  };

  // Conditionally render sections based on available data
  const canShowMap = pickup !== null && dropoff !== null;
  const canShowPrice = journey.Price !== undefined && journey.Price !== null;
  const canShowStatus = status && status.Status;

  return (
    <Modal visible={visible} animationType="slide" onRequestClose={onClose}>
      <View className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-white"}`}>
        {!isValidBooking ? (
          // Display a loading state if booking data is not valid
          <View className="flex-1 justify-center items-center p-5">
            <ActivityIndicator size="large" color="#2563EB" className="mb-4" />
            <Text className="text-center text-lg">Loading ride details...</Text>
            <TouchableOpacity
              onPress={onClose}
              className="mt-8 p-4 bg-blue-600 rounded-xl"
            >
              <Text className="text-white text-center font-JakartaBold">Close</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <>
            <View className="h-1/3">
              {canShowMap ? (
                <Map pickup={pickup} dropoff={dropoff} />
              ) : (
                <View className="flex-1 justify-center items-center bg-gray-200">
                  <Text>Map not available</Text>
                </View>
              )}

              <TouchableOpacity
                onPress={onClose}
                className={`absolute top-12 left-4 z-10 p-2 rounded-full ${
                  isDarkMode ? "bg-slate-800" : "bg-white"
                }`}
              >
                <FontAwesome5
                  name={icons.backArrow}
                  size={24}
                  color={isDarkMode ? "#FFF" : "#000"}
                />
              </TouchableOpacity>
            </View>

            <View className="p-5 flex-1">
              <Text className="text-2xl font-JakartaBold mt-4 mb-4">Ride Details</Text>

              <View
                className={`p-4 rounded-xl mb-4 ${
                  isDarkMode ? "bg-slate-800" : "bg-gray-50"
                }`}
              >
                {canShowStatus && <StatusBadge statusText={status.Status!} />}

                {journey.StartName && (
                  <View className="mb-3 mt-3">
                    <Text>From</Text>
                    <Text className="font-JakartaMedium">{journey.StartName}</Text>
                  </View>
                )}

                {journey.EndName && (
                  <View className="mb-3">
                    <Text>To</Text>
                    <Text className="font-JakartaMedium">{journey.EndName}</Text>
                  </View>
                )}

                <View className="mb-3">
                  <Text>Departure</Text>
                  <Text className="font-JakartaMedium">{rideTime.toUTCString()}</Text>
                </View>

                {canShowPrice && journey.Price !== undefined && (
                  <View>
                    <Text>Price</Text>
                    <Text className="font-JakartaMedium">{`£${journey.Price.toFixed(2)}`}</Text>
                  </View>
                )}
                
                {/* Schedule visualization */}
                {isCommuterJourney && journey.Recurrance && journey.RepeatUntil && (
                  <View className="mt-4">
                    <CronVisualizer 
                      cron={journey.Recurrance}
                      endDate={typeof journey.RepeatUntil === 'string' 
                        ? new Date(journey.RepeatUntil) 
                        : journey.RepeatUntil}
                      isDarkMode={isDarkMode}
                    />
                  </View>
                )}
              </View>

              {!journeyView && <View className="flex-row gap-4 flex-wrap">
                <TouchableOpacity
                  onPress={handleContactPerson}
                  className="flex-1 bg-blue-600 p-4 rounded-xl"
                >
                  <Text className="text-white text-center font-JakartaBold">
                    {driverView ? "Contact Passenger" : "Contact Driver"}
                  </Text>
                </TouchableOpacity>

                {isPastRide ? (
                  <TouchableOpacity
                    onPress={onComplete}
                    className="flex-1 bg-green-600 p-4 rounded-xl"
                  >
                    <Text className="text-white text-center font-JakartaBold">
                      Confirm Completion
                    </Text>
                  </TouchableOpacity>
                ) : (
                  <TouchableOpacity
                    onPress={onCancel}
                    className="flex-1 bg-red-600 p-4 rounded-xl"
                  >
                    <Text className="text-white text-center font-JakartaBold">
                      Cancel Ride
                    </Text>
                  </TouchableOpacity>
                )}

                {!isPastRide && driverView && status.Status === "Pending" && (
                  <TouchableOpacity className="flex-1 bg-blue-600 p-4 rounded-xl"
                    onPress={() => {
                      Alert.alert("Approve Journey", "Are you sure you want to approve this journey?\n\nPlease ensure no booking ammendments have been made.", [
                        { text: "No", onPress: () => {}, style: "cancel" },
                        { text: "Yes", onPress: () => onApproveJourney()}
                      ]);
                    }}>
                    <Text className="text-center text-white font-JakartaBold">
                      Approve Journey
                    </Text>
                  </TouchableOpacity>
                )}

                {/* Add button for commuter schedule amendment */}
                {isCommuterJourney && (
                  <TouchableOpacity
                    onPress={() => setShowScheduleAmendmentModal(true)}
                    className="flex-1 bg-indigo-600 p-4 rounded-xl mt-2"
                  >
                    <Text className="text-white text-center font-JakartaBold">
                      Amend Schedule
                    </Text>
                  </TouchableOpacity>
                )}
              </View>}
            </View>

            {/* Commuter Schedule Amendment Modal - only show if booking is valid */}
            {isValidBooking && (
              <CommuterScheduleAmendmentModal
                visible={showScheduleAmendmentModal}
                onClose={() => setShowScheduleAmendmentModal(false)}
                booking={booking}
                isDriver={driverView}
              />
            )}
          </>
        )}
      </View>
      {children}
    </Modal>
  );
};

export default UpcomingRideDetailsModal;