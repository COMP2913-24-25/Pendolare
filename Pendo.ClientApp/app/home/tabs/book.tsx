import { useState } from "react";
import {
  ScrollView,
  Text,
  View,
  TouchableOpacity,
  Image,
  Modal,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import BookingCategory from "@/components/BookingCategory";
import CreateRide from "@/components/CreateRide";
import RideEntry from "@/components/RideEntry";
import { icons, dummyRides } from "@/constants";

const Book = () => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [showRides, setShowRides] = useState(false);
  const [showCreateRideModal, setShowCreateRideModal] = useState(false);

  return (
    <SafeAreaView className="flex-1 bg-general-500">
      <ScrollView
        className="px-5"
        contentContainerStyle={{ paddingBottom: 120 }}
      >
        <Text className="text-2xl font-JakartaBold my-5">Book a Ride</Text>

        <View className="mb-5">
          <BookingCategory
            title="Search for Ride"
            description="Find available rides to your destination"
            onPress={() => {
              setSelectedCategory("search");
              setShowRides(true);
            }}
            isSelected={selectedCategory === "search"}
          />

          <BookingCategory
            title="Commuter Journey"
            description="Set up regular rides for your daily commute"
            onPress={() => {
              setSelectedCategory("commuter");
              setShowRides(false);
            }}
            isSelected={selectedCategory === "commuter"}
          />
        </View>

        {showRides ? (
          <View>
            <Text className="text-xl font-JakartaBold mb-4">
              Available Rides
            </Text>
            {dummyRides.map((ride) => (
              <RideEntry key={ride.id} ride={ride} />
            ))}
          </View>
        ) : (
          selectedCategory === "commuter" && (
            <View className="bg-white p-5 rounded-xl">
              <Text className="text-xl font-JakartaBold mb-4">
                Schedule Commuter Journey
              </Text>
              <View className="bg-gray-100 p-4 rounded-lg">
                <Text className="text-gray-600">
                  Commuter booking form will be implemented here
                </Text>
              </View>
            </View>
          )
        )}

        <TouchableOpacity
          className="bg-blue-500 p-4 rounded-lg mt-5"
          onPress={() => setShowCreateRideModal(true)}
        >
          <Text className="text-white text-center">Create a Ride</Text>
        </TouchableOpacity>

        <Modal
          visible={showCreateRideModal}
          animationType="slide"
          onRequestClose={() => setShowCreateRideModal(false)}
        >
          <CreateRide onClose={() => setShowCreateRideModal(false)} />
        </Modal>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Book;
