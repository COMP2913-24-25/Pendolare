import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import * as React from "react";
import { View, Text, Modal, TouchableOpacity as RNTouchableOpacity } from "react-native";
import { TouchableOpacity } from "react-native-gesture-handler";

import SafeAreaView from "@/components/common/ThemedSafeAreaView";

import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";

/*
    Settings
    Screen for user settings
*/
const Settings = () => {
  const { isDarkMode, themeMode, setTheme } = useTheme();
  const [dropdownVisible, setDropdownVisible] = React.useState(false);

  const themeOptions = [
    { label: "Light", value: "light" },
    { label: "Dark", value: "dark" },
    { label: "System", value: "system" },
  ];

  const getThemeLabel = () => {
    const option = themeOptions.find(option => option.value === themeMode);
    return option ? option.label : "Light";
  };

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
          {/* Theme Selector */}
          <TouchableOpacity 
            className="flex-row justify-between items-center p-4 border-b border-gray-200"
            onPress={() => setDropdownVisible(true)}
          >
            <View className="flex-row items-center">
              <View className="w-8 h-8 bg-blue-100 rounded-full items-center justify-center mr-3">
                <FontAwesome5 name="moon" size={16} color="#2563EB" />
              </View>
              <Text
                className={`text-lg font-JakartaMedium ${isDarkMode ? "text-white" : "text-black"}`}
              >
                Theme
              </Text>
            </View>
            <View className="flex-row items-center">
              <Text
                className={`mr-2 ${isDarkMode ? "text-white" : "text-gray-600"}`}
              >
                {getThemeLabel()}
              </Text>
              <FontAwesome5
                name="chevron-down"
                size={16}
                color={isDarkMode ? "#FFF" : "#000"}
              />
            </View>
          </TouchableOpacity>
        </View>
      </View>

      {/* Theme Selection Modal */}
      <Modal
        visible={dropdownVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setDropdownVisible(false)}
      >
        <RNTouchableOpacity
          style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.5)' }}
          activeOpacity={1}
          onPress={() => setDropdownVisible(false)}
        >
          <View 
            className={`absolute bottom-0 w-full ${
              isDarkMode ? "bg-slate-800" : "bg-white"
            } rounded-t-xl p-4`}
          >
            <Text 
              className={`text-xl font-JakartaBold mb-4 ${
                isDarkMode ? "text-white" : "text-black"
              }`}
            >
              Select Theme
            </Text>
            {themeOptions.map((option) => (
              <RNTouchableOpacity
                key={option.value}
                className={`py-3 px-4 mb-2 rounded-lg ${
                  themeMode === option.value 
                    ? isDarkMode ? "bg-blue-900" : "bg-blue-100" 
                    : isDarkMode ? "bg-slate-700" : "bg-gray-100"
                }`}
                onPress={() => {
                  setTheme(option.value as any);
                  setDropdownVisible(false);
                }}
              >
                <Text 
                  className={`text-lg ${
                    themeMode === option.value
                      ? "text-blue-500 font-JakartaBold"
                      : isDarkMode ? "text-white" : "text-black"
                  }`}
                >
                  {option.label}
                </Text>
              </RNTouchableOpacity>
            ))}
            <RNTouchableOpacity
              className={`py-3 px-4 mt-2 rounded-lg ${isDarkMode ? "bg-slate-700" : "bg-gray-200"}`}
              onPress={() => setDropdownVisible(false)}
            >
              <Text className={`text-center font-JakartaBold ${isDarkMode ? "text-white" : "text-black"}`}>
                Cancel
              </Text>
            </RNTouchableOpacity>
          </View>
        </RNTouchableOpacity>
      </Modal>
    </SafeAreaView>
  );
};

export default Settings;
