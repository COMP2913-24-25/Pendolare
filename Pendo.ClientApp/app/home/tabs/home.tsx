import { router } from "expo-router";
import { useState } from "react";
import { Text, View, TouchableOpacity, Modal, ScrollView, Image } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import Map from "@/components/Map";
import UpcomingRide from "@/components/UpcomingRide";
import { icons, upcomingRides, pastRides } from "@/constants";

const Home = () => {
  const [showModal, setShowModal] = useState(false);
  const [showAllRides, setShowAllRides] = useState(false);
  const [showPastRides, setShowPastRides] = useState(false);
  
  const nextRide = upcomingRides[0]; // Get the next upcoming ride

  const handleSignOut = () => {
    setShowModal(true);
  };

  const confirmSignOut = () => {
    setShowModal(false);
    router.replace("/auth/sign-in");
  };

  return (
    <SafeAreaView className="flex-1 bg-general-500">
      <ScrollView className="flex-1">
        <View className="px-4">
          {/* Header */}
          <View className="flex-row items-center justify-between my-5">
            <Text className="text-2xl font-JakartaExtraBold">
              Welcome {"John"}👋
            </Text>
            <TouchableOpacity
              onPress={handleSignOut}
              className="justify-center items-center w-10 h-10 rounded-full bg-white"
            >
              <Image source={icons.out} className="w-4 h-4" />
            </TouchableOpacity>
          </View>

          {/* Map Section - Reduced height */}
          <Text className="text-xl font-JakartaBold mt-2 mb-3">
            Your current location
          </Text>
          <View className="h-[200px] border-2 border-gray-300 rounded-lg overflow-hidden">
            <Map pickup={null} dropoff={null} />
          </View>

          {/* Next Ride Section */}
          <View className="mt-5">
            <Text className="text-xl font-JakartaBold mb-3">Next Ride</Text>
            {nextRide ? (
              <UpcomingRide ride={nextRide} />
            ) : (
              <View className="bg-white rounded-lg p-4 shadow-md">
                <Text className="text-gray-500">No upcoming rides</Text>
              </View>
            )}
          </View>

          {/* View All Rides Button */}
          {upcomingRides.length > 1 && (
            <TouchableOpacity
              onPress={() => setShowAllRides(true)}
              className="mt-4 bg-blue-600 py-3 rounded-xl"
            >
              <Text className="text-white text-center font-JakartaBold">
                View All Upcoming Rides
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
        <SafeAreaView className="flex-1 bg-general-500">
          <View className="flex-1 px-4">
            <View className="flex-row items-center justify-between my-5">
              <TouchableOpacity 
                onPress={() => setShowAllRides(false)}
                className="p-2"
              >
                <Image source={icons.backArrow} className="w-6 h-6" />
              </TouchableOpacity>
              <Text className="text-2xl font-JakartaBold">
                {showPastRides ? "Ride History" : "Upcoming Rides"}
              </Text>
              <View className="w-8" />
            </View>

            <View className="flex-row bg-gray-100 rounded-xl p-1 mb-4">
              <TouchableOpacity
                className={`flex-1 py-2 rounded-lg ${!showPastRides ? 'bg-white shadow' : ''}`}
                onPress={() => setShowPastRides(false)}
              >
                <Text 
                  className={`text-center font-JakartaMedium ${
                    !showPastRides ? 'text-blue-600' : 'text-gray-500'
                  }`}
                >
                  Upcoming
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                className={`flex-1 py-2 rounded-lg ${showPastRides ? 'bg-white shadow' : ''}`}
                onPress={() => setShowPastRides(true)}
              >
                <Text 
                  className={`text-center font-JakartaMedium ${
                    showPastRides ? 'text-blue-600' : 'text-gray-500'
                  }`}
                >
                  Past
                </Text>
              </TouchableOpacity>
            </View>

            <ScrollView showsVerticalScrollIndicator={false}>
              {(showPastRides ? pastRides : upcomingRides).map((ride) => (
                <UpcomingRide key={ride.id} ride={ride} />
              ))}
              {(showPastRides ? pastRides : upcomingRides).length === 0 && (
                <View className="bg-white rounded-lg p-4 shadow-md">
                  <Text className="text-gray-500">
                    No {showPastRides ? 'past' : 'upcoming'} rides
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
          <View className="bg-white p-6 rounded-2xl w-[80%] items-center">
            <Text className="text-xl font-JakartaBold mb-4">Sign Out</Text>
            <Text className="text-center text-gray-600 mb-6">
              Are you sure you want to sign out?
            </Text>
            <View className="flex-row gap-4">
              <TouchableOpacity
                onPress={() => setShowModal(false)}
                className="bg-gray-200 py-3 px-6 rounded-full"
              >
                <Text className="font-JakartaMedium">Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={confirmSignOut}
                className="bg-general-400 py-3 px-6 rounded-full"
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
