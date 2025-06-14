import { router } from "expo-router";
import { useState } from "react";
import { Alert, ScrollView, View, Keyboard } from "react-native";

import Button from "@/components/common/ThemedButton";
import InputField from "@/components/common/ThemedInputField";
import { Text } from "@/components/common/ThemedText";
import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import { useTheme } from "@/context/ThemeContext";
import { useAuth } from "@/context/AuthContext";

import { updateUser, getUser } from "@/services/authService";
import { stringLengthValidator } from "@/utils/validators";

/*
  CaptureName
  Screen for capturing first and last name from a new user
*/
const CaptureName = () => {

  if (!useAuth().isLoggedIn) {
    router.replace("/auth/signin");
  }
  
  const [firstName, setFirstName] = useState("");
  const [firstNameValidationMessage, setFirstNameValidationMessage] = useState<string | null>("");

  const [lastName, setLastName] = useState("");
  const [lastNameValidationMessage, setLastNameValidationMessage] = useState<string | null>("");

  const { isDarkMode } = useTheme();

  /*
    Handle Next button press
    Validates input and navigates to the next onboarding step
  */
  const onNextPress = async () => {
    if (!firstName || !lastName) {
      Alert.alert("Error", "Please enter both your first and last name");
      return;
    }

    // Call Identity Server to update name
    let response = await updateUser(firstName, lastName);
    if (!response) {
        Alert.alert("Error", "Failed to update name");
        return;
    }

    getUser().then(() => router.push("/auth/onboarding"));
  };

  return (
    <ThemedSafeAreaView className="flex-1">
      <ScrollView
        className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-white"}`}
        contentContainerStyle={{ padding: 20 }}
      >
        <View className="flex-1">
          {/* Header Section */}
          <View className="relative w-full h-[150px]">
            <Text className="text-2xl font-JakartaSemiBold absolute bottom-5 left-5">
              Welcome! Let&apos;s get to know you.
            </Text>
          </View>

          {/* Input Form Section */}
          <View className="mt-6">
            <InputField
              label="First Name"
              placeholder="Enter your first name"
              textContentType="givenName"
              value={firstName}
              onChangeText={(text) => stringLengthValidator(setFirstName, text, 1, 30, setFirstNameValidationMessage)}
              onSubmitEditing={() => Keyboard.dismiss()}
              labelStyle={isDarkMode ? "text-gray-300" : "text-gray-600"}
              containerStyle={
                isDarkMode
                  ? "bg-slate-700 border-slate-600"
                  : "bg-neutral-100 border-neutral-100"
              }
              inputStyle={isDarkMode ? "text-white" : "text-black"}
            />
            {firstNameValidationMessage !== null && (
            <Text className="mt-1 text-sm text-red-500">
              {firstNameValidationMessage}
            </Text>
            )}
            <InputField
              label="Last Name"
              placeholder="Enter your last name"
              textContentType="familyName"
              value={lastName}
              onChangeText={(text) => stringLengthValidator(setLastName, text, 1, 30, setLastNameValidationMessage)}
              labelStyle={isDarkMode ? "text-gray-300" : "text-gray-600"}
              containerStyle={
                isDarkMode
                  ? "bg-slate-700 border-slate-600"
                  : "bg-neutral-100 border-neutral-100"
              }
              inputStyle={isDarkMode ? "text-white" : "text-black"}
            />
            {lastNameValidationMessage !== null && (
            <Text className="mt-1 text-sm text-red-500">
              {lastNameValidationMessage}
            </Text>
            )}
            <Button
              title="Next"
              onPress={onNextPress}
              className="mt-6"
              disabled={!firstName || !lastName}
            />
          </View>
        </View>
      </ScrollView>
    </ThemedSafeAreaView>
  );
};

export default CaptureName;