import React, { useEffect, useState } from "react";
import { View, Modal, TouchableOpacity, Alert } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { FontAwesome5 } from "@expo/vector-icons";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText";
import ThemedButton from "@/components/common/ThemedButton";


interface BlankModalProps {
  visible: boolean;
  onClose: () => void;
}

/*
  RequestPayoutModal
  Calls the request payout endpoint and displays options to user
*/
const RequestPayoutModal = ({ visible, onClose }: BlankModalProps) => {
    
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
          {/* Header */}
          <View className="flex-row items-center justify-between mb-6">
            <TouchableOpacity onPress={onClose} className="p-2 -ml-2 mt-4">
              <FontAwesome5
                name={icons.backArrow}
                size={24}
                color={isDarkMode ? "#FFF" : "#000"}
              />
            </TouchableOpacity>
            <Text className="text-2xl font-JakartaBold mt-4">Blank Modal</Text>
            <View className="w-10 mt-4" />
          </View>

          {/* Body */}
          <View className="flex-1 justify-center items-center">
            <Text className={`text-base ${isDarkMode ? "text-white" : "text-black"}`}>
              This is a blank modal.
            </Text>

          </View>
        </View>
      </SafeAreaView>
    </Modal>
  );
};

export default RequestPayoutModal;
