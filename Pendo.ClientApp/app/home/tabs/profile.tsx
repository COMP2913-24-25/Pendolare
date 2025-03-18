import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import { ScrollView, Image } from "react-native";

import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import ThemedView from "@/components/common/ThemedView";
import { Text } from "@/components/common/ThemedText";
import ThemedInputField from "@/components/common/ThemedInputField";
import ThemedButton from "@/components/common/ThemedButton";

import { USER_FIRST_NAME_KEY, USER_LAST_NAME_KEY, USER_RATING_KEY } from "@/services/authService";
import * as SecureStore from "expo-secure-store";

const Profile = () => {

  const user: { firstName: string; lastName: string; rating: string } = {
    firstName: "",
    lastName: "",
    rating: "N/A",
  };

  async function loadUser(): Promise<void> {
    user.firstName = (await SecureStore.getItemAsync(USER_FIRST_NAME_KEY)) ?? "No first name set!";
    user.lastName = (await SecureStore.getItemAsync(USER_LAST_NAME_KEY)) ?? "No last name set!";
    user.rating = (await SecureStore.getItemAsync(USER_RATING_KEY)) ?? "N/A";
  }

  (async () => {
    await loadUser();
  })();

  return (
    <ThemedSafeAreaView className="flex-1">
      {/* Header */}
      <ThemedView className="flex-row justify-between items-center px-5 my-5">
        <Text className="text-2xl font-JakartaBold">My profile</Text>
        <ThemedButton
          onPress={() => router.push("/home/settings")}
          title=""
          IconLeft={() => (
            <FontAwesome5 name="cog" size={24} color="currentColor" />
          )}
          className="p-2"
        />
      </ThemedView>

      <ScrollView
        contentContainerStyle={{ paddingVertical: 20, paddingBottom: 120 }}
        className="px-5"
      >
        {/* Profile Image */}
        <ThemedView className="items-center my-5">
          <Image
            source={{
              uri: "../assets/images/test-pic.jpg",
            }}
            style={{ width: 110, height: 110, borderRadius: 55, borderWidth: 3, borderColor: "#FFF" }}
            className="shadow-sm"
          />
        </ThemedView>

        {/* Profile Information */}
        <ThemedView className="bg-white rounded-lg shadow-sm px-5 py-3">
          <ThemedInputField
            label="First name"
            placeholder={user.firstName}
            editable={false}
            containerStyle="mb-4"
          />
          <ThemedInputField
            label="Last name"
            placeholder={user.lastName}
            editable={false}
            containerStyle="mb-4"
          />
        </ThemedView>
      </ScrollView>
    </ThemedSafeAreaView>
  );
};

export default Profile;
