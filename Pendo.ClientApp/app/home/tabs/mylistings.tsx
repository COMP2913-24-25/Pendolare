import { View, TouchableOpacity, ScrollView } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import { SafeAreaView } from "react-native-safe-area-context";
import { useState, useEffect, useCallback } from "react";
import { useFocusEffect } from "expo-router";

import UpcomingRide from "@/components/RideView/UpcomingRide";
import DriverRideCard from "@/components/RideView/DriverRideCard";

import { getBookings } from "@/services/bookingService";
import { getJourneys, JourneyDetails } from "@/services/journeyService";
import { convertRideToBookingDetails, Ride } from "@/utils/bookingUtils";

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
      console.log("Fetching bookings with driverView=true");
      const response = await getBookings(true);

      console.log(
        `Raw bookings response, found ${response.bookings?.length || 0} bookings:`,
        response.bookings?.length > 0 ? "Data exists" : "No data"
      );

      if (!response.success || !response.bookings || response.bookings.length === 0) {
        console.log("No bookings found or API request was unsuccessful");
        setBookedJourneys([]);
        setPastJourneys([]);
        return;
      }

      const bookings = response.bookings || [];

      const upcoming = bookings.filter((booking) => {
        const rideTime = booking.Booking?.RideTime
          ? typeof booking.Booking.RideTime === "string"
            ? new Date(booking.Booking.RideTime)
            : booking.Booking.RideTime
          : new Date();

        const isPending = booking.BookingStatus?.Status === "Pending";
        const isConfirmed = booking.BookingStatus?.Status === "Confirmed";
        const isFuture = rideTime > new Date();
        return (isPending || isConfirmed) && isFuture;
      });

      const past = bookings.filter((booking) => {
        const rideTime = booking.Booking?.RideTime
          ? typeof booking.Booking.RideTime === "string"
            ? new Date(booking.Booking.RideTime)
            : booking.Booking.RideTime
          : new Date();

        const isCancelled = booking.BookingStatus?.Status === "Cancelled";
        const isPast = rideTime <= new Date();
        return isCancelled || isPast;
      });

      console.log(`Filtered: ${upcoming.length} upcoming, ${past.length} past bookings`);

      setBookedJourneys(upcoming);
      setPastJourneys(past);
    } catch (error) {
      console.error("Error fetching bookings:", error);
      setBookedJourneys([]);
      setPastJourneys([]);
    }
  };

  const fetchJourneys = async () => {
    const response = await getJourneys({
      StartDate: new Date().toISOString(),
      DriverView: true,
    });

    console.log(`Fetched ${response.journeys.length} journeys`);
    console.log(response.journeys);

    const journeys: Ride[] = response.journeys.map((journey: JourneyDetails) => ({
      BookingId: "N/A",
      Status: "Advertised",
      PassengerName: "N/A",
      JourneyId: journey.JourneyId,
      DriverId: journey.UserId,
      DriverName: journey.User_.FirstName,
      RideTime: new Date(journey.StartDate),
      Price: journey.AdvertisedPrice,
      Pickup: {
        latitude: journey.StartLat,
        longitude: journey.StartLong,
        name: journey.StartName,
      },
      Dropoff: {
        latitude: journey.EndLat,
        longitude: journey.EndLong,
        name: journey.EndName,
      },
    }));

    setAdvertisedJourneys(journeys.sort((a, b) => a.RideTime.getTime() - b.RideTime.getTime()));
  };

  useEffect(() => {
    fetchJourneys();
    fetchBookings();
  }, []);

  useFocusEffect(
    useCallback(() => {
      console.log("My Listings tab focused - refreshing data");
      fetchBookings();
      fetchJourneys();
      return () => {
        // Cleanup if needed
      };
    }, [])
  );

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
        <View className="mb-20">
          {currentTab === "Booked" &&
            (bookedJourneys.length > 0 ? (
              bookedJourneys.map((booking, index) => (
                <View key={index}>
                  <DriverRideCard
                    booking={booking}
                    approveBookingCallback={() => fetchBookings()}
                  />
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
                <View key={index}>
                  <DriverRideCard 
                    booking={convertRideToBookingDetails(journey)} 
                    journeyView={true} 
                  />
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
                  <DriverRideCard 
                    booking={convertRideToBookingDetails(journey)} 
                    journeyView={true} 
                  />
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