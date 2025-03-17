import { useUser } from "@clerk/clerk-expo";
import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import { Image, ScrollView, View, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import InputField from "@/components/common/ThemedInputField";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";

/*
  Profile
  Profile screen for the app
*/
const Profile = () => {
  const { user } = useUser();
  const { isDarkMode } = useTheme();

  return (
    <SafeAreaView
      className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-white"}`}
    >
      {/* Header Section */}
      <View className="flex-row justify-between items-center px-5 my-5">
        <Text className="text-2xl font-JakartaBold">My profile</Text>
        <TouchableOpacity
          onPress={() => router.push("/home/settings")}
          className="p-2"
        >
          <FontAwesome5
            name="cog"
            size={24}
            color={isDarkMode ? "#FFF" : "#000"}
          />
        </TouchableOpacity>
      </View>

      <ScrollView
        className="px-5"
        contentContainerStyle={{ paddingBottom: 120 }}
      >
        {/* Profile Image Section */}
        <View className="flex items-center justify-center my-5">
          <Image
            source={{
              uri: user?.externalAccounts[0]?.imageUrl ?? user?.imageUrl,
            }}
            style={{ width: 110, height: 110, borderRadius: 110 / 2 }}
            className="rounded-full h-[110px] w-[110px] border-[3px] border-white shadow-sm shadow-neutral-300"
          />
        </View>

        {/* User Information Form Section */}
        <View
          className={`flex flex-col items-start justify-center bg-white rounded-lg shadow-sm shadow-neutral-300 px-5 py-3 ${
            isDarkMode ? "bg-slate-800 shadow-slate-800" : "bg-white"
          }`}
        >
          <View className="flex flex-col items-start justify-start w-full">
            <InputField
              label="First name"
              placeholder={user?.firstName || "Not Found"}
              containerStyle="w-full"
              inputStyle={`p-3.5 ${isDarkMode ? "text-white" : "text-black"}`}
              labelStyle={isDarkMode ? "text-gray-300" : "text-gray-600"}
              editable={false}
            />

            <InputField
              label="Last name"
              placeholder={user?.lastName || "Not Found"}
              containerStyle="w-full"
              inputStyle={`p-3.5 ${isDarkMode ? "text-white" : "text-black"}`}
              labelStyle={isDarkMode ? "text-gray-300" : "text-gray-600"}
              editable={false}
            />

            <InputField
              label="Email"
              placeholder={
                user?.primaryEmailAddress?.emailAddress || "Not Found"
              }
              containerStyle="w-full"
              inputStyle={`p-3.5 ${isDarkMode ? "text-white" : "text-black"}`}
              labelStyle={isDarkMode ? "text-gray-300" : "text-gray-600"}
              editable={false}
            />
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Profile;
