import { router } from "expo-router";
import { useState } from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { View } from "react-native";

import CancellationReasonModal from "./Modals/CancellationReasonModal";
import LateCancellationModal from "./Modals/LateCancellationModal";
import RatingModal from "./Modals/RatingModal";
import RideCompletionModal from "./Modals/RideCompletionModal";
import UpcomingRideDetailsModal from "./Modals/UpcomingRideDetailsModal";
import UpcomingRideCard from "./UpcomingRideCard";

interface UpcomingRideProps {
  ride: {
    id: number;
    driverName: string;
    driverId: number;
    departureTime: number;
    price: string;
    pickup: any;
    dropoff: any;
    status?: string;
    rating?: number;
  };
}

/*
    UpcomingRide
    Component for an upcoming ride in ride view
*/
const UpcomingRide = ({ ride }: UpcomingRideProps) => {
  const [showDetails, setShowDetails] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [showLateCancelWarning, setShowLateCancelWarning] = useState(false);
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [rating, setRating] = useState(0);
  const [showCompletionModal, setShowCompletionModal] = useState(false);
  const insets = useSafeAreaInsets();

  // Check if the ride is within 15 minutes of departure
  const isLastMinuteCancellation = () => {
    const now = Date.now();
    const fifteenMinutes = 15 * 60 * 1000;
    return ride.departureTime - now <= fifteenMinutes;
  };

  const isPastRide = () => {
    return Date.now() > ride.departureTime;
  };

  const handleCancelAttempt = () => {
    if (isLastMinuteCancellation()) {
      setShowLateCancelWarning(true);
    } else {
      setShowCancelModal(true);
    }
  };

  const handleCancel = async (reason: string) => {
    try {
      await Promise.resolve(); // Replace with actual API call
      setShowCancelModal(false);
      setShowDetails(false);
    } catch (error) {
      console.error("Error cancelling ride:", error);
    }
  };

  const handleContactDriver = async () => {
    try {
      setShowDetails(false);
      // Small delay to allow modal to start closing
      await new Promise((resolve) => setTimeout(resolve, 100));
      router.push(`/home/chat/${ride.driverId}`);
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
      router.push("/home/chat/1");
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
    <View style={{ paddingTop: insets.top > 0 ? insets.top : 20 }}>
      <UpcomingRideCard ride={ride} onPress={() => setShowDetails(true)} />

      <UpcomingRideDetailsModal
        ride={ride}
        visible={showDetails}
        onClose={() => setShowDetails(false)}
        onContactDriver={handleContactDriver}
        onCancel={handleCancelAttempt}
        onComplete={handleCompletionStart}
        isPastRide={isPastRide()}
      />

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
        driverName={ride.driverName}
        rating={rating}
        setRating={setRating}
        onClose={() => setShowRatingModal(false)}
        onSubmit={handleRate}
      />

      <RideCompletionModal
        visible={showCompletionModal}
        driverName={ride.driverName}
        rating={rating}
        setRating={setRating}
        onClose={() => setShowCompletionModal(false)}
        onSubmit={handleComplete}
        onDispute={handleDisputeRide}
      />
    </View>
  );
};

export default UpcomingRide;
