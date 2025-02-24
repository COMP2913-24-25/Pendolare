import { FontAwesome5 } from "@expo/vector-icons";
import { router, useLocalSearchParams } from "expo-router";
import React, { useState } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { Text } from "@/components/ThemedText";
import { icons, demoChats } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { formatTimestamp } from "@/utils/formatTime";

const ChatDetail = () => {
  const { id } = useLocalSearchParams();
  const [newMessage, setNewMessage] = useState("");
  const { isDarkMode } = useTheme();

  const chat = demoChats.find((c) => c.id === Number(id));

  if (!chat) {
    return null;
  }

  const MessageBubble = ({
    message,
    isUser,
  }: {
    message: { text: string; timestamp: number; sender: string };
    isUser: boolean;
  }) => (
    <View
      className={`flex-row mb-4 ${isUser ? "justify-end" : "justify-start"}`}
    >
      <View
        className={`rounded-2xl px-4 py-3 max-w-[80%] ${
          isUser ? "bg-blue-600" : isDarkMode ? "bg-slate-700" : "bg-gray-100"
        }`}
      >
        <Text className={isUser ? "text-white" : undefined}>
          {message.text}
        </Text>
        <Text
          className={`text-xs mt-1 ${
            isUser
              ? "text-blue-200"
              : isDarkMode
                ? "text-gray-400"
                : "text-gray-500"
          }`}
        >
          {formatTimestamp(message.timestamp)}
        </Text>
      </View>
    </View>
  );

  return (
    <SafeAreaView
      className={isDarkMode ? "flex-1 bg-slate-900" : "flex-1 bg-white"}
    >
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        className="flex-1"
      >
        <View
          className={`flex-row itemse-center p-4 border-b ${isDarkMode ? "border-slate-700" : "border-gray-200"}`}
        >
          <TouchableOpacity onPress={() => router.back()} className="mr-4">
            <FontAwesome5
              name={icons.backArrow}
              size={24}
              color={isDarkMode ? "#FFF" : "#000"}
            />
          </TouchableOpacity>
          <View className="flex-row items-center">
            <View
              className={`w-10 h-10 rounded-full items-center justify-center mr-3 ${
                isDarkMode ? "bg-slate-700" : "bg-gray-100"
              }`}
            >
              <FontAwesome5
                name={chat.type === "support" ? icons.chat : icons.person}
                size={20}
                color="#2563EB"
              />
            </View>
            <Text className="font-JakartaBold text-lg">{chat.title}</Text>
          </View>
        </View>

        <ScrollView
          className="flex-1 px-4"
          contentContainerStyle={{ paddingVertical: 20 }}
        >
          {chat.messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              isUser={message.sender === "user"}
            />
          ))}
        </ScrollView>

        <View className="p-4 border-t border-gray-200 flex-row items-center">
          <TextInput
            className={`flex-1 px-4 py-2 mr-2 rounded-full ${
              isDarkMode ? "bg-slate-700 text-white" : "bg-gray-100 text-black"
            }`}
            placeholder="Type a message..."
            placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
            value={newMessage}
            onChangeText={setNewMessage}
            multiline
          />
          <TouchableOpacity
            className="bg-blue-600 w-10 h-10 rounded-full items-center justify-center"
            disabled={!newMessage.trim()}
            onPress={() => {
              // Handle sending message
              setNewMessage("");
            }}
          >
            <FontAwesome5 name={icons.chat} size={20} color="#FFF" />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default ChatDetail;
