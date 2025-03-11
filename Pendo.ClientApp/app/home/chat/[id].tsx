import { FontAwesome5 } from "@expo/vector-icons";
import { router, useLocalSearchParams } from "expo-router";
import React, { useState, useEffect, useRef } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  ScrollView as RNScrollView,
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
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const [isTyping, setIsTyping] = useState(false);
  const [typingUser, setTypingUser] = useState<string | null>(null);
  const scrollViewRef = useRef<RNScrollView>(null);
  const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const inputRef = useRef<TextInput>(null);

  const chat = demoChats.find((c: { id: number }) => c.id === Number(id));

  useEffect(() => {
    // Set the conversation ID in the message service when the chat changes
    // This ensures we're in the correct conversation context
    if (chat && messageService) {
      messageService.setConversationId(`chat-${chat.id}`);
    }

    // Clear messages when switching chats
    setMessages([]);
    setIsLoadingHistory(false);
  }, [chat?.id]);

  useEffect(() => {
    // Set up WebSocket event listeners
    messageService.on("connected", () => {
      setIsConnected(true);
      setIsConnecting(false);
      setConnectionError(null);

      // Once connected, request message history
      if (chat) {
        setIsLoadingHistory(true);
        messageService.requestMessageHistory();
      }
    });

    messageService.on("disconnected", (reason) => {
      setIsConnected(false);
      setIsLoadingHistory(false);
      if (reason) {
        setConnectionError(`Disconnected: ${reason}`);
      }
    });

    messageService.on("error", (error) => {
      setConnectionError(`Connection error: ${error}`);
      setIsConnecting(false);
      setIsLoadingHistory(false);
    });

    // New listener for history loaded event
    messageService.on("historyLoaded", (historyMessages) => {
      console.log("History loaded:", historyMessages.length, "messages");
      setIsLoadingHistory(false);

      // Process and add historical messages
      if (historyMessages.length > 0) {
        setMessages((prevMessages) => {
          // Merge with any existing messages, avoiding duplicates by ID
          const existingIds = new Set(prevMessages.map((m) => m.id));
          const newMessages = historyMessages.filter(
            (m) => m.id && !existingIds.has(m.id),
          );

          // Sort all messages by timestamp
          return [...prevMessages, ...newMessages].sort(
            (a, b) =>
              new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime(),
          );
        });

        // Scroll to bottom after history is loaded
        setTimeout(() => {
          scrollViewRef.current?.scrollToEnd({ animated: false });
        }, 100);
      }
    });

    messageService.on("message", (message) => {
      if ((message as any).isEcho) {
        // Update the last outgoing message with status "sent"
        setMessages((prevMessages) => {
          const idx = prevMessages.findIndex(
            (msg) =>
              msg.status === "sending" && msg.content === message.content,
          );
          if (idx !== -1) {
            const updated = {
              ...prevMessages[idx],
              ...message,
              status: "sent" as const, // <-- cast to const
            };
            const newMessages = [...prevMessages];
            newMessages[idx] = updated;
            return newMessages;
          }
          return prevMessages;
        });
      } else if (message.type === "welcome" && message.content) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { ...message, id: generateUniqueId(), sender: "system" },
        ]);
      } else if (message.type === "chat" && message.content) {
        const sender = message.from === "12345" ? "user" : "other";

        if (sender === "other" && message.id) {
          messageService.sendReadReceipt(message.id);
        }

        setMessages((prevMessages) => {
          // For outgoing messages, update existing one if found
          if (sender === "user") {
            const idx = prevMessages.findIndex(
              (msg) =>
                msg.status === "sending" && msg.content === message.content,
            );
            if (idx !== -1) {
              const updated = {
                ...prevMessages[idx],
                ...message,
                status: "sent" as const, // <-- cast to const
              };
              const newMessages = [...prevMessages];
              newMessages[idx] = updated;
              return newMessages;
            }
          }
          return [
            ...prevMessages,
            {
              ...message,
              id: message.id || generateUniqueId(),
              sender,
              read: sender === "user",
              status: sender === "user" ? "delivered" : undefined,
            },
          ];
        });
      } else if (message.type === "read_receipt") {
        setMessages((prevMessages) => {
          return prevMessages.map((msg) => {
            if (
              msg.id === (message as any).message_id &&
              msg.sender === "user"
            ) {
              return { ...msg, read: true, status: "read" as const };
            }
            return msg;
          });
        });
      }
      // Scroll to bottom
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);
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
      messageService.off("historyLoaded");
    };
  }, [chat?.id]);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messages.length > 0 && !isLoadingHistory) {
      scrollViewRef.current?.scrollToEnd({ animated: false });
    }
  }, [messages.length, isLoadingHistory]);

  const sendMessage = () => {
    if (!newMessage.trim() || !isConnected) return;

    const success = messageService.sendMessage(newMessage.trim());

    if (success) {
      // Removed optimistic UI update – wait for server echo
      setNewMessage("");

      // Scroll to bottom
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  };

  // Handle typing indicator
  const handleTextChange = (text: string) => {
    setNewMessage(text);
  };

  const MessageBubble = ({ message }: { message: ChatMessage }) => {
    const isUser = message.sender === "user";
    const isSystem = message.sender === "system";

    // Special styling for system messages
    if (isSystem) {
      return (
        <View className="flex-row justify-center mb-4">
          <View
            className={`rounded-2xl px-4 py-2 max-w-[90%] ${
              isDarkMode ? "bg-slate-800" : "bg-gray-100"
            }`}
          >
            <Text
              className={`text-center ${isDarkMode ? "text-blue-300" : "text-blue-600"}`}
            >
              {message.content}
            </Text>
            <Text
              className={`text-xs mt-1 text-center ${
                isDarkMode ? "text-gray-400" : "text-gray-500"
              }`}
            >
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
          <View className="flex-row items-center justify-between mt-1">
            <Text
              className={`text-xs ${
                isUser
                  ? "text-blue-200"
                  : isDarkMode
                    ? "text-gray-400"
                    : "text-gray-500"
              }`}
            >
              {formatTimestamp(new Date(message.timestamp).getTime())}
            </Text>

            {/* Read receipt indicator for user messages */}
            {isUser && message.status && (
              <View className="ml-2">
                {message.status === "sending" && (
                  <FontAwesome5
                    name="clock"
                    size={10}
                    color={isDarkMode ? "#9CA3AF" : "#9CA3AF"}
                  />
                )}
                {message.status === "sent" && (
                  <FontAwesome5
                    name="check"
                    size={10}
                    color={isDarkMode ? "#9CA3AF" : "#9CA3AF"}
                  />
                )}
                {message.status === "delivered" && (
                  <FontAwesome5
                    name="check-double"
                    size={10}
                    color={isDarkMode ? "#9CA3AF" : "#9CA3AF"}
                  />
                )}
                {message.status === "read" && (
                  <FontAwesome5 name="check-double" size={10} color="#3B82F6" />
                )}
              </View>
            )}
          </View>
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

        <RNScrollView
          ref={scrollViewRef} // No need for type casting when using the correct type
          className="flex-1 px-4"
          contentContainerStyle={{ paddingVertical: 20 }}
        >
          {/* History loading indicator */}
          {isLoadingHistory && (
            <View className="flex-row justify-center mb-4">
              <ActivityIndicator size="small" color="#2563EB" />
              <Text className="ml-2 text-gray-500">
                Loading message history...
              </Text>
            </View>
          )}

          {messages.map((message, index) => (
            <MessageBubble
              key={message.id || `msg-${index}-${message.timestamp}`}
              message={message}
            />
          ))}
        </RNScrollView>

        <View className="p-4 border-t border-gray-200 flex-row items-center">
          <TextInput
            ref={inputRef}
            className={`flex-1 px-4 py-2 mr-2 rounded-full ${
              isDarkMode ? "bg-slate-700 text-white" : "bg-gray-100 text-black"
            }`}
            placeholder="Type a message..."
            placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
            value={newMessage}
            onChangeText={handleTextChange}
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
