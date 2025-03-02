import { FontAwesome5 } from "@expo/vector-icons";
import { router, useLocalSearchParams } from "expo-router";
import React, { useState, useEffect, useRef } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { Text } from "@/components/ThemedText";
import { icons, demoChats } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { messageService, ChatMessage } from "@/services/messageService";
import { formatTimestamp } from "@/utils/formatTime";

// Helper function to generate unique IDs
const generateUniqueId = () => {
  return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

const ChatDetail = () => {
  const { id } = useLocalSearchParams();
  const [newMessage, setNewMessage] = useState("");
  const { isDarkMode } = useTheme();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(true);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const scrollViewRef = useRef<ScrollView>(null);

  const chat = demoChats.find((c: { id: number; }) => c.id === Number(id));

  useEffect(() => {
    // Initialize with existing messages from demo data
    if (chat) {
      const formattedMessages = chat.messages.map((msg: { id: number; sender: string; text: string; timestamp: number; }) => {
        return ({
          id: `demo-${msg.id}`, // Ensure unique ID by adding prefix
          type: "chat",
          from: msg.sender === "user" ? "12345" : "other",
          content: msg.text,
          timestamp: new Date(msg.timestamp).toISOString(),
          sender: msg.sender
        });
      });
      
      setMessages(formattedMessages);
    }

    // Set up WebSocket event listeners
    messageService.on("connected", () => {
      setIsConnected(true);
      setIsConnecting(false);
      setConnectionError(null);
    });

    messageService.on("disconnected", (reason) => {
      setIsConnected(false);
      if (reason) {
        setConnectionError(`Disconnected: ${reason}`);
      }
    });

    messageService.on("error", (error) => {
      setConnectionError(`Connection error: ${error}`);
      setIsConnecting(false);
    });

    messageService.on("message", (message) => {
      // If echo message detected, update status of the last "sending" message
      if ((message as any).isEcho) {
        setMessages((prevMessages: any) => {
          const index = prevMessages.findIndex((msg: ChatMessage) => msg.status === "sending");
          if (index !== -1) {
            const updatedMsg = { ...prevMessages[index], status: "sent" };
            return [...prevMessages.slice(0, index), updatedMsg, ...prevMessages.slice(index + 1)];
          }
          return prevMessages;
        });
      } 
      else if (message.type === "welcome" && message.content) {
        setMessages((prevMessages: any) => [
          ...prevMessages,
          { ...message, id: generateUniqueId(), sender: "system" }
        ]);
        setTimeout(() => {
          scrollViewRef.current?.scrollToEnd({ animated: true });
        }, 100);
      } 
      else if (message.type === "chat" && message.content) {
        const sender = message.from === "12345" ? "user" : "other";
        setMessages((prevMessages: any) => [
          ...prevMessages,
          { ...message, id: message.id || generateUniqueId(), sender }
        ]);
        setTimeout(() => {
          scrollViewRef.current?.scrollToEnd({ animated: true });
        }, 100);
      }
    });

    // Connect to WebSocket
    messageService.connect();

    // Clean up on unmount
    return () => {
      messageService.disconnect();
      messageService.off("connected");
      messageService.off("disconnected");
      messageService.off("error");
      messageService.off("message");
    };
  }, [chat?.id]);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollViewRef.current?.scrollToEnd({ animated: false });
  }, [messages.length]);

  const sendMessage = () => {
    if (!newMessage.trim() || !isConnected) return;

    const success = messageService.sendMessage(newMessage.trim());
    
    if (success) {
      // Optimistically add message to UI with guaranteed unique ID
      const newMsg: ChatMessage = {
        id: generateUniqueId(),
        type: "chat",
        from: "12345",
        content: newMessage.trim(),
        timestamp: new Date().toISOString(),
        sender: "user",
        // Mark as still sending until echo confirms
        status: "sending"
      };
      
      setMessages((prevMessages: any) => [...prevMessages, newMsg]);
      setNewMessage("");
      
      // Scroll to bottom
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  };

  const MessageBubble = ({
    message,
  }: {
    message: ChatMessage;
  }) => {
    const isUser = message.sender === "user";
    const isSystem = message.sender === "system";
    
    // Special styling for system messages
    if (isSystem) {
      return (
        <View className="flex-row justify-center mb-4">
          <View className={`rounded-2xl px-4 py-2 max-w-[90%] ${
            isDarkMode ? "bg-slate-800" : "bg-gray-100"
          }`}>
            <Text className={`text-center ${isDarkMode ? "text-blue-300" : "text-blue-600"}`}>
              {message.content}
            </Text>
            <Text className={`text-xs mt-1 text-center ${
              isDarkMode ? "text-gray-400" : "text-gray-500"
            }`}>
              {formatTimestamp(new Date(message.timestamp).getTime())}
            </Text>
          </View>
        </View>
      );
    }
    
    return (
      <View
        className={`flex-row mb-4 ${isUser ? "justify-end" : "justify-start"}`}
      >
        <View
          className={`rounded-2xl px-4 py-3 max-w-[80%] ${
            isUser ? "bg-blue-600" : isDarkMode ? "bg-slate-700" : "bg-gray-100"
          }`}
        >
          <Text className={isUser ? "text-white" : undefined}>
            {message.content}
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
            {formatTimestamp(new Date(message.timestamp).getTime())}
          </Text>
        </View>
      </View>
    );
  };

  if (!chat) {
    return null;
  }

  return (
    <SafeAreaView
      className={isDarkMode ? "flex-1 bg-slate-900" : "flex-1 bg-white"}
    >
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        className="flex-1"
      >
        <View
          className={`flex-row items-center p-4 border-b ${isDarkMode ? "border-slate-700" : "border-gray-200"}`}
        >
          <TouchableOpacity onPress={() => router.back()} className="mr-4">
            <FontAwesome5
              name={icons.backArrow}
              size={24}
              color={isDarkMode ? "#FFF" : "#000"}
            />
          </TouchableOpacity>
          <View className="flex-row items-center flex-1">
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
          
          {/* Connection status indicator */}
          <View className="flex-row items-center">
            {isConnecting ? (
              <ActivityIndicator size="small" color="#2563EB" />
            ) : isConnected ? (
              <View className="w-3 h-3 rounded-full bg-green-500 mr-1"></View>
            ) : (
              <View className="w-3 h-3 rounded-full bg-red-500 mr-1"></View>
            )}
          </View>
        </View>

        {connectionError && (
          <View className="bg-red-500 p-2">
            <Text className="text-white text-center">{connectionError}</Text>
          </View>
        )}

        <ScrollView
          ref={scrollViewRef}
          className="flex-1 px-4"
          contentContainerStyle={{ paddingVertical: 20 }}
        >
          {messages.map((message: ChatMessage, index: any) => (
            <MessageBubble
              key={message.id || `msg-${index}-${message.timestamp}`}
              message={message}
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
            className={`w-10 h-10 rounded-full items-center justify-center ${
              !newMessage.trim() || !isConnected ? "bg-blue-300" : "bg-blue-600"
            }`}
            disabled={!newMessage.trim() || !isConnected}
            onPress={sendMessage}
          >
            <FontAwesome5 name="paper-plane" size={18} color="#FFF" />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default ChatDetail;
