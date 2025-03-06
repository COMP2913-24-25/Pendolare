import { router } from "expo-router";
import { useState, useEffect } from "react";
import {
  Alert,
  ScrollView,
  View,
  TouchableOpacity,
  ActivityIndicator,
} from "react-native";
import { ReactNativeModal } from "react-native-modal";

import CustomButton from "@/components/CustomButton";
import InputField from "@/components/InputField";
import { Text } from "@/components/ThemedText";
import VerificationCodeInput from "@/components/VerificationCodeInput";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";
import { requestOTP, verifyOTP } from "@/services/authService";

const SignIn = () => {
  const [email, setEmail] = useState("");
  const [countdown, setCountdown] = useState(0);
  const [loading, setLoading] = useState(false);
  const [verification, setVerification] = useState({
    state: "default",
    error: "",
    code: "",
  });

  const { setIsLoggedIn } = useAuth();
  const { isDarkMode } = useTheme();

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (countdown > 0) {
      timer = setInterval(() => setCountdown((prev) => prev - 1), 1000);
    }
    return () => clearInterval(timer);
  }, [countdown]);

  const sendVerificationCode = async () => {
    if (!email) {
      Alert.alert("Error", "Please enter your email");
      return;
    }

    try {
      setLoading(true);
      const response = await requestOTP(email);

      if (response.success) {
        setVerification({
          ...verification,
          state: "pending",
          error: "",
        });
        setCountdown(60);
      } else {
        Alert.alert(
          "Error",
          response.message || "Failed to send verification code",
        );
      }
    } catch (err: any) {
      console.error(JSON.stringify(err, null, 2));
      Alert.alert(
        "Error",
        "Failed to send verification code. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  const onSignInPress = async () => {
    await sendVerificationCode();
  };

  const handleVerifyOTP = async () => {
    if (verification.code.length !== 6) {
      setVerification({
        ...verification,
        error: "Please enter a valid 6-digit code",
      });
      return;
    }

    try {
      setLoading(true);
      const response = await verifyOTP(email, verification.code);

      if (response.authenticated) {
        setIsLoggedIn(true);
        router.replace("/home/tabs/home");
      } else {
        setVerification({
          ...verification,
          error: response.error || "Invalid verification code",
        });
      }
    } catch (err: any) {
      console.error(JSON.stringify(err, null, 2));
      setVerification({
        ...verification,
        error: "Verification failed. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleBypass = () => {
    router.replace("/home/tabs/home");
  };

  return (
    <ScrollView
      className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-white"}`}
    >
      <View className="flex-1">
        {/* Welcome Header Section */}
        <View className="relative w-full h-[150px]">
          <Text className="text-2xl font-JakartaSemiBold absolute bottom-5 left-5">
            Welcome Back
          </Text>
        </View>

        {/* Login Form Section */}
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
                ? "bg-slate-700 border-slate-600"
                : "bg-neutral-100 border-neutral-100"
            }
            inputStyle={isDarkMode ? "text-white" : "text-black"}
          />
          <CustomButton
            title={loading ? "Please wait..." : "Sign In"}
            onPress={onSignInPress}
            disabled={loading}
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

          {/* Sign Up Link */}
          <View className="mt-6 flex-row justify-center">
            <Text className="font-Jakarta">Don't have an account? </Text>
            <TouchableOpacity onPress={() => router.replace("/auth/sign-up")}>
              <Text className="text-blue-500 font-JakartaMedium">Sign Up</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* OTP Verification Modal */}
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
                setVerification({ ...verification, code, error: "" })
              }
            />
            {verification.error && (
              <Text className="text-red-500 text-sm mt-1">
                {verification.error}
              </Text>
            )}
            <CustomButton
              title={loading ? "Verifying..." : "Verify & Sign In"}
              onPress={handleVerifyOTP}
              disabled={loading}
              className="mt-5 bg-success-500"
            />

            {/* Resend Code Section */}
            <View className="mt-4 items-center">
              {loading ? (
                <ActivityIndicator color={isDarkMode ? "#fff" : "#000"} />
              ) : countdown > 0 ? (
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
