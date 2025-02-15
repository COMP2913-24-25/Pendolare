import React from "react";
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  Modal,
  ScrollView,
} from "react-native";

import Map from "./Map";

import { icons } from "@/constants";

const RideDetails = ({ ride, visible, onClose }) => {
  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={onClose}
    >
      <View className="flex-1 bg-white">
        <View className="h-1/2">
          <Map pickup={ride.pickup} dropoff={ride.dropoff} />
          <TouchableOpacity
            className="absolute top-12 left-4 bg-white p-2 rounded-full shadow-sm"
            onPress={onClose}
          >
            <Image source={icons.close} style={{ width: 24, height: 24 }} />
          </TouchableOpacity>
        </View>

        <ScrollView className="p-5">
          <View className="flex-row items-center justify-between mb-4">
            <View className="flex-row items-center">
              <View className="w-12 h-12 bg-gray-200 rounded-full mr-3" />
              <View>
                <Text className="font-JakartaBold text-lg">
                  {ride.driverName}
                </Text>
                <View className="flex-row items-center">
                  <Image
                    source={icons.star}
                    className="w-4 h-4 mr-1"
                    style={{ tintColor: "#FFC107" }}
                  />
                  <Text className="text-gray-500">{ride.rating}</Text>
                </View>
              </View>
            </View>
            <Text className="font-JakartaBold text-2xl text-blue-600">
              {ride.price}
            </Text>
          </View>

          <View className="bg-gray-50 p-4 rounded-xl mb-4">
            <View className="flex-row items-center mb-3">
              <Image
                source={icons.target}
                className="w-5 h-5 mr-2"
                style={{ tintColor: "#666666" }}
              />
              <Text className="text-gray-600">{ride.departureTime}</Text>
            </View>

            <View className="flex-row items-center mb-3">
              <Image
                source={icons.to}
                className="w-5 h-5 mr-2"
                style={{ tintColor: "#2563EB" }}
              />
              <Text className="text-gray-600">{ride.pickup.name}</Text>
            </View>

            <View className="flex-row items-center">
              <Image
                source={icons.target}
                className="w-5 h-5 mr-2"
                style={{ tintColor: "#DC2626" }}
              />
              <Text className="text-gray-600">{ride.dropoff.name}</Text>
            </View>
          </View>

          <View className="bg-gray-50 p-4 rounded-xl mb-6">
            <View className="flex-row items-center">
              <Image
                source={icons.person}
                className="w-5 h-5 mr-2"
                style={{ tintColor: "#666666" }}
              />
              <Text className="text-gray-600">
                {ride.availableSeats} seats available
              </Text>
            </View>
          </View>

          <TouchableOpacity
            className="bg-blue-600 p-4 rounded-xl"
            onPress={() => {
              // Handle booking
              onClose();
            }}
          >
            <Text className="text-white text-center font-JakartaBold text-lg">
              Book Ride
            </Text>
          </TouchableOpacity>
        </ScrollView>
      </View>
    </Modal>
  );
};

export default RideDetails;
