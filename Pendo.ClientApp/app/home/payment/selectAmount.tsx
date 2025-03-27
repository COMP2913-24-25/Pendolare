import { View, TouchableOpacity, ScrollView } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import { SafeAreaView } from "react-native-safe-area-context";
import { useState, useEffect } from "react";
import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import { icons } from "@/constants";

/*
  SelectAmount
  Page to allow a user to select the amount they wish to top up on their account
*/
const SelectAmount = () => {
  const { isDarkMode } = useTheme();

  return (
    <SafeAreaView
      className={`flex-1 pt-2 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
    >
      <ScrollView className="flex-1 px-4">
        <View className="flex-row items-center my-5">
          <TouchableOpacity onPress={() => router.back()} className="mr-4">
              <FontAwesome5
                name={icons.backArrow}
                size={24}
                color={isDarkMode ? "#FFF" : "#000"}
              />
            </TouchableOpacity>
            <Text
            className={`text-2xl font-JakartaExtraBold ${
              isDarkMode ? "text-white" : "text-black"
            }`}
          >
            Top Up Balance
          </Text>
        </View>
                
        {/* Tabs */}
        <View
          className={`flex-row rounded-xl p-1 mb-4 ${
            isDarkMode ? "bg-slate-800" : "bg-gray-100"
          }`}
        >
          <TouchableOpacity
            className={`flex-1 py-2 rounded-lg`}
          >
            <Text
              className={`text-center font-JakartaMedium`}
            >
              Bookings
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            className={`flex-1 py-2 rounded-lg `}
          >
            <Text
              className={`text-center font-JakartaMedium`}
            >
              Advertised
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            className={`flex-1 py-2 rounded-lg `}
          >
            <Text
              className={`text-center font-JakartaMedium `}
            >
              Past Journeys
            </Text>
          </TouchableOpacity>
        </View>

        <View className="bg-white rounded-lg p-4 shadow-md">
                <Text className="text-gray-500">No past journeys found</Text>
        </View>


      </ScrollView>
    </SafeAreaView>
  );
};

export default SelectAmount;