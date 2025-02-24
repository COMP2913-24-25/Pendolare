import { FontAwesome5 } from "@expo/vector-icons";
import React, { useState } from "react";
import { View, TouchableOpacity } from "react-native";

import RideDetails from "@/components/RideView/RideDetails";
import { Text } from "@/components/ThemedText";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";

interface RideEntryProps {
  ride: any;
}

const RideEntry = ({ ride }: RideEntryProps) => {
  const [showDetails, setShowDetails] = useState(false);
  const { isDarkMode } = useTheme();

  return (
    <>
      <TouchableOpacity
        className={`p-4 rounded-xl mb-4 shadow-sm ${
          isDarkMode ? "bg-slate-800" : "bg-white"
        }`}
        onPress={() => setShowDetails(true)}
      >
        <View className="flex-row justify-between items-center mb-3">
          <View className="flex-row items-center">
            <View
              className={`w-10 h-10 rounded-full items-center justify-center mr-2 ${
                isDarkMode ? "bg-slate-700" : "bg-gray-100"
              }`}
            >
              <FontAwesome5
                name={icons.person}
                size={20}
                color={isDarkMode ? "#FFF" : "#666666"}
              />
            </View>
            <View>
              <Text className="font-JakartaBold">{ride.driverName}</Text>
              <View className="flex-row items-center">
                <FontAwesome5
                  name={icons.star}
                  size={12}
                  color="#FFC107"
                  style={{ marginRight: 4 }}
                />
                <Text className="text-gray-500 text-sm">{ride.rating}</Text>
              </View>
            </View>
          </View>
          <Text className="font-JakartaBold text-blue-600">{ride.price}</Text>
        </View>

        <View>
          <View className="flex-row items-center mb-2">
            <FontAwesome5
              name={icons.time}
              size={16}
              color={isDarkMode ? "#FFF" : "#666666"}
              style={{ marginRight: 8 }}
            />
            <Text className={isDarkMode ? "text-gray-200" : "text-gray-600"}>
              {ride.departureTime}
            </Text>
          </View>
          <View className="flex-row items-center mb-2">
            <FontAwesome5
              name={icons.to}
              size={16}
              color="#2563EB"
              style={{ marginRight: 8 }}
            />
            <Text className={isDarkMode ? "text-gray-200" : "text-gray-600"}>
              {ride.pickup.name}
            </Text>
          </View>
          <View className="flex-row items-center">
            <FontAwesome5
              name={icons.target}
              size={16}
              color="#DC2626"
              style={{ marginRight: 8 }}
            />
            <Text className={isDarkMode ? "text-gray-200" : "text-gray-600"}>
              {ride.dropoff.name}
            </Text>
          </View>
        </View>
      </TouchableOpacity>

      <RideDetails
        ride={ride}
        visible={showDetails}
        onClose={() => setShowDetails(false)}
      />
    </>
  );
};

export default RideEntry;
