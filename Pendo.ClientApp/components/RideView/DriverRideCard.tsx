import { router } from "expo-router";
import { useState } from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Alert, View } from "react-native";

import UpcomingRideDetailsModal from "./Modals/UpcomingRideDetailsModal";
import UpcomingRideCard from "./UpcomingRideCard";

import { approveBooking } from "@/services/bookingService";

interface DriverRideCardProps {
  ride: any;
  journeyView?: boolean;
  approveBookingCallback?: () => void;
}

/*
    DriverUpcomingRide
    Component for an upcoming ride from the driver's perspective.
    This version removes ride cancellation and completion functionality.
*/
const DriverRideCard = ({ ride, journeyView = false, approveBookingCallback }: DriverRideCardProps) => {
  const [showDetails, setShowDetails] = useState(false);
  const insets = useSafeAreaInsets();

  const handleContactPassenger = async () => {
    try {
      setShowDetails(false);
      // Small delay to allow modal to start closing
      await new Promise((resolve) => setTimeout(resolve, 100));
      router.push(`/home/chat/${ride.PassengerId}?name=${ride.PassengerName}`);
    } catch (error) {
      console.error("Error navigating to chat:", error);
    }
  };

  // Ensure consistent top spacing
  insets.top = 0;

  return (
    <View style={{ paddingTop: insets.top > 0 ? insets.top : 20 }}>
      <UpcomingRideCard ride={ride} onPress={() => setShowDetails(true)} />
      <UpcomingRideDetailsModal
        visible={showDetails}
        ride={ride}
        onClose={() => setShowDetails(false)}
        onCancel={() => {}}
        onContactDriver={() => handleContactPassenger()}
        onComplete={() => {}}
        isPastRide={false}
        driverView={true}
        journeyView={journeyView}
        onApproveJourney={() => { 
          approveBooking(ride.BookingId).then((response) => {
            if (response.Status !== "Error") {
              Alert.alert("Journey Approved Successfully.");
              setShowDetails(false);
              approveBookingCallback && approveBookingCallback();
            } else {
              Alert.alert("Failed to approve journey", `${response.Message}`);
            }
          });
        }}
      />
    </View>
  );
};

export default DriverRideCard;