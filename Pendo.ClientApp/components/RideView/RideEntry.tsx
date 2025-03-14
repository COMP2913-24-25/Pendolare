import { useState } from "react";

import RideEntryCard from "./RideEntryCard";

import RideDetails from "@/components/RideView/RideDetails";

interface RideEntryProps {
  ride: any;
}

/*
  RideEntry
  Ride entry component for displaying a ride
*/
const RideEntry = ({ ride }: RideEntryProps) => {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <>
      <RideEntryCard ride={ride} onPress={() => setShowDetails(true)} />

      <RideDetails
        ride={ride}
        visible={showDetails}
        onClose={() => setShowDetails(false)}
      />
    </>
  );
};

export default RideEntry;
