import { useState, useEffect, useRef } from "react";
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
  const debounceRef = useRef<NodeJS.Timeout | null>(null);

  // Debounced category setter
  const handleCategorySelect = (category: string) => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }
    debounceRef.current = setTimeout(() => {
      setSelectedCategory(category);
      setResetFilters(true);
    }, 300); // 300ms debounce
  };

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
            onPress={() => handleCategorySelect("normal")}
            isSelected={selectedCategory === "normal"}
          />

          <BookingCategory
            title="Search Commuter Journeys"
            description="Find reoccuring journeys for your daily commute"
            onPress={() => handleCategorySelect("commuter")}
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
