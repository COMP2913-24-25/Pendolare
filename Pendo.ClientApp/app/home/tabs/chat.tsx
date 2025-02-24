import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import { useState } from "react";
import { ScrollView, View, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import ChatThread from "@/components/ChatThread";
import ContactSupport from "@/components/ContactSupport";
import { Text } from "@/components/ThemedText";
import { icons, demoChats } from "@/constants";
import { useTheme } from "@/context/ThemeContext";

// Add type validation helper
const isChatType = (type: string): type is "support" | "driver" => {
  return type === "support" || type === "driver";
};

const Chat = () => {
  const { isDarkMode } = useTheme();
  const [showSupport, setShowSupport] = useState(false);

  const handleSupportCategory = (category: string) => {
    console.log("Creating support chat for category:", category);
    setShowSupport(false);
  };

  const handleChatPress = (chatId: number) => {
    router.push(`/home/chat/${chatId}`);
  };

  return (
    <SafeAreaView
      className={isDarkMode ? "flex-1 bg-slate-900" : "flex-1 bg-white"}
    >
      <View className="flex-1 px-5">
        <View className="flex-row justify-between items-center my-5">
          <Text className="text-2xl font-JakartaBold">Chat</Text>
          <TouchableOpacity
            onPress={() => setShowSupport(true)}
            className="bg-blue-600 px-4 py-2 rounded-lg flex-row items-center"
          >
            <FontAwesome5
              name={icons.support}
              size={16}
              color="#FFF"
              style={{ marginRight: 8 }}
            />
            <Text className="text-white font-JakartaMedium">
              Contact Support
            </Text>
          </TouchableOpacity>
        </View>

        {demoChats.length > 0 ? (
          <ScrollView showsVerticalScrollIndicator={false}>
            {demoChats.map((chat) => {
              // Validate chat type before passing to ChatThread
              if (!isChatType(chat.type)) {
                console.error(`Invalid chat type: ${chat.type}`);
                return null;
              }

              return (
                <ChatThread
                  key={chat.id}
                  type={chat.type}
                  title={chat.title}
                  lastMessage={chat.lastMessage}
                  timestamp={chat.timestamp}
                  unread={chat.unread}
                  onPress={() => handleChatPress(chat.id)}
                />
              );
            })}
          </ScrollView>
        ) : (
          <View className="flex-1 h-fit flex justify-center items-center">
            <Text className="text-3xl font-JakartaBold mt-3">
              No Messages Yet
            </Text>
            <Text className="text-base mt-2 text-center px-7">
              Start a conversation with your drivers and support
            </Text>
          </View>
        )}

        <ContactSupport
          visible={showSupport}
          onClose={() => setShowSupport(false)}
          onSelectCategory={handleSupportCategory}
        />
      </View>
    </SafeAreaView>
  );
};

export default Chat;
