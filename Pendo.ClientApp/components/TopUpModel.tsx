import React, { useEffect, useState } from "react";
import { View, Modal, TouchableOpacity, Alert } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { FontAwesome5 } from "@expo/vector-icons";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText";
import ThemedButton from "@/components/common/ThemedButton";
import { fetchPaymentSheetParams } from "@/services/paymentService";

// stripe requirements
import {presentPaymentSheet, StripeProvider, usePaymentSheet} from "@stripe/stripe-react-native";
const stripe_publishable = process.env.EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY ?? "NA"

interface BlankModalProps {
  visible: boolean;
  onClose: () => void;
}

/*
  StripeModal
  To display the PaymentSheet to user
*/
const StripeModal = ({ visible, onClose }: BlankModalProps) => {
    
    const { isDarkMode } = useTheme();
    const [ready, setReady] = useState(false);
    const {initPaymentSheet, presentPaymentSheet, loading} = usePaymentSheet();

    useEffect(() => {
        initalisePaymentSheet();
    }, [])

    const initalisePaymentSheet = async () => {
        const {PaymentIntent, EphemeralKey, CustomerId} = await fetchPaymentSheetParams();
        
        const {error} = await initPaymentSheet({
            customerId: CustomerId, 
            customerEphemeralKeySecret: EphemeralKey,
            paymentIntentClientSecret: PaymentIntent,
            merchantDisplayName: "Pendolare",
            allowsDelayedPaymentMethods: true
            
        });
        if (error) {
            Alert.alert(`Error: ${error.code}`, error.message);
        }
        else {
            setReady(true)
        }
    }

    async function buy() {
        const {error} = await presentPaymentSheet();

        if (error) {
            Alert.alert(`Error: ${error.code}`, error.message);
        }
        else {
            Alert.alert("GREAT SUCCESS")
            setReady(false)
        }
    }

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
              This is a blank modal. Add your content here!
            </Text>

            {/* Stripe Body */}
            <StripeProvider publishableKey={stripe_publishable}>
                <Text className={`text-base ${isDarkMode ? "text-white" : "text-black"}`}>
                WOW A STRIPY
                </Text>
                <ThemedButton
                    title="Request Payout"
                    style={{ paddingVertical: 25 }}
                    onPress={buy}
                    disabled={loading || !ready}
                />
            </StripeProvider>

          </View>
        </View>
      </SafeAreaView>
    </Modal>
  );
};

export default StripeModal;
