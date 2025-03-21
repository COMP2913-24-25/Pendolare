import { FontAwesome5 } from "@expo/vector-icons";
import { useState, useEffect } from "react";
import {
  View,
  TouchableOpacity,
  Modal,
  ScrollView,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import Map from "@/components/Map/Map";
import { Text } from "@/components/common/ThemedText";
import UpcomingRide from "@/components/RideView/UpcomingRide";
import { icons, Ride } from "@/constants";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";
import { USER_FIRST_NAME_KEY } from "@/services/authService";
import * as SecureStore from "expo-secure-store";
import { getBookings } from "@/services/bookingService";

/*
  Home
  Home screen for the app
*/
const Home = () => {
  const [showModal, setShowModal] = useState(false);
  const [showAllRides, setShowAllRides] = useState(false);
  const [currentJourneyTab, setCurrentJourneyTab] = useState("Upcoming");
  const { isDarkMode } = useTheme();
  const { logout } = useAuth();

  const [upcomingRides, setUpcomingRides] = useState<Ride[]>([]);
  const [pastRides, setPastRides] = useState<Ride[]>([]);
  const [cancelledRides, setCancelledRides] = useState<Ride[]>([]);
  const [nextRide, setNextRide] = useState<Ride | null>(null);
  const [userFirstName, setUserFirstName] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserFirstName = async () => {
      const storedFirstName = await SecureStore.getItemAsync(USER_FIRST_NAME_KEY);
      setUserFirstName(storedFirstName);
    };
    fetchUserFirstName();
  }, []);

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await getBookings();
        
        // Process the response to transform the bookings into Ride objects
        const allRides: Ride[] = response.bookings.map((booking: any) => ({
          BookingId: booking.Booking.BookingId,
          RideTime: new Date(booking.Booking.RideTime),
          Status: booking.BookingStatus.Status,
          DriverName: booking.Journey.User.FirstName,
          DriverId: booking.Journey.UserId,
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
        
        // Split the rides into upcoming and past based on the current time
        const cancelled = allRides.filter(ride => ride.Status === "Cancelled");
        const upcoming = allRides.filter(ride => ride.RideTime.getTime() > Date.now() && !cancelled.includes(ride));
        const past = allRides.filter(ride => ride.RideTime.getTime() <= Date.now());
        const next = upcoming.length > 0 ? upcoming[0] : null;

        // Update state with the retrieved rides
        setUpcomingRides(upcoming);
        setPastRides(past);
        setCancelledRides(cancelled);
        setNextRide(next);
      } catch (error) {
        console.error('Error fetching bookings:', error);
      }
    };

    fetchBookings();
  }, []);

  useEffect(() => {
    setCurrentJourneyTab("Upcoming");
  }, []);

  const confirmSignOut = async () => {
    setShowModal(false);
    // Call the logout function from the AuthContext
    await logout();
  };

  return (
    <SafeAreaView
      className={`flex-1 pt-2 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
    >
      <ScrollView className="flex-1">
        <View className="px-4">
          {/* Header */}
          <View className="flex-row justify-between items-center mb-2">
            <Text
              className={`text-2xl font-JakartaExtraBold ${isDarkMode ? "text-white" : "text-black"}`}
            >
              Welcome {userFirstName ?? ""} 👋
            </Text>
            <TouchableOpacity
              onPress={() => setShowModal(true)}
              className="p-2"
            >
              <FontAwesome5
                name={icons.out}
                size={24}
                color={isDarkMode ? "#FFF" : "#000"}
              />
            </TouchableOpacity>
          </View>

          {/* Map Section */}
          <Text
            className={`text-xl font-JakartaBold mt-2 mb-3 ${isDarkMode ? "text-white" : "text-black"}`}
          >
            Your current location
          </Text>
          <View className="h-[200px] border-2 border-gray-300 rounded-lg overflow-hidden">
            <Map pickup={null} dropoff={null} />
          </View>

          {/* Next Journey Section */}
          <View className="mt-2">
            <Text
              className={`text-xl font-JakartaBold mt-2 ${isDarkMode ? "text-white" : "text-black"}`}
            >
              Upcoming Journeys
            </Text>
            {nextRide ? (
              <UpcomingRide ride={nextRide} />
            ) : (
              <View className="bg-white rounded-lg p-4 shadow-md">
                <Text className="text-gray-500">No upcoming journeys</Text>
              </View>
            )}
          </View>

          {/* View All Journeys Button */}
          <TouchableOpacity
            onPress={() => setShowAllRides(true)}
            className="mt-4 bg-blue-600 py-3 rounded-xl"
          >
            <Text className="text-white text-center font-JakartaBold">
              View All Upcoming Journeys
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>

      {/* All Rides Modal */}
      <Modal
        visible={showAllRides}
        animationType="slide"
        onRequestClose={() => setShowAllRides(false)}
      >
        <SafeAreaView
          className={`flex-1 pt-4 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
        >
          <View className="flex-1 px-4">
            <View className="flex-row items-center justify-between my-5">
              <TouchableOpacity
                onPress={() => setShowAllRides(false)}
                className="p-2"
              >
                <FontAwesome5
                  name={icons.backArrow}
                  size={24}
                  color={isDarkMode ? "#FFF" : "#000"}
                />
              </TouchableOpacity>
              <Text
                className={`text-2xl font-JakartaBold ${isDarkMode ? "text-white" : "text-black"}`}
              >
                {currentJourneyTab}
              </Text>
              <View className="w-8" />
            </View>

            <View
              className={`flex-row rounded-xl p-1 ${isDarkMode ? "bg-slate-800" : "bg-gray-100"}`}
            >
              <TouchableOpacity
                className={`flex-1 py-2 rounded-lg ${
                  currentJourneyTab === "Upcoming"
                    ? isDarkMode
                      ? "bg-slate-700"
                      : "bg-white shadow"
                    : ""
                }`}
                onPress={() => setCurrentJourneyTab("Upcoming")}
              >
                <Text
                  className={`text-center font-JakartaMedium ${
                    currentJourneyTab === "Upcoming"
                      ? "text-blue-600"
                      : isDarkMode
                        ? "text-gray-400"
                        : "text-gray-500"
                  }`}
                >
                  Upcoming
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                className={`flex-1 py-2 rounded-lg ${
                  currentJourneyTab === "Past"
                    ? isDarkMode
                      ? "bg-slate-700"
                      : "bg-white shadow"
                    : ""
                }`}
                onPress={() => setCurrentJourneyTab("Past")}
              >
                <Text
                  className={`text-center font-JakartaMedium ${
                    currentJourneyTab === "Past"
                      ? "text-blue-600"
                      : isDarkMode
                        ? "text-gray-400"
                        : "text-gray-500"
                  }`}
                >
                  Past
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                className={`flex-1 py-2 rounded-lg ${
                  currentJourneyTab === "Cancelled"
                    ? isDarkMode
                      ? "bg-slate-700"
                      : "bg-white shadow"
                    : ""
                }`}
                onPress={() => setCurrentJourneyTab("Cancelled")}
              >
                <Text
                  className={`text-center font-JakartaMedium ${
                    currentJourneyTab === "Cancelled"
                      ? "text-blue-600"
                      : isDarkMode
                        ? "text-gray-400"
                        : "text-gray-500"
                  }`}
                >
                  Cancelled
                </Text>
              </TouchableOpacity>
            </View>

            <ScrollView
              showsVerticalScrollIndicator={false}
              contentContainerStyle={{ paddingTop: 8 }}
            >
              {(currentJourneyTab === "Cancelled" ? cancelledRides : (currentJourneyTab === "Upcoming" ? upcomingRides : pastRides)).map(
                (ride, index) => (
                  <View key={ride.BookingId} className={index > 0 ? "mt-4" : ""}>
                    <UpcomingRide ride={ride} />
                  </View>
                ),
              )}
              {(currentJourneyTab === "Cancelled" ? cancelledRides : (currentJourneyTab === "Upcoming" ? upcomingRides : pastRides)).length === 0 && (
                <View className="bg-white rounded-lg p-4 shadow-md">
                  <Text className="text-gray-500">
                    No {currentJourneyTab} journeys
                  </Text>
                </View>
              )}
            </ScrollView>
          </View>
        </SafeAreaView>
      </Modal>

      {/* Sign Out Modal */}
      <Modal
        animationType="fade"
        transparent={true}
        visible={showModal}
        onRequestClose={() => setShowModal(false)}
      >
        <View className="flex-1 justify-center items-center bg-black/50">
          <View
            className={`p-6 rounded-2xl w-[80%] items-center ${
              isDarkMode ? "bg-slate-800" : "bg-white"
            }`}
          >
            <Text
              className={`text-xl font-JakartaBold mb-4 ${
                isDarkMode ? "text-white" : "text-black"
              }`}
            >
              Sign Out
            </Text>
            <Text
              className={`text-center mb-6 ${
                isDarkMode ? "text-gray-300" : "text-gray-600"
              }`}
            >
              Are you sure you want to sign out?
            </Text>
            <View className="flex-row gap-4">
              <TouchableOpacity
                onPress={() => setShowModal(false)}
                className={`py-3 px-6 rounded-full ${
                  isDarkMode ? "bg-slate-700" : "bg-gray-200"
                }`}
              >
                <Text
                  className={`font-JakartaMedium ${
                    isDarkMode ? "text-gray-300" : "text-gray-600"
                  }`}
                >
                  Cancel
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={confirmSignOut}
                className="bg-blue-600 py-3 px-6 rounded-full"
              >
                <Text className="text-white font-JakartaMedium">Sign Out</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
};

export default Home;