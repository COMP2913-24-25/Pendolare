import { useState, useEffect } from "react";
import { ScrollView, View, TouchableOpacity, Modal } from "react-native";
import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import BookingCategory from "@/components/BookingCategory";
import CreateRide from "@/components/CreateRide/CreateRide";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import FilteredRides from "@/components/RideView/FilteredRides";

/*
  Book
  Screen for booking journeys
*/
const Book = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>("normal");
  const [showCreateRideModal, setShowCreateRideModal] = useState(false);
  const [resetFilters, setResetFilters] = useState(false);
  const { isDarkMode } = useTheme();

  return (
    <ThemedSafeAreaView
      className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
    >
      <ScrollView
        className="px-5"
        contentContainerStyle={{ paddingBottom: 120 }}
      >
          {/* Create Ride Button */}
          <Text className={`text-2xl font-JakartaBold my-5 ${isDarkMode ? "text-white" : "text-black"}`}>Advertise your Journey</Text>
          <TouchableOpacity
            className="bg-blue-500 p-4 rounded-lg mb-5"
            onPress={() => setShowCreateRideModal(true)}
          >

          <Text className="text-md font-JakartaSemiBold text-white text-center">Create a Ride</Text>
          </TouchableOpacity>

        {/* Header Section */}
        <Text
          className={`text-2xl font-JakartaBold my-2 ${isDarkMode ? "text-white" : "text-black"}`}
        >
          Book a Journey
        </Text>

        {/* Booking Categories Section */}
        <View className="mb-1">
          <BookingCategory
            title="Search Regular Journeys"
            description="Find available journeys to your destination"
            onPress={() => {
              setSelectedCategory("normal");
              setResetFilters(true);
            }}
            isSelected={selectedCategory === "normal"}
          />

          <BookingCategory
            title="Search Commuter Journeys"
            description="Find reoccuring journeys for your daily commute"
            onPress={() => {
              setSelectedCategory("commuter");
              setResetFilters(true);
            }}
            isSelected={selectedCategory === "commuter"}
          />
        </View>

        {/* Available Journeys or Commuter Section */}
        <FilteredRides resetFilters={resetFilters} setResetFilters={setResetFilters} isDarkMode={isDarkMode} journeyType={selectedCategory === "commuter" ? 2 : 1} />

        {/* Create Ride Modal */}
        <Modal
          visible={showCreateRideModal}
          animationType="slide"
          presentationStyle="pageSheet"
          onRequestClose={() => setShowCreateRideModal(false)}
        >
          <CreateRide onClose={() => setShowCreateRideModal(false)} />
        </Modal>
      </ScrollView>
    </ThemedSafeAreaView>
  );
};

export default Book;
