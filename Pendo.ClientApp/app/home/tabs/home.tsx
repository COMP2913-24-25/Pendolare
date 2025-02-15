import { Text, View, TouchableOpacity, Modal } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { router } from "expo-router";
import { useState } from "react";

import Map from "@/components/Map";

const Home = () => {
  const [showModal, setShowModal] = useState(false);

  const handleSignOut = () => {
    setShowModal(true);
  };

  const confirmSignOut = () => {
    setShowModal(false);
    router.replace("/auth/sign-up");
  };

  return (
    <SafeAreaView className="bg-general-500 flex-1">
      <View className="flex flex-row items-center justify-between my-5 px-4">
        <Text className="text-2xl font-JakartaExtraBold">
          Welcome {"John"}👋
        </Text>
        <TouchableOpacity
          onPress={handleSignOut}
          className="justify-center items-center w-10 h-10 rounded-full bg-white"
        >
          {/* <Image source={icons.out} className="w-4 h-4" /> */}
        </TouchableOpacity>
      </View>

      <View className="px-4">
        <Text className="text-xl font-JakartaBold mt-5 mb-3">
          Your current location
        </Text>
        <View className="flex flex-row items-center bg-transparent h-[300px] border-2 border-gray-300 rounded-lg p-2">
          <Map />
        </View>
      </View>

      <View className="px-4 mt-5">
        <Text className="text-xl font-JakartaBold mb-3">Recent Rides</Text>
        <View className="bg-white rounded-lg p-4 shadow-md">
          <Text className="text-gray-500">No recent rides available</Text>
        </View>
      </View>

      <Modal
        animationType="fade"
        transparent={true}
        visible={showModal}
        onRequestClose={() => setShowModal(false)}
      >
        <View className="flex-1 justify-center items-center bg-black/50">
          <View className="bg-white p-6 rounded-2xl w-[80%] items-center">
            <Text className="text-xl font-JakartaBold mb-4">Sign Out</Text>
            <Text className="text-center text-gray-600 mb-6">
              Are you sure you want to sign out?
            </Text>
            <View className="flex-row gap-4">
              <TouchableOpacity
                onPress={() => setShowModal(false)}
                className="bg-gray-200 py-3 px-6 rounded-full"
              >
                <Text className="font-JakartaMedium">Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={confirmSignOut}
                className="bg-general-400 py-3 px-6 rounded-full"
              >
                <Text className="text-white font-JakartaMedium">Sign Out</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
};

export default Home;
