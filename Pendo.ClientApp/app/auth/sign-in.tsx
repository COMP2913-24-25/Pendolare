import { router } from "expo-router";
import { useState, useEffect } from "react";
import { Alert, ScrollView, View, TouchableOpacity } from "react-native";
import { ReactNativeModal } from "react-native-modal";

import CustomButton from "@/components/CustomButton";
import InputField from "@/components/InputField";
import { Text } from "@/components/ThemedText";
import VerificationCodeInput from "@/components/VerificationCodeInput";
import { useTheme } from "@/context/ThemeContext";

const SignIn = () => {
  const [email, setEmail] = useState("");
  const [countdown, setCountdown] = useState(0);
  const [verification, setVerification] = useState({
    state: "default",
    error: "",
    code: "",
  });

  const { isDarkMode } = useTheme();

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

  const onSignInPress = async () => {
    if (!email) {
      Alert.alert("Error", "Please enter your email");
      return;
    }
    await sendVerificationCode();
  };

  const handleBypass = () => {
    router.replace("/home/tabs/home");
  };

  return (
    <ScrollView
      className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-white"}`}
    >
      <View className="flex-1">
        <View className="relative w-full h-[150px]">
          <Text className="text-2xl font-JakartaSemiBold absolute bottom-5 left-5">
            Welcome Back
          </Text>
        </View>

        <View className="p-5">
          <InputField
            label="Email"
            placeholder="Enter email"
            textContentType="emailAddress"
            value={email}
            onChangeText={setEmail}
            labelStyle={isDarkMode ? "text-gray-300" : "text-gray-600"}
            containerStyle={
              isDarkMode
                ? "bg-slate-700 bsorder-slate-600"
                : "bg-neutral-100 border-neutral-100"
            }
            inputStyle={isDarkMode ? "text-white" : "text-black"}
          />
          <CustomButton
            title="Sign In"
            onPress={onSignInPress}
            className="mt-6"
          />

          <TouchableOpacity
            onPress={handleBypass}
            className={`mt-4 p-3 rounded-full ${
              isDarkMode ? "bg-slate-800" : "bg-gray-200"
            }`}
          >
            <Text
              className={`text-center font-JakartaMedium ${
                isDarkMode ? "text-gray-300" : "text-gray-600"
              }`}
            >
              TESTING: BYPASS
            </Text>
          </TouchableOpacity>
        </View>

        <ReactNativeModal isVisible={verification.state === "pending"}>
          <View
            className={`px-7 py-9 rounded-2xl min-h-[300px] ${
              isDarkMode ? "bg-slate-800" : "bg-white"
            }`}
          >
            <Text className="font-JakartaExtraBold text-2xl mb-2">
              Verification
            </Text>
            <Text className="font-Jakarta mb-5">
              We've sent a verification code to {email}.
            </Text>
            <VerificationCodeInput
              code={verification.code}
              onCodeChange={(code) =>
                setVerification({ ...verification, code })
              }
            />
            {verification.error && (
              <Text className="text-red-500 text-sm mt-1">
                {verification.error}
              </Text>
            )}
            <CustomButton
              title="Verify & Sign In"
              onPress={() => router.replace("/home/tabs/home")}
              className="mt-5 bg-success-500"
            />

            <View className="mt-4 items-center">
              {countdown > 0 ? (
                <Text
                  className={isDarkMode ? "text-gray-400" : "text-gray-500"}
                >
                  Resend code in {countdown}s
                </Text>
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
      </View>
    </ScrollView>
  );
};

export default SignIn;
