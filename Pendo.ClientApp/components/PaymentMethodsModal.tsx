import React, { useCallback, useEffect, useState } from "react";
import { View, Modal, TouchableOpacity } from "react-native";
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
  To display the saved PaymentMethods to user
*/
const PaymentMethodsModal = ({ visible, onClose }: BlankModalProps) => {

  const { isDarkMode } = useTheme();

  const [methods, setPaymentMethods] = useState<PaymentMethodResponse>({
    Status: "loading", // Change initial status to loading
    Methods: []
  });

  const [hasError, setHasError] = useState(false);

  useFocusEffect(
    useCallback(() => {
      setPaymentMethods({
        Status: "loading",
        Methods: []
      });
      setHasError(false);
      
      PaymentMethods().then((result) => {
        setPaymentMethods(result);
        if (result.Status === "fail") {
          // Handle specific 400 error for no payment methods more gracefully
          if (result.Methods.length === 0) {
            setHasError(true);
            setErrorMessage("No payment methods have been added yet.");
          }
        }
      }).catch(error => {
        // Silently handle the error here without console.error to suppress expo logs
        // We're expecting 400 errors for users without payment methods
        setPaymentMethods({
          Status: "fail",
          Methods: []
        });
        setHasError(true);
      });
    }, [PaymentMethods, setPaymentMethods])
  );

  // Render empty state
  const renderEmptyState = () => {
    return (
      <View className={`flex-1 justify-center items-center p-6 ${isDarkMode ? "bg-slate-800" : "bg-gray-100"} rounded-xl`}>
        <FontAwesome5
          name={icons.card}
          size={48}
          color={isDarkMode ? "#9CA3AF" : "#6B7280"}
          style={{ marginBottom: 20 }}
        />
        <Text className="text-lg font-JakartaBold text-center mb-2">
          No Payment Methods
        </Text>
        <Text className="text-center text-gray-500">
          You haven't added any payment methods to your account yet.
        </Text>
      </View>
    );
  };

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
          {methods.Status === "loading" ? (
            <View className="flex-1 justify-center items-center">
              <Text className="text-lg font-JakartaMedium mb-4">Loading payment methods...</Text>
            </View>
          ) : hasError || methods.Methods.length === 0 ? (
            // Empty or error state
            renderEmptyState()
          ) : (
            // Payment methods list
            <View className={`flex rounded-xl p-1 mb-4`}>
              {methods.Methods?.map((method, index) => (
                <TouchableOpacity
                  key={index}
                  className={`flex-1 py-2 rounded-lg`}
                  style={{
                    borderColor: "#000",
                    borderWidth: 2,
                    minHeight: 100,
                    margin: 5,
                    justifyContent: "center",
                    alignItems: "center",
                    backgroundColor: isDarkMode ? "#fff" : "#fff"
                  }}
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
          )}
        </View>
      </SafeAreaView>
    </Modal>
  );
};

export default PaymentMethodsModal;
