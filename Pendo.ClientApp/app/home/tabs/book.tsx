import { useState } from "react";
import { ScrollView, View, TouchableOpacity, Modal } from "react-native";
import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import BookingCategory from "@/components/BookingCategory";
import CreateRide from "@/components/CreateRide/CreateRide";
import RideEntry from "@/components/RideView/RideEntry";
import { Text } from "@/components/common/ThemedText";
import { dummyRides } from "@/constants";
import { useTheme } from "@/context/ThemeContext";

const Book = () => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [showRides, setShowRides] = useState(false);
  const [showCreateRideModal, setShowCreateRideModal] = useState(false);
  const { isDarkMode } = useTheme();

  return (
    <ThemedSafeAreaView
      className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
    >
      <ScrollView
        className="px-5"
        contentContainerStyle={{ paddingBottom: 120 }}
      >
        {/* Header Section */}
        <Text
          className={`text-2xl font-JakartaBold my-5 ${isDarkMode ? "text-white" : "text-black"}`}
        >
          Book a Journey
        </Text>

        {/* Booking Categories Section */}
        <View className="mb-5">
          <BookingCategory
            title="Search for Journey"
            description="Find available journeys to your destination"
            onPress={() => {
              setSelectedCategory("normal");
              setShowRides(true);
            }}
            isSelected={selectedCategory === "normal"}
          />

          <BookingCategory
            title="Commuter Journey"
            description="Set up regular journeys for your daily commute"
            onPress={() => {
              setSelectedCategory("commuter");
              setShowRides(false);
            }}
            isSelected={selectedCategory === "commuter"}
          />
        </View>

        {/* Available Journeys or Commuter Section */}
        {showRides ? (
          <View>
            <Text
              className={`text-xl font-JakartaBold mb-4 ${isDarkMode ? "text-white" : "text-black"}`}
            >
              Available Journeys
            </Text>
            {dummyRides.map((ride) => (
              <RideEntry key={ride.id} ride={ride} />
            ))}
          </View>
        ) : (
          selectedCategory === "commuter" && (
            <View
              className={`p-5 rounded-xl ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
            >
              <Text
                className={`text-xl font-JakartaBold mb-4 ${isDarkMode ? "text-white" : "text-black"}`}
              >
                Schedule Commuter Journey
              </Text>
              <View
                className={`p-4 rounded-lg ${isDarkMode ? "bg-slate-700" : "bg-gray-100"}`}
              >
                <Text
                  className={isDarkMode ? "text-gray-200" : "text-gray-600"}
                >
                  Commuter booking form
                </Text>
              </View>
            </View>
          )
        )}

        {/* Create Ride Button */}
        <TouchableOpacity
          className="bg-blue-500 p-4 rounded-lg mt-5"
          onPress={() => setShowCreateRideModal(true)}
        >
          <Text className="text-white text-center">Create a Ride</Text>
        </TouchableOpacity>

        {/* Create Ride Modal */}
        <Modal
          visible={showCreateRideModal}
          animationType="slide"
          onRequestClose={() => setShowCreateRideModal(false)}
        >
          <CreateRide onClose={() => setShowCreateRideModal(false)} />
        </Modal>
      </ScrollView>
    </ThemedSafeAreaView>
  );
};

export default Book;
