import { router } from "expo-router";
import { useState } from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { View } from "react-native";

import UpcomingRideDetailsModal from "./Modals/UpcomingRideDetailsModal";
import UpcomingRideCard from "./UpcomingRideCard";

interface DriverRideCardProps {
  ride: any;
}

/*
    DriverUpcomingRide
    Component for an upcoming ride from the driver's perspective.
    This version removes ride cancellation and completion functionality.
*/
const DriverRideCard = ({ ride }: DriverRideCardProps) => {
  const [showDetails, setShowDetails] = useState(false);
  const insets = useSafeAreaInsets();

  // Ensure consistent top spacing
  insets.top = 0;

  return (
    <View style={{ paddingTop: insets.top > 0 ? insets.top : 20 }}>
      <UpcomingRideCard ride={ride} onPress={() => setShowDetails(true)} />
    </View>
  );
};

export default DriverRideCard;