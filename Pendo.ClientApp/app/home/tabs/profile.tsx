import { FontAwesome5 } from "@expo/vector-icons";
import { router, useFocusEffect } from "expo-router";

import { ScrollView, Image, Alert, TouchableOpacity } from "react-native";

import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import ThemedView from "@/components/common/ThemedView";
import { Text } from "@/components/common/ThemedText";
import ThemedInputField from "@/components/common/ThemedInputField";
import ThemedButton from "@/components/common/ThemedButton";

import { useState, useEffect, useCallback } from "react";
import { Rating } from "react-native-ratings";
import { getUser as apiGetUser, updateUser as apiUpdateUser } from "@/services/authService";
import { useTheme } from "@/context/ThemeContext";
import { ViewBalance } from "@/services/paymentService";
import PaymentMethodsModal from "@/components/PaymentMethodsModal"
import RequestPayoutModal from "@/components/RequestPayoutModal"
import { useAuth } from "@/context/AuthContext";
import { stringLengthValidator } from "@/utils/validators";
import { icons } from "@/constants";

const Profile = () => {  
  const { isDarkMode } = useTheme();
  const { userData, updateUserData, refreshUserData } = useAuth();

  const [user, setUser] = useState({ firstName: '', lastName: '', rating: 'N/A' });
  const [firstNameValidationMessage, setFirstNameValidationMessage] = useState<string | null>(null);
  const [lastNameValidationMessage, setLastNameValidationMessage] = useState<string | null>(null);

  const [originalUser, setOriginalUser] = useState({ firstName: '', lastName: '', rating: 'N/A' });
  const [balanceSheet, setBalanceSheet] = useState({ NonPending: 0.00, Pending: 0.00 });
  const [methodsModalVisible, setMethodsModalVisible] = useState(false);
  const [payoutModalVisible, setPayoutModalVisible] = useState(false);

  useEffect(() => {
    // Initialise from AuthContext
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
      const loadData = async () => {
        await refreshUserData();
        try {
          const balance = await ViewBalance();
          setBalanceSheet(balance);
        } catch (error) {
          console.error("Failed to load balance:", error);
        }
      };
      
      loadData();
    }, [])
  );

  const updateUser = (newUser: { firstName: string; lastName: string, rating: string }) => {
    setUser(newUser);
  };

  const cardStyle = `${isDarkMode ? "bg-dark" : "bg_white"} rounded-lg shadow-sm px-5 py-3`;

  return (
    <ThemedSafeAreaView className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}>
      {/* Header */}
      <ThemedView className="flex-row justify-between items-center px-5 pt-5 pb-2">
        <Text className="text-2xl font-JakartaBold">My Profile</Text>

        <TouchableOpacity
          onPress={() => router.push("/home/settings")}
        >
          <FontAwesome5 
            name={icons.cog} 
            size={24} 
            color={isDarkMode ? "#CBD5E1" : "#64748B"}
          />
        </TouchableOpacity>
      </ThemedView>

      <ScrollView
        contentContainerStyle={{ paddingVertical: 20, paddingBottom: 120 }}
        className="px-5"
      >
        {/* Profile Image */}
        <ThemedView className={`items-center my-3 ${cardStyle}`}>
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
        <ThemedView className={`${cardStyle} mb-4`}>
          <ThemedInputField
            label="First name"
            value={user.firstName}
            editable={true}
            containerStyle="mb-4"
            onChangeText={(text) => stringLengthValidator((value) => updateUser({ ...user, firstName: value }), text, 1, 30, setFirstNameValidationMessage)}
          />
          {firstNameValidationMessage !== null && (
          <Text className="mt-1 text-sm text-red-500">
            {firstNameValidationMessage}
          </Text>
          )}
          <ThemedInputField
            label="Last name"
            value={user.lastName}
            editable={true}
            containerStyle="mb-4"
            onChangeText={(text) => stringLengthValidator((value) => updateUser({ ...user, lastName: value }), text, 1, 30, setLastNameValidationMessage)}
          />
          {lastNameValidationMessage !== null && (
          <Text className="mt-1 text-sm text-red-500">
            {lastNameValidationMessage}
          </Text>
          )}
          {(originalUser.firstName != user.firstName || originalUser.lastName != user.lastName) && (
            <ThemedButton
              title="Save Changes"
              disabled={user.firstName.length < 1 || user.lastName.length < 1}
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
        <ThemedView className={`${cardStyle} mb-4`}>
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
