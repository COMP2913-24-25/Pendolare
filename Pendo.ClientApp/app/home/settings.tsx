import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import React from "react";
import { View, Text, TouchableOpacity, Switch } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";

const Settings = () => {
  const { isDarkMode, toggleTheme } = useTheme();

  return (
    <SafeAreaView
      className={isDarkMode ? "flex-1 bg-slate-900" : "flex-1 bg-white"}
    >
      <View className="flex-1 px-5">
        {/* Header Section */}
        <View className="flex-row items-center my-5">
          <TouchableOpacity onPress={() => router.back()} className="mr-4">
            <FontAwesome5
              name={icons.backArrow}
              size={24}
              color={isDarkMode ? "#FFF" : "#000"}
            />
          </TouchableOpacity>
          <Text
            className={`text-2xl font-JakartaBold ${isDarkMode ? "text-white" : "text-black"}`}
          >
            Settings
          </Text>
        </View>

        {/* Settings Options Section */}
        <View
          className={
            isDarkMode ? "bg-slate-700 rounded-xl" : "bg-gray-50 rounded-xl"
          }
        >
          {/* Dark Mode Toggle */}
          <TouchableOpacity className="flex-row justify-between items-center p-4 border-b border-gray-200">
            <View className="flex-row items-center">
              <View className="w-8 h-8 bg-blue-100 rounded-full items-center justify-center mr-3">
                <FontAwesome5 name="moon" size={16} color="#2563EB" />
              </View>
              <Text
                className={`text-lg font-JakartaMedium ${isDarkMode ? "text-white" : "text-black"}`}
              >
                Dark Mode
              </Text>
            </View>
            <Switch
              value={isDarkMode}
              onValueChange={toggleTheme}
              trackColor={{ false: "#767577", true: "#2563EB" }}
              thumbColor="#ffffff"
            />
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
};

export default Settings;
