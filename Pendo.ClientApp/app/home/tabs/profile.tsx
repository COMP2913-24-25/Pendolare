import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import { ScrollView, Image, Alert } from "react-native";

import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import ThemedView from "@/components/common/ThemedView";
import { Text } from "@/components/common/ThemedText";
import ThemedInputField from "@/components/common/ThemedInputField";
import ThemedButton from "@/components/common/ThemedButton";

import { USER_FIRST_NAME_KEY, USER_LAST_NAME_KEY, USER_RATING_KEY } from "@/services/authService";
import * as SecureStore from "expo-secure-store";

import { useState } from "react";
import { Rating } from "react-native-ratings";
import { getUser as apiGetUser, updateUser as apiUpdateUser } from "@/services/authService";
import { useTheme } from "@/context/ThemeContext";
import { ViewBalance } from "@/services/paymentService";

const Profile = () => {

  //Refresh in the background when we load in
  apiGetUser();
  ViewBalance();

  const { isDarkMode } = useTheme();

  const getUser = () => {
      return {
      firstName: SecureStore.getItem(USER_FIRST_NAME_KEY) ?? "No first name set!",
      lastName: SecureStore.getItem(USER_LAST_NAME_KEY) ?? "No last name set!",
      rating: SecureStore.getItem(USER_RATING_KEY) ?? "N/A"
    };
  };

  const getBalanceSheet = () => {
    return {
      Pending: SecureStore.getItem(USER_PENDING_BALANCE) ?? -99,
      Non-Pending: SecureStore.getItem(USER_NON_PENDING_BALANCE) ?? -99
    };
  };

  const originalUser = getUser();

  const [user, setUser] = useState(getUser());

  const updateUser = (newUser : { firstName: string; lastName: string, rating: string}) => {
    if (newUser.firstName.length > 30 || newUser.lastName.length > 30) {
      return;
    }
    setUser(newUser);
  };

  const cardStyle = `${isDarkMode ? "bg-dark" : "bg_white"} rounded-lg shadow-sm px-5 py-3`;

  

  return (
    <ThemedSafeAreaView className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}>
      {/* Header */}
      <ThemedView className="flex-row justify-between items-center px-5 my-5">
        <Text className="text-2xl font-JakartaBold my-5">My Profile</Text>
        <ThemedButton
          onPress={() => router.push("/home/settings")}
          title=""
          IconLeft={() => (
            <FontAwesome5 name="cog" size={24} color="currentColor" />
          )}
          className="w-16 h-16 ml-6 rounded-l-full"
        />
      </ThemedView>

      <ScrollView
        contentContainerStyle={{ paddingVertical: 20, paddingBottom: 120 }}
        className="px-5"
      >
        {/* Profile Image */}
        <ThemedView className={`items-center my-5 ${cardStyle}`}>
          <Image
            source={{
              uri: "../../assets/images/test-pic.jpg",
            }}
            style={{ width: 110, height: 110, borderRadius: 55, borderWidth: 3, borderColor: "#FFF" }}
            className="shadow-sm"
          />
          <ThemedView className="items-center mt-3">
            {user.rating === "N/A" ? (
              <Text className="text-lg font-Jakarta">No driver rating yet!</Text>
            ) : (
              <Rating startingValue={Number.parseInt(user.rating)} readonly />
            )}
            <Text className="text-xl font-JakartaBold">
              {user.firstName} {user.lastName}
            </Text>
          </ThemedView>
        </ThemedView>

        {/* Profile Information */}
        <ThemedView className={cardStyle}>
          <ThemedInputField
            label="First name"
            value={user.firstName}
            editable={true}
            containerStyle="mb-4"
            onChangeText={(text) => updateUser({...user, firstName: text})}
          />
          <ThemedInputField
            label="Last name"
            value={user.lastName}
            editable={true}
            containerStyle="mb-4"
            onChangeText={(text) => updateUser({...user, lastName: text})}
          />
          {(originalUser.firstName != user.firstName || originalUser.lastName != user.lastName) && (
            <ThemedButton
              title="Save Changes"
              onPress={async () => {
                let result = await apiUpdateUser(user.firstName, user.lastName);
                if (!result) {
                  Alert.alert("Failed to update user. Please try again.");
                  console.error("Failed to update user. Please try again.");
                  return;
                }
                SecureStore.setItem(USER_FIRST_NAME_KEY, user.firstName);
                SecureStore.setItem(USER_LAST_NAME_KEY, user.lastName);
              }}
            />
          )}
        </ThemedView>

        {/* User's Balance */}
        <ThemedView className={cardStyle} style={{ marginTop: 25 }}>
          <ThemedInputField
            label="Pending Balance"
            value="£69.42"
            editable={false}
            containerStyle="mb-4"
            // onChangeText={(text) => updateUser({...user, firstName: text})}
          />
          <Text style={{ fontSize: 14, color: "#888", marginBottom: 4 }}>
            If you have accepted a ride, but it is not yet complete, your expected payout (the price of the journey minus the admin fee) will show here
          </Text>
          <ThemedInputField
            label="Non-Pending Balance"
            value="£99.69"
            editable={false}
            containerStyle="mb-4"
            // onChangeText={(text) => updateUser({...user, lastName: text})}
          />
          <Text style={{ fontSize: 14, color: "#888", marginBottom: 4 }}>
            The value you can use to book journeys. Add to it by becoming a driver or via the button below
          </Text>
        </ThemedView>
        <ThemedButton
            title="Top Up Balance"
            style={{ marginVertical: 25 }}
          />
          <ThemedButton
            title="Request Payout"
            style={{ paddingVertical: 25 }}
          />

      </ScrollView>
    </ThemedSafeAreaView>
  );
};

export default Profile;
