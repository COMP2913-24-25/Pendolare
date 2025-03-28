import React, { useEffect, useState } from "react";
import { View, Modal, TouchableOpacity, Alert } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { FontAwesome5 } from "@expo/vector-icons";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText";

interface BlankModalProps {
  visible: boolean;
  onClose: () => void;
}



/*
  PaymentMethodsModal
  To display the PaymentSheet to user
*/
const PaymentMethodsModal = ({ visible, onClose }: BlankModalProps) => {
    
  const { isDarkMode } = useTheme();

  const methods = PaymentMeth

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
            <Text className="text-2xl font-JakartaBold mt-4">Saved Payment Methods</Text>
            <View className="w-10 mt-4" />
          </View>

          {/* Body */}
        <View
          className={`flex rounded-xl p-1 mb-4`}
        >
          {methods.map((amount) => (
          <TouchableOpacity
          key={amount}
          className={`flex-1 py-2 rounded-lg`}
          style = {{borderColor: "#000", 
                    borderWidth: 2, 
                    minHeight: 100,
                    margin: 5, 
                    justifyContent: "center", 
                    alignItems: "center", 
                    backgroundColor: isDarkMode ? "#fff" : "#fff" }}
        >
          <Text
            className={`text-center text-xl font-JakartaSemiBold`}
          >
            {"£" + amount}
          </Text>
        </TouchableOpacity>
        ))}
        </View>


        </View>
      </SafeAreaView>
    </Modal>
  );
};

export default PaymentMethodsModal;
