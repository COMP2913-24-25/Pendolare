import React, { useState } from "react";
import { View, Text, TouchableOpacity, Image, Modal } from "react-native";

import Map from "@/components/Map";
import { icons } from "@/constants";

interface RideProps {
  driverName: string;
  rating: number;
  price: string;
  departureTime: string;
  destination: string;
  availableSeats: number;
  pickup: any;
  dropoff: any;
}

const RideEntry = ({ ride }: { ride: RideProps }) => {
  const [showDetails, setShowDetails] = useState(false);

  if (!ride) {
    return null; // or some fallback UI
  }

  return (
    <>
      <TouchableOpacity
        className="bg-white p-4 rounded-xl mb-4 shadow-sm"
        onPress={() => setShowDetails(true)}
      >
        <View className="flex-row justify-between items-center mb-2">
          <View className="flex-row items-center">
            <View className="w-10 h-10 bg-gray-200 rounded-full mr-3" />
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
          <Text className="font-JakartaBold text-xl text-blue-600">
            {ride.price}
          </Text>
        </View>

        <View className="flex-row justify-between items-center mt-2">
          <View className="flex-1">
            <View className="flex-row items-center mb-1">
              <Image
                source={icons.target}
                className="w-4 h-4 mr-2"
                style={{ tintColor: "#666666" }}
              />
              <Text className="text-gray-600">{ride.departureTime}</Text>
            </View>
            <View className="flex-row items-center">
              <Image
                source={icons.to}
                className="w-4 h-4 mr-2"
                style={{ tintColor: "#666666" }}
              />
              <Text className="text-gray-600">{ride.destination}</Text>
            </View>
          </View>
          <View className="flex-row items-center">
            <Image
              source={icons.person}
              className="w-4 h-4 mr-1"
              style={{ tintColor: "#666666" }}
            />
            <Text className="text-gray-600 mr-2">
              {ride.availableSeats} seats
            </Text>
          </View>
        </View>
      </TouchableOpacity>

      <Modal
        animationType="slide"
        transparent={true}
        visible={showDetails}
        onRequestClose={() => setShowDetails(false)}
      >
        <View className="flex-1 bg-white">
          <View className="h-1/2">
            <Map pickup={ride.pickup} dropoff={ride.dropoff} />
            <TouchableOpacity
              className="absolute top-12 left-4 bg-white p-2 rounded-full shadow-sm"
              onPress={() => setShowDetails(false)}
            >
              <Image source={icons.close} style={{ width: 24, height: 24 }} />
            </TouchableOpacity>
          </View>

          <View className="p-5">
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
              onPress={() => setShowDetails(false)}
            >
              <Text className="text-white text-center font-JakartaBold text-lg">
                Book Ride
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </>
  );
};

export default RideEntry;
