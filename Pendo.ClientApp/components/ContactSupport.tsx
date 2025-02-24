import { FontAwesome5 } from "@expo/vector-icons";
import React, { useState } from "react";
import { View, Text, TouchableOpacity, Modal } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";

const supportCategories = [
  { id: "billing", title: "Billing & Payments", icon: "dollar-sign" },
  { id: "auth", title: "Account & Authentication", icon: "user-shield" },
  { id: "disputes", title: "Disputes & Issues", icon: "exclamation-circle" },
  { id: "general", title: "General Enquiries", icon: "comment-dots" },
];

interface ContactSupportProps {
  visible: boolean;
  onClose: () => void;
  onSelectCategory: (category: string) => void;
}

const ContactSupport = ({
  visible,
  onClose,
  onSelectCategory,
}: ContactSupportProps) => {
  const { isDarkMode } = useTheme();

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
    >
      <SafeAreaView
        className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
      >
        <View className="flex-1 px-5 pt-8 pb-4">
          <View className="flex-row items-center justify-between mb-6">
            <TouchableOpacity onPress={onClose} className="p-2 -ml-2 mt-4">
              <FontAwesome5
                name={icons.backArrow}
                size={24}
                color={isDarkMode ? "#FFF" : "#000"}
              />
            </TouchableOpacity>
            <Text
              className={`text-2xl font-JakartaBold mt-4 ${
                isDarkMode ? "text-white" : "text-black"
              }`}
            >
              Contact Support
            </Text>
            <View className="w-10 mt-4" />
          </View>

          <Text
            className={`text-base mb-6 ${
              isDarkMode ? "text-gray-300" : "text-gray-600"
            }`}
          >
            Please select a category for your enquiry
          </Text>

          {supportCategories.map((category) => (
            <TouchableOpacity
              key={category.id}
              className={`p-4 rounded-xl mb-4 flex-row items-center ${
                isDarkMode ? "bg-slate-800" : "bg-white"
              }`}
              onPress={() => onSelectCategory(category.id)}
            >
              <View
                className={`w-10 h-10 rounded-full items-center justify-center mr-4 ${
                  isDarkMode ? "bg-slate-700" : "bg-blue-50"
                }`}
              >
                <FontAwesome5
                  name={category.icon}
                  size={20}
                  color={isDarkMode ? "#60A5FA" : "#2563EB"}
                />
              </View>
              <Text
                className={`text-lg font-JakartaMedium ${
                  isDarkMode ? "text-white" : "text-black"
                }`}
              >
                {category.title}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </SafeAreaView>
    </Modal>
  );
};

export default ContactSupport;
