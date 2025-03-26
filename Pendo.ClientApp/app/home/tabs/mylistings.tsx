import { View, TouchableOpacity, ScrollView } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import { SafeAreaView } from "react-native-safe-area-context";
import { useState, useEffect } from "react";
import UpcomingRide from "@/components/RideView/UpcomingRide";
import { Ride } from "@/constants";
import DriverRideCard from "@/components/RideView/DriverRideCard";

import { getBookings } from "@/services/bookingService";
import { getJourneys } from "@/services/journeyService";

/*
  MyListings
  Page to display the journeys created by the user.
*/
const MyListings = () => {
  const { isDarkMode } = useTheme();
  const [currentTab, setCurrentTab] = useState("Booked");
  const [bookedJourneys, setBookedJourneys] = useState<any[]>([]);
  const [advertisedJourneys, setAdvertisedJourneys] = useState<any[]>([]);
  const [pastJourneys, setPastJourneys] = useState<any[]>([]);

  const fetchBookings = async () => {
    try {
      const response = await getBookings(true);
      
      // Process the response to transform the bookings into Ride objects
      const allRides: Ride[] = response.bookings.map((booking: any) => ({
        BookingId: booking.Booking.BookingId,
        JourneyId: booking.Journey.JourneyId,
        RideTime: new Date(booking.Booking.RideTime),
        Status: booking.BookingStatus.Status,
        DriverName: booking.Journey.User.FirstName,
        PassengerName: booking.Booking.User.FirstName,
        DriverId: booking.Journey.User.UserId,
        Price: booking.Journey.Price,
        Pickup: {
          latitude: booking.Journey.StartLat,
          longitude: booking.Journey.StartLong,
          name: booking.Journey.StartName
        },
        Dropoff: {
          latitude: booking.Journey.EndLat,
          longitude: booking.Journey.EndLong,
          name: booking.Journey.EndName
        }
      }));

      allRides.forEach(ride => console.log(ride.DriverId));

      const cancelled = allRides.filter(ride => ride.Status === "Cancelled");
      const upcoming = allRides.filter(ride => ride.RideTime.getTime() > Date.now() && !cancelled.includes(ride))
        .sort((a, b) => a.RideTime.getTime() - b.RideTime.getTime());

      const past = allRides
        .filter(ride => ride.RideTime.getTime() <= Date.now())
        .concat(cancelled)
        .sort((a, b) => b.RideTime.getTime() - a.RideTime.getTime());

      //  Update state with the retrieved rides
      setBookedJourneys(upcoming);
      setPastJourneys(past);
    } catch (error) {
      console.error('Error fetching bookings:', error);
    }
  };

  const fetchJourneys = async () => {
    const response = await getJourneys(undefined, true);
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  return (
    <SafeAreaView
      className={`flex-1 pt-2 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
    >
      <ScrollView className="flex-1 px-4">
        <Text
          className={`text-2xl font-JakartaExtraBold mb-4 ${
            isDarkMode ? "text-white" : "text-black"
          }`}
        >
          My Listings
        </Text>

        {/* Tabs */}
        <View
          className={`flex-row rounded-xl p-1 ${
            isDarkMode ? "bg-slate-800" : "bg-gray-100"
          }`}
        >
          <TouchableOpacity
            className={`flex-1 py-2 rounded-lg ${
              currentTab === "Booked"
                ? isDarkMode
                  ? "bg-slate-700"
                  : "bg-white shadow"
                : ""
            }`}
            onPress={() => setCurrentTab("Booked")}
          >
            <Text
              className={`text-center font-JakartaMedium ${
                currentTab === "Booked"
                  ? "text-blue-600"
                  : isDarkMode
                  ? "text-gray-400"
                  : "text-gray-500"
              }`}
            >
              Bookings
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            className={`flex-1 py-2 rounded-lg ${
              currentTab === "Advertised"
                ? isDarkMode
                  ? "bg-slate-700"
                  : "bg-white shadow"
                : ""
            }`}
            onPress={() => setCurrentTab("Advertised")}
          >
            <Text
              className={`text-center font-JakartaMedium ${
                currentTab === "Advertised"
                  ? "text-blue-600"
                  : isDarkMode
                  ? "text-gray-400"
                  : "text-gray-500"
              }`}
            >
              Advertised
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            className={`flex-1 py-2 rounded-lg ${
              currentTab === "Past"
                ? isDarkMode
                  ? "bg-slate-700"
                  : "bg-white shadow"
                : ""
            }`}
            onPress={() => setCurrentTab("Past")}
          >
            <Text
              className={`text-center font-JakartaMedium ${
                currentTab === "Past"
                  ? "text-blue-600"
                  : isDarkMode
                  ? "text-gray-400"
                  : "text-gray-500"
              }`}
            >
              Past Journeys
            </Text>
          </TouchableOpacity>
        </View>

        {/* Journey List */}
        <View>
          {currentTab === "Booked" &&
            (bookedJourneys.length > 0 ? (
              bookedJourneys.map((journey, index) => (
                <View key={index}>
                  <DriverRideCard ride={journey} />
                </View>
              ))
            ) : (
              <View className="bg-white rounded-lg p-4 shadow-md mt-4">
                <Text className="text-gray-500">No booked journeys found</Text>
              </View>
            ))}

          {currentTab === "Advertised" &&
            (advertisedJourneys.length > 0 ? (
              advertisedJourneys.map((journey, index) => (
                <View key={index} className="mb-4">
                  <DriverRideCard ride={journey} />
                </View>
              ))
            ) : (
              <View className="bg-white rounded-lg p-4 shadow-md mt-4">
                <Text className="text-gray-500">
                  No advertised journeys found
                </Text>
              </View>
            ))}

          {currentTab === "Past" &&
            (pastJourneys.length > 0 ? (
              pastJourneys.map((journey, index) => (
                <View key={index}>
                  <DriverRideCard ride={journey} />
                </View>
              ))
            ) : (
              <View className="bg-white rounded-lg p-4 shadow-md mt-4">
                <Text className="text-gray-500">No past journeys found</Text>
              </View>
            ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default MyListings;