import { useUser } from "@clerk/clerk-expo";
import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import { ScrollView, Image } from "react-native";

import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import ThemedView from "@/components/common/ThemedView";
import { Text } from "@/components/common/ThemedText";
import ThemedInputField from "@/components/common/ThemedInputField";
import ThemedButton from "@/components/common/ThemedButton";

const Profile = () => {
  const { user } = useUser();

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
              uri: user?.externalAccounts[0]?.imageUrl || user?.imageUrl,
            }}
            style={{ width: 110, height: 110, borderRadius: 55, borderWidth: 3, borderColor: "#FFF" }}
            className="shadow-sm"
          />
        </ThemedView>

        {/* Profile Information */}
        <ThemedView className="bg-white rounded-lg shadow-sm px-5 py-3">
          <ThemedInputField
            label="First name"
            placeholder={user?.firstName || "Not Found"}
            editable={false}
            containerStyle="mb-4"
          />
          <ThemedInputField
            label="Last name"
            placeholder={user?.lastName || "Not Found"}
            editable={false}
            containerStyle="mb-4"
          />
          <ThemedInputField
            label="Email"
            placeholder={user?.primaryEmailAddress?.emailAddress || "Not Found"}
            editable={false}
          />
        </ThemedView>
      </ScrollView>
    </ThemedSafeAreaView>
  );
};

export default Profile;
