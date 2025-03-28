import React, { useCallback, useEffect, useState } from "react";
import { View, Modal, TouchableOpacity, Alert } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { FontAwesome5 } from "@expo/vector-icons";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText";
import { PaymentMethodResponse, PaymentMethods } from "@/services/paymentService";
import { useFocusEffect } from "expo-router";

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

  const [methods, setPaymentMethods] = useState<PaymentMethodResponse>({
    Status: "fail",
    Methods: [{
      Brand: "",
      Funding: "",
      Last4: "",
      Exp_month: 0,
      Exp_year: 0,
      PaymentType: ""
    }]
  });

  useFocusEffect(
    useCallback(() => {
      PaymentMethods().then((result) => {
        setPaymentMethods(result);
      });
    }, [PaymentMethods, setPaymentMethods])
  );

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
          {/* {methods.map((amount) => (
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
        ))} */}

        {methods.Methods?.map((method, index) => (
        <TouchableOpacity
        key={index}
        className={`flex-1 py-2 rounded-lg`}
        style = {{borderColor: "#000", 
                  borderWidth: 2, 
                  minHeight: 100,
                  margin: 5, 
                  justifyContent: "center", 
                  alignItems: "center", 
                  backgroundColor: isDarkMode ? "#fff" : "#fff" }}
        >
          <View style={{ marginVertical: 10 }}>

            <View style={{ flexDirection: "row", alignItems: "center", justifyContent: "space-around" }}>
              <Text className="text-lg font-JakartaBold">
                {method.Brand.toUpperCase()}
              </Text>
              <Text style={{ marginHorizontal: 20 }}>
                {"Exp: " + method.Exp_month + "/" + method.Exp_year}
              </Text>
            </View>
            
            <View style={{ flexDirection: "row", alignItems: "center", justifyContent: "space-around", marginTop: 5 }}>

              <Text className="text-sm font-Jakarta">{"••••" + method.Last4}</Text>
              <Text style={{ marginHorizontal: 20 }}>
                {method.Funding.charAt(0).toUpperCase() + method.Funding.slice(1) + " Card"}
              </Text>
            </View>
          </View>

          </TouchableOpacity>
        ))}
        </View>


        </View>
      </SafeAreaView>
    </Modal>
  );
};

export default PaymentMethodsModal;
