import { FontAwesome5 } from "@expo/vector-icons";
import { router, useFocusEffect } from "expo-router";

import { ScrollView, Image, Alert, TouchableOpacity } from "react-native";

import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import ThemedView from "@/components/common/ThemedView";
import { Text } from "@/components/common/ThemedText";
import ThemedInputField from "@/components/common/ThemedInputField";
import ThemedButton from "@/components/common/ThemedButton";

import { getUserObject, USER_FIRST_NAME_KEY, USER_LAST_NAME_KEY, USER_RATING_KEY, setUserData } from "@/services/authService";
import * as SecureStore from "expo-secure-store";

import { useState, useEffect, useCallback } from "react";
import { Rating } from "react-native-ratings";
import { getUser as apiGetUser, updateUser as apiUpdateUser } from "@/services/authService";
import { useTheme } from "@/context/ThemeContext";
import { ViewBalance } from "@/services/paymentService";
import PaymentMethodsModal from "@/components/PaymentMethodsModal"
import RequestPayoutModal from "@/components/RequestPayoutModal"
import { useAuth } from "@/context/AuthContext";

const Profile = () => {

  //Refresh in the background when the user is on this screen
  apiGetUser();

  const { isDarkMode } = useTheme();
  const { userData, updateUserData, refreshUserData } = useAuth();

  const [user, setUser] = useState({ firstName: '', lastName: '', rating: 'N/A' });
  const [originalUser, setOriginalUser] = useState({ firstName: '', lastName: '', rating: 'N/A' });
  const [balanceSheet, setBalanceSheet] = useState({ NonPending: 0.00, Pending: 0.00 });
  const [methodsModalVisible, setMethodsModalVisible] = useState(false);
  const [payoutModalVisible, setPayoutModalVisible] = useState(false);

  useEffect(() => {
    // Initialize from AuthContext
    setUser({
      firstName: userData.firstName || '',
      lastName: userData.lastName || '',
      rating: userData.rating || 'N/A'
    });
    setOriginalUser({
      firstName: userData.firstName || '',
      lastName: userData.lastName || '',
      rating: userData.rating || 'N/A'
    });
  }, [userData]);

  function setPayoutModalVisibleFunc(state: boolean) {
    setTimeout(() => {
      setPayoutModalVisible(state);
    }, 0);
  }

  useFocusEffect(
    useCallback(() => {
      refreshUserData();
      ViewBalance().then((result) => {
        setBalanceSheet(result);
      });
    }, [refreshUserData])
  );

  const updateUser = (newUser: { firstName: string; lastName: string, rating: string }) => {
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
            onChangeText={(text) => updateUser({ ...user, firstName: text })}
          />
          <ThemedInputField
            label="Last name"
            value={user.lastName}
            editable={true}
            containerStyle="mb-4"
            onChangeText={(text) => updateUser({ ...user, lastName: text })}
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
                await updateUserData(user.firstName, user.lastName);
                setOriginalUser({ ...user });
              }}
            />
          )}
        </ThemedView>

        {/* User's Balance */}
        <ThemedView className={cardStyle} style={{ marginTop: 25 }}>
          <ThemedInputField
            label="Pending Balance"
            value={"£" + balanceSheet.Pending.toFixed(2).toString()}
            editable={false}
            containerStyle="mb-4"
          />
          <Text style={{ fontSize: 14, color: "#888", marginBottom: 4 }}>
            If you have accepted a ride, but it is not yet complete, your expected payout (the price of the journey minus the admin fee) will show here
          </Text>
          <ThemedInputField
            label="Non-Pending Balance"
            value={"£" + balanceSheet.NonPending.toFixed(2).toString()}
            editable={false}
            containerStyle="mb-4"
          />
          <Text style={{ fontSize: 14, color: "#888", marginBottom: 4 }}>
            The value you can use to book journeys. Add to it by becoming a driver or via the button below
          </Text>

          {/* Top Up Selector */}
          <TouchableOpacity
            className={`p-3 mb-4 rounded-xl ${isDarkMode
                ? "bg-slate-800"
                : "bg-white"
              }`}
            style={{ borderColor: "#888", borderWidth: 2, marginVertical: 10 }}
            onPress={() => router.push("/home/payment/selectamount")}
          >
            <Text
              className={`text-lg font-JakartaBold ${isDarkMode
                  ? "text-blue-200"
                  : "text-blue-600"
                }`}
            >
              Top Up Balance
            </Text>
            <Text>Add to your balance via card payment</Text>
          </TouchableOpacity>

          {/* Payment Methods selector */}
          <TouchableOpacity
            className={`p-3 mb-4 rounded-xl ${isDarkMode
                ? "bg-slate-800"
                : "bg-white"
              }`}
            style={{ borderColor: "#888", borderWidth: 2, marginVertical: 10 }}
            onPress={() => setMethodsModalVisible(true)}
          >
            <Text
              className={`text-lg font-JakartaBold ${isDarkMode
                  ? "text-blue-200"
                  : "text-blue-600"
                }`}
            >
              Payment Methods
            </Text>
            <Text>View previously saved Payment Methods</Text>
          </TouchableOpacity>

          {/* Request Payout selector */}
          <TouchableOpacity
            className={`p-3 mb-4 rounded-xl ${isDarkMode
                ? "bg-slate-800"
                : "bg-white"
              }`}
            style={{ borderColor: "#888", borderWidth: 2, marginVertical: 10 }}
            onPress={() => setPayoutModalVisible(true)}
          >
            <Text
              className={`text-lg font-JakartaBold ${isDarkMode
                  ? "text-blue-200"
                  : "text-blue-600"
                }`}
            >
              Request Payout
            </Text>
            <Text>Transfer your non-pending balance to your bank account</Text>
          </TouchableOpacity>

        {/* Modal Imports */}
        </ThemedView>
        <PaymentMethodsModal
          visible={methodsModalVisible}
          onClose={() => setMethodsModalVisible(false)}
        />
        <RequestPayoutModal
          visible={payoutModalVisible}
          onClose={() => setPayoutModalVisibleFunc(false)}
          amount={balanceSheet.NonPending.toFixed(2).toString()}
        />
      </ScrollView>
    </ThemedSafeAreaView>

  );
};

export default Profile;
