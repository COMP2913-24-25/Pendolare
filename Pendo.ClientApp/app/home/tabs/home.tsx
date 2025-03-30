import { FontAwesome5 } from "@expo/vector-icons";
import { useFocusEffect } from "expo-router";
import { useState, useEffect, useCallback } from "react";
import {
  View,
  TouchableOpacity,
  Modal,
  ScrollView,
  Alert,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import Map from "@/components/Map/Map";
import { Text } from "@/components/common/ThemedText";
import UpcomingRide from "@/components/RideView/UpcomingRide";
import { icons } from "@/constants";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";
import { getBookings, completeBooking, confirmAtPickup } from "@/services/bookingService";
import RideConfirmationCard from "@/components/RideView/RideConfirmationCard";
import DriverPickupConfirmationCard from "@/components/RideView/DriverPickupConfirmationCard";
import { Ride, convertBookingDetailsToRide, convertRideToBookingDetails } from "@/utils/bookingUtils";
import { getNextCronDates } from "@/utils/cronTools";

/*
  Home
  Home screen for the app
*/
const Home = () => {
  const [showModal, setShowModal] = useState(false);
  const [showAllRides, setShowAllRides] = useState(false);
  const [currentJourneyTab, setCurrentJourneyTab] = useState("Upcoming");
  const { isDarkMode } = useTheme();
  const { logout, userData } = useAuth();

  const [upcomingRides, setUpcomingRides] = useState<Ride[]>([]);
  const [pastRides, setPastRides] = useState<Ride[]>([]);
  const [pendingCompletionRides, setPendingCompletionRides] = useState<Ride[]>([]);
  const [cancelledRides, setCancelledRides] = useState<Ride[]>([]);
  const [nextRide, setNextRide] = useState<Ride | null>(null);
  const [upcomingDriverRide, setUpcomingDriverRide] = useState<Ride | null>(null);

  const fetchBookings = async (driverView: boolean = false) => {
    try {
      console.log(`Fetching bookings with driverView=${driverView}`);
      const response = await getBookings(driverView);
      
      console.log(`Raw bookings response, found ${response.bookings?.length || 0} bookings:`, 
        response.bookings?.length > 0 ? 'Data exists' : 'No data'
      );
      
      if (!response.success || !response.bookings || response.bookings.length === 0) {
        console.log("No bookings found or API request was unsuccessful");
        if (!driverView) {
          setUpcomingRides([]);
          setPastRides([]);
          setPendingCompletionRides([]);
          setCancelledRides([]);
          setNextRide(null);
        } else {
          setUpcomingDriverRide(null);
        }
        return;
      }
      
      if (driverView) {
        const now = Date.now();
        const thirtyMinutes = 30 * 60 * 1000;
        
        const ridesInRange = response.bookings.filter(booking => {
          const status = booking.BookingStatus?.Status;
          if (status !== 'Confirmed') return false;
          
          let rideTime = new Date();
          if (booking.Booking?.RideTime) {
            if (typeof booking.Booking.RideTime === 'string') {
              rideTime = new Date(booking.Booking.RideTime);
            } else if (booking.Booking.RideTime instanceof Date) {
              rideTime = booking.Booking.RideTime;
            }
          }
          
          return rideTime.getTime() >= now - thirtyMinutes &&
                 rideTime.getTime() <= now + thirtyMinutes;
        });
        
        const nextDriverRide = ridesInRange.sort((a, b) => {
          const timeA = new Date(a.Booking.RideTime).getTime();
          const timeB = new Date(b.Booking.RideTime).getTime();
          return Math.abs(timeA - now) - Math.abs(timeB - now);
        })[0];
        
        // Convert BookingDetails to Ride
        setUpcomingDriverRide(nextDriverRide ? convertBookingDetailsToRide(nextDriverRide) : null);
        return;
      }
      
      const bookings = response.bookings || [];
      
      // Convert all BookingDetails to Ride objects
      const rideBookings = bookings.map(booking => convertBookingDetailsToRide(booking));
      
      const cancelled = rideBookings.filter(ride => 
        ride.Status === 'Cancelled'
      );
      
      const upcoming = rideBookings.filter(ride => {
        if (ride.Status === 'Cancelled') return false;

        const bigTime = 5 * 365 * 24 * 60 * 60 * 1000;

        if (ride.EndBookingWindow) {
          const endBookingWindow = ride.EndBookingWindow instanceof Date 
            ? ride.EndBookingWindow 
            : new Date(ride.EndBookingWindow);
        
          if (endBookingWindow.getTime() < new Date("1972-01-15T00:00:00.000Z").getTime()) {
            ride.EndBookingWindow = new Date(Date.now() + bigTime);
          }
        }        

        const dateComp = ride.EndBookingWindow 
          ? new Date(ride.EndBookingWindow ?? Date.now() + bigTime)
          : new Date(Date.now() + bigTime);

        const startDate = ride.RideTime.getTime() < Date.now() ? new Date(Date.now()) : ride.RideTime;

        const commuterPred = (ride.Recurrence && getNextCronDates(ride.Recurrence, startDate, new Date(Date.now() + bigTime), 1)[0]?.getTime() < dateComp.getTime());

        return ride.RideTime.getTime() > Date.now() || commuterPred;

      }).sort((a, b) => a.RideTime.getTime() - b.RideTime.getTime());
      
      const past = rideBookings.filter(ride => {
        if (ride.Status === 'Cancelled') return false;

        return ride.RideTime.getTime() <= Date.now() ;
      });
      
      const pendingCompletion = past.filter(ride => 
        ride.Status === 'PendingCompletion' || 
        ride.Status === 'Confirmed'
      );
      
      const next = upcoming.length > 0 ? upcoming[0] : null;
      
      console.log(`Filtered: ${upcoming.length} upcoming, ${past.length} past, ${cancelled.length} cancelled, ${pendingCompletion.length} pending completion`);
      console.log(`Next ride: ${next ? 'exists' : 'none'}`);
      
      setUpcomingRides(upcoming);
      setPastRides(past);
      setCancelledRides(cancelled);
      setPendingCompletionRides(pendingCompletion);
      setNextRide(next);
    } catch (error) {
      console.error('Error fetching bookings:', error);
    }
  };

  useEffect(() => {
    setCurrentJourneyTab("Upcoming");
  }, []);

  useFocusEffect(
    useCallback(() => {
      fetchBookings(false);
      fetchBookings(true);
    }, [])
  );

  const confirmSignOut = async () => {
    setShowModal(false);
    await logout();
  };

  return (
    <SafeAreaView
      className={`flex-1 pt-2 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
    >
      <ScrollView className="flex-1">
        <View className="px-4">
          <View className="flex-row justify-between items-center mb-2">
            <Text
              className={`text-2xl font-JakartaExtraBold ${isDarkMode ? "text-white" : "text-black"}`}
            >
              Welcome {userData.firstName ?? ""} 👋
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

          {(pendingCompletionRides?.length > 0 && 
            <RideConfirmationCard ride={pendingCompletionRides[0]} onConfirmComplete={async () => {
              await completeBooking(pendingCompletionRides[0].BookingId, true);
              fetchBookings();
            }} onConfirmIncomplete={() => {
              Alert.alert("Ride Incomplete", "Are you sure you want to mark this ride as incomplete?", [
                { text: "Cancel", onPress: () => {} },
                { text: "Confirm", onPress: async () => {
                  await completeBooking(pendingCompletionRides[0].BookingId, false);
                  fetchBookings();
                }}
              ]);
            }} />)}

          <Text
            className={`text-xl font-JakartaBold mt-2 mb-3 ${isDarkMode ? "text-white" : "text-black"}`}
          >
            Your current location
          </Text>
          <View className="h-[200px] border-2 border-gray-300 rounded-lg overflow-hidden mb-2">
            <Map pickup={null} dropoff={null} />
          </View>

          {(upcomingDriverRide != null && 
            <DriverPickupConfirmationCard passenger={upcomingDriverRide.PassengerName} 
              onConfirmArrival={() => {
                confirmAtPickup(upcomingDriverRide.BookingId).then((response) => {
                  if (!response.success) {
                    Alert.alert("Error", "There was an error confirming your arrival at the pickup location.");
                    return;
                  }
                  fetchBookings(true);
                  Alert.alert("Pickup Confirmed", "You have confirmed your arrival at the pickup location.");
                });
              }} />)}

          <View className="mt-2">
            <Text
              className={`text-xl font-JakartaBold my-2 ${isDarkMode ? "text-white" : "text-black"}`}
            >
              Upcoming Journeys
            </Text>
            {nextRide ? (
              <UpcomingRide booking={convertRideToBookingDetails(nextRide)} />
            ) : (
              <View className="bg-white rounded-lg p-4 shadow-md">
                <Text className="text-gray-500">No upcoming journeys</Text>
              </View>
            )}
          </View>

          <TouchableOpacity
            onPress={() => setShowAllRides(true)}
            className="mt-4 mb-20 bg-blue-600 py-3 rounded-xl"
          >
            <Text className="text-white text-center font-JakartaBold">
              View All Upcoming Journeys
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>

      <Modal
        visible={showAllRides}
        presentationStyle="pageSheet"
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
              {(currentJourneyTab === "Cancelled" 
                ? cancelledRides 
                : (currentJourneyTab === "Upcoming" 
                    ? upcomingRides 
                    : pastRides)
              ).map((ride, index) => (
                <View key={ride.BookingId || index} className={index > 0 ? "mt-4" : ""}>
                  <UpcomingRide booking={convertRideToBookingDetails(ride)} />
                </View>
              ))}
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