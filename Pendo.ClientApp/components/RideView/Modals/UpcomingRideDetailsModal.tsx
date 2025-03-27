import React from "react";
import { FontAwesome5 } from "@expo/vector-icons";
import { View, TouchableOpacity, Modal } from "react-native";

import Map from "../../Map/Map";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText";
import { Ride } from "@/constants";
import StatusBadge from "../StatusBadge";

interface UpcomingRideDetailsModalProps {
  ride: Ride;
  visible: boolean;
  onClose: () => void;
  onContactDriver: () => void;
  onCancel: () => void;
  onComplete: () => void;
  isPastRide: boolean;
  children?: React.ReactNode;
}

/*
    UpcomingRideDetailsModal
    Modal component for viewing upcoming ride details.
*/
const UpcomingRideDetailsModal = ({
  ride,
  visible,
  onClose,
  onContactDriver,
  onCancel,
  onComplete,
  isPastRide,
  children,
}: UpcomingRideDetailsModalProps) => {
  const { isDarkMode } = useTheme();

  return (
    <Modal visible={visible} animationType="slide" onRequestClose={onClose}>
      <View className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-white"}`}>
        <View className="h-1/3">
          <Map pickup={ride.Pickup} dropoff={ride.Dropoff} />
          <TouchableOpacity
            onPress={onClose}
            className={`absolute top-12 left-4 z-10 p-2 rounded-full ${
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
          <Text className="text-2xl font-JakartaBold mt-4 mb-4">Ride Details</Text>

          <View
            className={`p-4 rounded-xl mb-4 ${
              isDarkMode ? "bg-slate-800" : "bg-gray-50"
            }`}
          >
            <StatusBadge statusText={ride.Status} />
            <View className="mb-3 mt-3">
              <Text>From</Text>
              <Text className="font-JakartaMedium">{ride.Pickup.name}</Text>
            </View>
            <View className="mb-3">
              <Text>To</Text>
              <Text className="font-JakartaMedium">{ride.Dropoff.name}</Text>
            </View>
            <View className="mb-3">
              <Text>Departure</Text>
              <Text className="font-JakartaMedium">{ride.RideTime.toUTCString()}</Text>
            </View>
            <View>
              <Text>Price</Text>
              <Text className="font-JakartaMedium">{`£${ride.Price.toFixed(2)}`}</Text>
            </View>
          </View>

          <View className="flex-row gap-4">
            <TouchableOpacity
              onPress={onContactDriver}
              className="flex-1 bg-blue-600 p-4 rounded-xl"
            >
              <Text className="text-white text-center font-JakartaBold">
                Contact Driver
              </Text>
            </TouchableOpacity>

            {isPastRide ? (
              <TouchableOpacity
                onPress={onComplete}
                className="flex-1 bg-green-600 p-4 rounded-xl"
              >
                <Text className="text-white text-center font-JakartaBold">
                  Confirm Completion
                </Text>
              </TouchableOpacity>
            ) : (
              <TouchableOpacity
                onPress={onCancel}
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
      {children}
    </Modal>
  );
};

export default UpcomingRideDetailsModal;