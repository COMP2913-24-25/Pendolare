import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import React, { useState } from "react";
import { View, Text, TouchableOpacity, Modal, Platform } from "react-native";

import Map from "../Map/Map";
import RatingStars from "../RatingStars";

import { icons, cancelReasons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { formatTimestamp } from "@/utils/formatTime";

interface UpcomingRideProps {
  ride: {
    id: number;
    driverName: string;
    driverId: number;
    departureTime: number;
    price: string;
    pickup: any;
    dropoff: any;
    status?: string;
    rating?: number; // Add optional rating property
  };
}

const UpcomingRide = ({ ride }: UpcomingRideProps) => {
  const { isDarkMode } = useTheme();
  const [showDetails, setShowDetails] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [showLateCancelWarning, setShowLateCancelWarning] = useState(false);
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [rating, setRating] = useState(0);
  const [showCompletionModal, setShowCompletionModal] = useState(false);

  const isLastMinuteCancellation = () => {
    const now = Date.now();
    const fifteenMinutes = 15 * 60 * 1000;
    return ride.departureTime - now <= fifteenMinutes;
  };

  const isPastRide = () => {
    return Date.now() > ride.departureTime;
  };

  const handleCancelAttempt = () => {
    if (isLastMinuteCancellation()) {
      setShowLateCancelWarning(true);
    } else {
      setShowCancelModal(true);
    }
  };

  const handleCancel = async (reason: string) => {
    try {
      await Promise.resolve(); // Replace with actual API call
      setShowCancelModal(false);
      setShowDetails(false);
    } catch (error) {
      console.error("Error cancelling ride:", error);
    }
  };

  const handleContactDriver = async () => {
    try {
      setShowDetails(false);
      // Small delay to allow modal to start closing
      await new Promise((resolve) => setTimeout(resolve, 100));
      router.push(`/home/chat/${ride.driverId}`);
    } catch (error) {
      console.error("Error navigating to chat:", error);
    }
  };

  const handleDisputeRide = async () => {
    try {
      setShowCompletionModal(false);
      setShowDetails(false);
      // Small delay to allow modals to start closing
      await new Promise((resolve) => setTimeout(resolve, 100));
      router.push("/home/chat/1");
    } catch (error) {
      console.error("Error navigating to support:", error);
    }
  };

  const handleRate = async () => {
    try {
      // Here you would implement the actual rating API call
      await Promise.resolve();
      setShowRatingModal(false);
      setShowDetails(false);
    } catch (error) {
      console.error("Error rating ride:", error);
    }
  };

  const handleCompletionStart = () => {
    setShowCompletionModal(true);
    setShowDetails(false);
  };

  const handleComplete = async () => {
    try {
      if (rating > 0) {
        await Promise.resolve(); // Replace with actual API call
        setShowCompletionModal(false);
      }
    } catch (error) {
      console.error("Error completing ride:", error);
    }
  };

  return (
    <>
      <TouchableOpacity
        className={`bg-white p-4 rounded-lg shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
        onPress={() => setShowDetails(true)}
      >
        <View className="flex-row justify-between items-center mb-2">
          <Text
            className={`text-lg font-JakartaBold ${isDarkMode ? "text-white" : "text-black"}`}
          >
            {ride.dropoff.name}
          </Text>
          <Text className="text-blue-600 font-JakartaBold">{ride.price}</Text>
        </View>
        <View className="flex-row justify-between items-center">
          <Text className={`${isDarkMode ? "text-gray-300" : "text-gray-500"}`}>
            {formatTimestamp(ride.departureTime)}
          </Text>
          <Text className={`${isDarkMode ? "text-gray-300" : "text-gray-500"}`}>
            with {ride.driverName}
          </Text>
        </View>
      </TouchableOpacity>

      <Modal
        visible={showDetails}
        animationType="slide"
        onRequestClose={() => {
          if (!showCancelModal && !showCompletionModal) {
            setShowDetails(false);
          }
        }}
      >
        <View className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-white"}`}>
          <View className="h-1/3">
            <Map pickup={ride.pickup} dropoff={ride.dropoff} />
            <TouchableOpacity
              onPress={() => setShowDetails(false)}
              className={`absolute top-6 left-4 z-10 p-2 rounded-full ${
                isDarkMode ? "bg-slate-800" : "bg-white"
              }`}
            >
              <FontAwesome5
                name={icons.backArrow}
                size={24}
                color={isDarkMode ? "#FFF" : "#000"}
              />
            </TouchableOpacity>
          </View>

          <View className="p-5 flex-1">
            <Text
              className={`text-2xl font-JakartaBold mt-8 mb-4 ${
                isDarkMode ? "text-white" : "text-black"
              }`}
            >
              Ride Details
            </Text>

            <View
              className={`p-4 rounded-xl mb-4 ${
                isDarkMode ? "bg-slate-800" : "bg-gray-50"
              }`}
            >
              <View className="mb-3">
                <Text
                  className={isDarkMode ? "text-gray-300" : "text-gray-500"}
                >
                  From
                </Text>
                <Text
                  className={`font-JakartaMedium ${isDarkMode ? "text-white" : "text-black"}`}
                >
                  {ride.pickup.name}
                </Text>
              </View>
              <View className="mb-3">
                <Text
                  className={isDarkMode ? "text-gray-300" : "text-gray-500"}
                >
                  To
                </Text>
                <Text
                  className={`font-JakartaMedium ${isDarkMode ? "text-white" : "text-black"}`}
                >
                  {ride.dropoff.name}
                </Text>
              </View>
              <View className="mb-3">
                <Text
                  className={isDarkMode ? "text-gray-300" : "text-gray-500"}
                >
                  Departure
                </Text>
                <Text
                  className={`font-JakartaMedium ${isDarkMode ? "text-white" : "text-black"}`}
                >
                  {formatTimestamp(ride.departureTime)}
                </Text>
              </View>
              <View>
                <Text
                  className={isDarkMode ? "text-gray-300" : "text-gray-500"}
                >
                  Price
                </Text>
                <Text
                  className={`font-JakartaMedium ${isDarkMode ? "text-white" : "text-black"}`}
                >
                  {ride.price}
                </Text>
              </View>
            </View>

            <View className="flex-row gap-4 mt-auto">
              <TouchableOpacity
                onPress={handleContactDriver}
                className="flex-1 bg-blue-600 p-4 rounded-xl"
              >
                <Text className="text-white text-center font-JakartaBold">
                  Contact Driver
                </Text>
              </TouchableOpacity>

              {isPastRide() ? (
                <TouchableOpacity
                  onPress={handleCompletionStart}
                  className="flex-1 bg-green-600 p-4 rounded-xl"
                >
                  <Text className="text-white text-center font-JakartaBold">
                    Confirm Completion
                  </Text>
                </TouchableOpacity>
              ) : (
                <TouchableOpacity
                  onPress={handleCancelAttempt}
                  className="flex-1 bg-red-600 p-4 rounded-xl"
                >
                  <Text className="text-white text-center font-JakartaBold">
                    Cancel Ride
                  </Text>
                </TouchableOpacity>
              )}
            </View>
          </View>
        </View>
      </Modal>

      <Modal
        visible={showLateCancelWarning}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setShowLateCancelWarning(false)}
      >
        <View className="flex-1 bg-black/50 justify-center items-center">
          <View className="bg-white p-6 rounded-xl w-[90%] max-w-[400px]">
            <Text className="text-xl font-JakartaBold mb-4">
              Late Cancellation Fee
            </Text>
            <Text className="text-gray-600 mb-6">
              Cancelling within 15 minutes of departure will incur a fee of 75%
              of the ride cost. Do you want to proceed?
            </Text>

            <View className="flex-row justify-end gap-4">
              <TouchableOpacity
                onPress={() => setShowLateCancelWarning(false)}
                className="py-2 px-4"
              >
                <Text className="text-gray-500">Never mind</Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={() => {
                  setShowLateCancelWarning(false);
                  setShowCancelModal(true);
                }}
                className="bg-red-600 py-2 px-4 rounded-lg"
              >
                <Text className="text-white">Yes, Cancel</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

      <Modal
        visible={showCancelModal}
        transparent={true}
        animationType="fade"
        // Prevent closing cancel modal by back button
        onRequestClose={() => null}
      >
        <View className="flex-1 bg-black/50 justify-center items-center">
          <View className="bg-white p-6 rounded-xl w-[90%] max-w-[400px]">
            <Text className="text-xl font-JakartaBold mb-4">Cancel Ride</Text>
            <Text className="text-gray-600 mb-4">
              Please select a reason for cancellation:
            </Text>

            {cancelReasons.map((reason) => (
              <TouchableOpacity
                key={reason}
                className="py-3 border-b border-gray-100"
                onPress={() => handleCancel(reason)}
              >
                <Text className="text-blue-600">{reason}</Text>
              </TouchableOpacity>
            ))}

            <TouchableOpacity
              className="mt-4 py-3"
              onPress={() => setShowCancelModal(false)}
            >
              <Text className="text-gray-500 text-center">Never mind</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      {/* Add Rating Modal */}
      <Modal
        visible={showRatingModal}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setShowRatingModal(false)}
      >
        <View className="flex-1 bg-black/50 justify-center items-center">
          <View className="bg-white p-6 rounded-xl w-[90%] max-w-[400px]">
            <Text className="text-xl font-JakartaBold mb-2 text-center">
              Rate your driver
            </Text>
            <Text className="text-gray-600 mb-4 text-center">
              How was your ride with {ride.driverName}?
            </Text>

            <RatingStars rating={rating} setRating={setRating} />

            <View className="flex-row justify-end gap-4 mt-4">
              <TouchableOpacity
                onPress={() => setShowRatingModal(false)}
                className="py-2 px-4"
              >
                <Text className="text-gray-500">Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={handleRate}
                disabled={rating === 0}
                className={`py-2 px-4 rounded-lg ${
                  rating > 0 ? "bg-blue-600" : "bg-gray-300"
                }`}
              >
                <Text className="text-white">Submit Rating</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

      {/* Completion Modal with Rating and Dispute options */}
      <Modal
        visible={showCompletionModal}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setShowCompletionModal(false)}
      >
        <View className="flex-1 bg-black/50 justify-center items-center">
          <View className="bg-white p-6 rounded-xl w-[90%] max-w-[400px]">
            <Text className="text-xl font-JakartaBold mb-2 text-center">
              How was your ride?
            </Text>

            <View className="mb-8">
              <Text className="text-gray-600 mb-4 text-center">
                Rate your ride with {ride.driverName}
              </Text>
              <RatingStars rating={rating} setRating={setRating} size={10} />
            </View>

            <View className="flex-row justify-between items-center">
              <TouchableOpacity
                onPress={handleDisputeRide}
                className="flex-row items-center"
              >
                <FontAwesome5
                  name={icons.close}
                  size={20}
                  color="#DC2626"
                  style={{ marginRight: 8 }}
                />
                <Text className="text-red-600 font-JakartaMedium">
                  Report an Issue
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                onPress={handleComplete}
                disabled={rating === 0}
                className={`py-2 px-4 rounded-lg ${
                  rating > 0 ? "bg-blue-600" : "bg-gray-300"
                }`}
              >
                <Text className="text-white">Submit</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </>
  );
};

export default UpcomingRide;
