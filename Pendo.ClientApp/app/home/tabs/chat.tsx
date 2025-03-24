import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import { useState, useEffect } from "react";
import { ScrollView, View, TouchableOpacity } from "react-native";

import ChatThread from "@/components/ChatThread";
import ContactSupport from "@/components/ContactSupport";
import { Text } from "@/components/common/ThemedText";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import { getUserConversations } from "@/services/messageService";

interface Conversation {
  id: string;
  type: "support" | "driver";
  title: string;
  lastMessage: string;
  timestamp: number;
  unread: number;
}

/*
  Type Guard
  Validate chat type
*/
const isChatType = (type: string): type is "support" | "driver" => {
  return type === "support" || type === "driver";
};

/*
  Chat
  Screen for user chats
*/
const Chat = () => {
  const { isDarkMode } = useTheme();
  const [showSupport, setShowSupport] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);

  /*
    Fetch Conversations
    Fetch user conversations from the server
  */
  const fetchConversations = async () => {
    try {
      const response = await getUserConversations();

      /*
        Normalise Conversations
        Convert API response to a simpler format
      */
      const normalisedConversations = response.conversations.map((conv: any) => ({
        ...conv,
        type: conv.Type ? conv.Type.toLowerCase() : conv.type,
        id: conv.id || conv.ConversationId,
        title: conv.Name,
        lastMessage: conv.lastMessage || "",
        timestamp: new Date(conv.CreateDate).getTime(),
      }));

      console.log("normalised conversations:", normalisedConversations);
      setConversations(normalisedConversations);
    } catch (error) {
      console.error("Failed to fetch conversations:", error);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  /*
    Handle Support Category
    Callback when user selects a support category
  */
  const handleSupportCategory = async (newConversation: any) => {
    console.log("New support chat created:", newConversation);
    await fetchConversations();
    setShowSupport(false);
  };

  /*
    Handle Chat Press
    Navigate to the chat screen when a chat is pressed
  */
  const handleChatPress = (chatId: string) => {
    router.push(`/home/chat/${chatId}`);
  };

  return (
    <ThemedSafeAreaView className={isDarkMode ? "flex-1 bg-slate-900" : "flex-1 bg-white"}>
      <View className="flex-1 px-5">
        {/* Header Section */}
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

        {/* Chat List or Empty State */}
        {conversations.length > 0 ? (
          <ScrollView showsVerticalScrollIndicator={false}>
            {conversations.map((chat) => {
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

        {/* Support Modal */}
        <ContactSupport
          visible={showSupport}
          onClose={() => setShowSupport(false)}
          onSelectCategory={handleSupportCategory}
        />
      </View>
    </ThemedSafeAreaView>
  );
};

export default Chat;
