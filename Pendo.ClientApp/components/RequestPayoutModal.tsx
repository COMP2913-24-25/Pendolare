import React, { useEffect, useState } from "react";
import { View, Modal, TouchableOpacity, Alert } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { FontAwesome5 } from "@expo/vector-icons";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText";
import ThemedButton from "@/components/common/ThemedButton";
import ThemedInputField from "./common/ThemedInputField";
import ThemedView from "./common/ThemedView";


interface RequestPayoutModalProps {
  visible: boolean;
  onClose: () => void;
  amount: string;
}

/*
  RequestPayoutModal
  Calls the request payout endpoint and displays options to user
*/
const RequestPayoutModal = ({ visible, onClose, amount }: RequestPayoutModalProps) => {
    
  const { isDarkMode } = useTheme();

  const cardStyle = `${isDarkMode ? "bg-dark" : "bg_white"} rounded-lg shadow-sm px-5 py-3`;

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
    >
    <SafeAreaView
      className={`flex-1 pt-2 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
    >
      <View className="flex-1 px-4">
          {/* Header */}
          <View className="flex-row items-center justify-between mb-6">
            <TouchableOpacity onPress={onClose} className="p-2 -ml-2 mt-4">
              <FontAwesome5
                name={icons.backArrow}
                size={24}
                color={isDarkMode ? "#FFF" : "#000"}
              />
            </TouchableOpacity>
            <Text className="text-2xl font-JakartaBold mt-4">Request Payout</Text>
            <View className="w-10 mt-4" />
          </View>

          {/* Body */}
          <Text className="font-JakartaSemiBold text-lg">By requesting a payout, you can transfer your confirmed balance to your bank account</Text>
            <View className="bg-white rounded-lg p-4 shadow-md" style = {{marginVertical: 20}}>
                <ThemedInputField
                  label="Your current confirmed balance is:"
                  value={"£" + amount}
                  editable={false}
                  containerStyle="mb-4"
                />
            </View>
            <Text className="font-Jakarta text-lg" style={{marginVertical: 10}}>
              You will recieve an email confimation, and your request will be processed by the admin team. This will reset your balance to zero.
            </Text>
            <ThemedButton
              title={`Pay out £${amount}?`}>
              
            </ThemedButton>
        </View>
      </SafeAreaView>
    </Modal>
  );
};

export default RequestPayoutModal;
