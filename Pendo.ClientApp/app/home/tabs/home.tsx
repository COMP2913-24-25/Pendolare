import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import { useState } from "react";
import {
  Text,
  View,
  TouchableOpacity,
  Modal,
  ScrollView,
  Platform,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import Map from "@/components/Map/Map";
import UpcomingRide from "@/components/RideView/UpcomingRide";
import { icons, upcomingRides, pastRides } from "@/constants";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";

const Home = () => {
  const [showModal, setShowModal] = useState(false);
  const [showAllRides, setShowAllRides] = useState(false);
  const [showPastRides, setShowPastRides] = useState(false);
  const { isDarkMode } = useTheme();
  const { logout } = useAuth();

  const nextRide = upcomingRides[0];

  const confirmSignOut = async () => {
    setShowModal(false);
    await logout();
  };

  return (
    <SafeAreaView
      className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
    >
      <ScrollView className="flex-1">
        <View className="px-4">
          {/* Header */}
          <View className="flex-row justify-between items-center mb-2">
            <Text
              className={`text-2xl font-JakartaExtraBold ${isDarkMode ? "text-white" : "text-black"}`}
            >
              Welcome {"John"}👋
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
            {Platform.OS === "web" ? (
              <View className="flex-1 items-center justify-center">
                <Text>Map not available on web</Text>
              </View>
            ) : (
              <Map pickup={null} dropoff={null} />
            )}
          </View>

          {/* Next Journey Section */}
          <View className="mt-5">
            <Text
              className={`text-xl font-JakartaBold mb-3 ${isDarkMode ? "text-white" : "text-black"}`}
            >
              Next Journey
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
          {upcomingRides.length > 1 && (
            <TouchableOpacity
              onPress={() => setShowAllRides(true)}
              className="mt-4 bg-blue-600 py-3 rounded-xl"
            >
              <Text className="text-white text-center font-JakartaBold">
                View All Upcoming Journeys
              </Text>
            </TouchableOpacity>
          )}
        </View>
      </ScrollView>

      {/* All Rides Modal */}
      <Modal
        visible={showAllRides}
        animationType="slide"
        onRequestClose={() => setShowAllRides(false)}
      >
        <SafeAreaView
          className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
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
                {showPastRides ? "Journey History" : "Upcoming Journeys"}
              </Text>
              <View className="w-8" />
            </View>

            <View
              className={`flex-row rounded-xl p-1 ${isDarkMode ? "bg-slate-800" : "bg-gray-100"}`}
            >
              <TouchableOpacity
                className={`flex-1 py-2 rounded-lg ${
                  !showPastRides
                    ? isDarkMode
                      ? "bg-slate-700"
                      : "bg-white shadow"
                    : ""
                }`}
                onPress={() => setShowPastRides(false)}
              >
                <Text
                  className={`text-center font-JakartaMedium ${
                    !showPastRides
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
                  showPastRides
                    ? isDarkMode
                      ? "bg-slate-700"
                      : "bg-white shadow"
                    : ""
                }`}
                onPress={() => setShowPastRides(true)}
              >
                <Text
                  className={`text-center font-JakartaMedium ${
                    showPastRides
                      ? "text-blue-600"
                      : isDarkMode
                        ? "text-gray-400"
                        : "text-gray-500"
                  }`}
                >
                  Past
                </Text>
              </TouchableOpacity>
            </View>

            <ScrollView
              showsVerticalScrollIndicator={false}
              contentContainerStyle={{ paddingTop: 8 }}
            >
              {(showPastRides ? pastRides : upcomingRides).map(
                (ride, index) => (
                  <View key={ride.id} className={index > 0 ? "mt-4" : ""}>
                    <UpcomingRide ride={ride} />
                  </View>
                ),
              )}
              {(showPastRides ? pastRides : upcomingRides).length === 0 && (
                <View className="bg-white rounded-lg p-4 shadow-md">
                  <Text className="text-gray-500">
                    No {showPastRides ? "past" : "upcoming"} journeys
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
