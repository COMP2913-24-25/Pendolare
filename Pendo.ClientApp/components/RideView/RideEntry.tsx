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
    driverName: ride.User_.FirstName || ride.User_.LastName || "Unknown Driver",
    rating: typeof ride.User_.UserRating !== "undefined" ? ride.User_.UserRating : -1,
    price:
      typeof ride.AdvertisedPrice === "number"
        ? `£${ride.AdvertisedPrice.toFixed(2)}`
        : ride.price || "",
    departureTime: new Date(ride.StartTime || ride.StartDate).toUTCString(),
    pickup: { name: ride.StartName || (ride.pickup && ride.pickup.name) || "Unknown Pickup" },
    dropoff: { name: ride.EndName || (ride.dropoff && ride.dropoff.name) || "Unknown Dropoff" },
    JourneyId: ride.JourneyId || ride.id,
    recurrence: ride.Recurrance,
    repeatUntil: ride.RepeatUntil,
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
