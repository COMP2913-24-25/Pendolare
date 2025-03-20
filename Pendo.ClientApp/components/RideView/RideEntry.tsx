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

  // Normalise the ride object from journey data
  const normalisedRide = {
    driverName: ride.driverName || "Unknown Driver",
    rating: ride.rating || 0,
    price:
      typeof ride.AdvertisedPrice === "number"
        ? `£${ride.AdvertisedPrice.toFixed(2)}`
        : ride.price || "",
    departureTime: ride.StartTime || ride.departureTime || "",
    pickup: { name: ride.StartName || (ride.pickup && ride.pickup.name) || "Unknown Pickup" },
    dropoff: { name: ride.EndName || (ride.dropoff && ride.dropoff.name) || "Unknown Dropoff" },
    JourneyId: ride.JourneyId || ride.id,
    ...ride,
  };

  return (
    <>
      <RideEntryCard ride={normalisedRide} onPress={() => setShowDetails(true)} />
      <RideDetails
        ride={normalisedRide}
        visible={showDetails}
        onClose={() => setShowDetails(false)}
      />
    </>
  );
};

export default RideEntry;
