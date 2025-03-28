import { router } from "expo-router";
import { useState } from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { View, ActivityIndicator } from "react-native";

import CancellationReasonModal from "./Modals/CancellationReasonModal";
import LateCancellationModal from "./Modals/LateCancellationModal";
import RatingModal from "./Modals/RatingModal";
import RideCompletionModal from "./Modals/RideCompletionModal";
import UpcomingRideDetailsModal from "./Modals/UpcomingRideDetailsModal";
import UpcomingRideCard from "./UpcomingRideCard";
import { BookingDetails, User } from "@/services/bookingService";
import { cancelBooking } from "@/services/bookingService";
import { createConversation } from "@/services/messageService";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";

interface UpcomingRideProps {
  booking?: BookingDetails;
  onPress?: () => void;
}

/*
    UpcomingRide
    Component for an upcoming ride in ride view
*/
const UpcomingRide = ({ booking, onPress }: UpcomingRideProps) => {
  const { isDarkMode } = useTheme();
  const [showDetails, setShowDetails] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [showLateCancelWarning, setShowLateCancelWarning] = useState(false);
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [rating, setRating] = useState(0);
  const [showCompletionModal, setShowCompletionModal] = useState(false);
  const insets = useSafeAreaInsets();

  // Check if booking is valid
  // This is a more explicit check to ensure booking is not null or undefined
  const isValidBooking = !!booking;

  // Handle missing data gracefully
  if (!isValidBooking) {
    console.log("No booking data available");
    return (
      <View style={{ paddingTop: insets.top > 0 ? insets.top : 20 }}>
        <View
          className={`p-4 rounded-lg shadow-sm ${
            isDarkMode ? "bg-slate-800" : "bg-white"
          } items-center`}
        >
          <ActivityIndicator size="small" color="#2563EB" className="mb-2" />
          <Text className="text-gray-500">Loading ride details...</Text>
        </View>
      </View>
    );
  }

  // Extract driver information safely
  let driverId = "";
  let driverName = "Driver";

  if (booking.Journey.User) {
    if (typeof booking.Journey.User === "object") {
      if ("UserId" in booking.Journey.User) {
        driverId = booking.Journey.User.UserId;
      }
      if ("Name" in booking.Journey.User) {
        driverName = booking.Journey.User.Name ?? "Driver";
      }
    }
  }

  // Get RideTime safely
  let rideTime: Date;
  try {
    if (typeof booking.Booking.RideTime === "string") {
      rideTime = new Date(booking.Booking.RideTime);
    } else if (booking.Booking.RideTime instanceof Date) {
      rideTime = booking.Booking.RideTime;
    } else {
      rideTime = new Date();
    }
  } catch (e) {
    rideTime = new Date();
  }

  const isLastMinuteCancellation = () => {
    const now = Date.now();
    const fifteenMinutes = 15 * 60 * 1000;
    return rideTime.getTime() - now <= fifteenMinutes;
  };

  const isPastRide = () => {
    return Date.now() > rideTime.getTime();
  };

  const handleCancelAttempt = () => {
    console.log("Handling cancellation.");

    if (isLastMinuteCancellation()) {
      setShowLateCancelWarning(true);
    } else {
      setShowCancelModal(true);
    }
  };

  const handleCancel = async (reason: string) => {
    try {
      await cancelBooking(booking.Booking.BookingId, reason);

      setShowCancelModal(false);
      await new Promise((resolve) => setTimeout(resolve, 100));

      setShowDetails(false);
      await new Promise((resolve) => setTimeout(resolve, 100));

      router.push(
        `/home/chat/${driverId}?name=${driverName}&initialMessage=Ride cancelled for reason: ${reason}.`
      );

      console.log(`Ride cancelled for reason: ${reason}`);
    } catch (error) {
      console.error("Error cancelling ride:", error);
    }
  };

  const handleContactDriver = async () => {
    try {
      setShowDetails(false);
      // Small delay to allow modal to start closing
      await new Promise((resolve) => setTimeout(resolve, 100));

      // Explicitly create a conversation before navigating
      // This ensures the conversation exists when the user navigates to the chat page
      try {
        const conversationResponse = await createConversation({
          ConversationType: "direct",
          name: `Chat with ${driverName}`,
          participants: [driverId],
        });

        console.log("Successfully created conversation:", conversationResponse);
      } catch (error) {
        // If creation fails, the chat page will try again
        console.log(
          "Could not pre-create conversation, will try in chat page:",
          error
        );
      }

      // Navigate to chat page with properly encoded parameters
      router.push(
        `/home/chat/${driverId}?name=${encodeURIComponent(driverName)}`
      );
    } catch (error) {
      console.error("Error navigating to chat:", error);
    }
  };

  const handleDisputeRide = async () => {
    try {
      setShowCompletionModal(false);
      setShowDetails(false);
      // Small delay to allow modals to start closing
      await new Promise((resolve) => setTimeout(resolve, 100));
      console.log(`DRIVER ID: ${driverId}`);
      router.push(`/home/chat/${driverId}`);
    } catch (error) {
      console.error("Error navigating to support:", error);
    }
  };

  const handleRate = async () => {
    try {
      // Replace with actual API call
      await Promise.resolve();
      setShowRatingModal(false);
      setShowDetails(false);
    } catch (error) {
      console.error("Error rating ride:", error);
    }
  };

  const handleCompletionStart = () => {
    setShowCompletionModal(true);
    setShowDetails(false);
  };

  const handleComplete = async () => {
    try {
      if (rating > 0) {
        await Promise.resolve(); // Replace with actual API call
        setShowCompletionModal(false);
      }
    } catch (error) {
      console.error("Error completing ride:", error);
    }
  };

  // Don't even ask! Only way I could fix the styling.
  insets.top = 0;

  return (
    <View>
      <UpcomingRideCard
        booking={booking}
        onPress={() => setShowDetails(true)}
      />
      <UpcomingRideDetailsModal
        booking={booking}
        visible={showDetails}
        onClose={() => setShowDetails(false)}
        onContactDriver={handleContactDriver}
        onCancel={handleCancelAttempt}
        onComplete={handleCompletionStart}
        isPastRide={isPastRide()}
      >
        <View>
          <LateCancellationModal
            visible={showLateCancelWarning}
            onClose={() => setShowLateCancelWarning(false)}
            onConfirm={() => {
              setShowLateCancelWarning(false);
              setShowCancelModal(true);
            }}
          />

          <CancellationReasonModal
            visible={showCancelModal}
            onCancel={() => setShowCancelModal(false)}
            onReasonSelect={handleCancel}
          />

          <RatingModal
            visible={showRatingModal}
            driverName={driverName}
            rating={rating}
            setRating={setRating}
            onClose={() => setShowRatingModal(false)}
            onSubmit={handleRate}
          />

          <RideCompletionModal
            visible={showCompletionModal}
            driverName={driverName}
            rating={rating}
            setRating={setRating}
            onClose={() => setShowCompletionModal(false)}
            onSubmit={handleComplete}
            onDispute={handleDisputeRide}
          />
        </View>
      </UpcomingRideDetailsModal>
    </View>
  );
};

export default UpcomingRide;
