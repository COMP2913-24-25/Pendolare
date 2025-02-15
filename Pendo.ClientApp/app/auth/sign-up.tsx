import { useState, useEffect } from "react";
import { Alert, ScrollView, Text, View, TouchableOpacity } from "react-native";
import { ReactNativeModal } from "react-native-modal";

import CustomButton from "@/components/CustomButton";
import InputField from "@/components/InputField";

const Signup = () => {
  const [form, setForm] = useState({
    name: "",
    email: "",
  });

  const [countdown, setCountdown] = useState(0);
  const [verification, setVerification] = useState({
    state: "default",
    error: "",
    code: "",
  });

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (countdown > 0) {
      timer = setInterval(() => setCountdown((prev) => prev - 1), 1000);
    }
    return () => clearInterval(timer);
  }, [countdown]);

  const sendVerificationCode = async () => {
    try {
      setVerification({
        ...verification,
        state: "pending",
      });
      setCountdown(5); // Start 5 second countdown
    } catch (err: any) {
      console.log(JSON.stringify(err, null, 2));
      Alert.alert("Error", "Failed to send verification code");
    }
  };

  const onSignUpPress = async () => {
    if (!form.email || !form.name) {
      Alert.alert("Error", "Please fill in all fields");
      return;
    }
    await sendVerificationCode();
  };

  return (
    <ScrollView className="flex-1 bg-white">
      <ReactNativeModal isVisible={verification.state === "pending"}>
        <View className="bg-white px-7 py-9 rounded-2xl min-h-[300px]">
          <Text className="font-JakartaExtraBold text-2xl mb-2">
            Verification
          </Text>
          <Text className="font-Jakarta mb-5">
            We've sent a verification code to {form.email}.
          </Text>
          <InputField
            label="Code"
            placeholder="123456"
            value={verification.code}
            keyboardType="numeric"
            onChangeText={(code) => setVerification({ ...verification, code })}
          />
          {verification.error && (
            <Text className="text-red-500 text-sm mt-1">
              {verification.error}
            </Text>
          )}
          <CustomButton
            title="Verify Email"
            //   onPress={onPressVerify}
            className="mt-5 bg-success-500"
          />

          <View className="mt-4 items-center">
            {countdown > 0 ? (
              <Text className="text-gray-500">Resend code in {countdown}s</Text>
            ) : (
              <TouchableOpacity onPress={sendVerificationCode}>
                <Text className="text-blue-500 font-JakartaMedium">
                  Resend verification code
                </Text>
              </TouchableOpacity>
            )}
          </View>
        </View>
      </ReactNativeModal>
    </ScrollView>
  );
};

export default Signup;
