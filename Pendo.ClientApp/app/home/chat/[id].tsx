import { FontAwesome5 } from "@expo/vector-icons";
import { router, useGlobalSearchParams, useLocalSearchParams } from "expo-router";
import { useState, useEffect, useRef } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  ScrollView as RNScrollView,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from "react-native";
import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import { Text } from "@/components/common/ThemedText";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { messageService, ChatMessage, getUserConversations, createConversation } from "@/services/messageService";
import { formatTimestamp } from "@/utils/formatTime";

/*
  Helper function to generate unique message IDs internally for categorisation
*/
const generateUniqueId = () => {
  return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

/*
  ChatDetail
  Screen for viewing and sending messages in a chat
*/
const ChatDetail = () => {
  const { id, name, initialMessage } = useLocalSearchParams();
  const [chat, setChat] = useState<any>(null);
  const [newMessage, setNewMessage] = useState(initialMessage as string);
  const { isDarkMode } = useTheme();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(true);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const [hasSetChatVars, setHasSetChatVars] = useState(false);
  const scrollViewRef = useRef<RNScrollView>(null);
  const inputRef = useRef<TextInput>(null);
  const lastSentMessageRef = useRef<string>("");

  /*
    Fetch chat details on initial load
  */
  useEffect(() => {
    async function fetchChat() {
      try {
        // Fetch conversation details from API
        console.log("Fetching conversation details for:", id);
        const response = await getUserConversations();
        
        // Normalise conversation data
        // This is a simplified version of the response structure
        const normalisedConversations = response.conversations.map((conv: any) => ({
          ...conv,
          type: conv.Type ? conv.Type.toLowerCase() : conv.type,
          id: conv.id || conv.ConversationId,
          title: conv.Name,
          lastMessage: conv.lastMessage || "",
          timestamp: new Date(conv.CreateDate).getTime()
        }));
        
        // Find the selected conversation by ID
        const selectedChat = normalisedConversations.find((c: any) => c.id === id);

        if (typeof selectedChat === "undefined") {
          console.log("Chat not found. Creating new conversation.");
          setIsLoadingHistory(false);

          const userName : any = typeof name === "undefined" ? id.toString() : name as string;

          try {
            const response = await createConversation({
              ConversationType: "direct",
              name: `Chat with ${userName}.`,
              participants: [ id.toString() ] // Driver ID
            });
            console.log("Conversation created:", response);

            setHasSetChatVars(true);
            setChat({
              id: response.ConversationId,
              ConversationId: response.ConversationId,
              type: response.Type,
              title: response.Name,
              lastMessage: "",
              timestamp: new Date().getTime(),
              UserId: id.toString()
            });  // pass conversation response

            return;
            
          } catch (error) {
            console.error("Failed to create conversation:", error);
          }
        }

        setHasSetChatVars(true);
        setChat(selectedChat);
      } catch (error) {
        console.error("Error fetching conversation:", error);
      }
    }
    fetchChat();
  }, [id]);

  useEffect(() => {
    console.log("Chat updated:", chat);
    if (chat && messageService) {
      messageService.setConversationId(chat.id);
      // Set user id from normalised conversation response
      // User ID is typically stamped when passing through the gateway 
      // However, non REST API calls bypass this and require manual setting
      if (hasSetChatVars) {
        console.log("Setting user ID:", chat.UserId);
        messageService.setUserId(chat.UserId);

        console.log("Setting conversation ID:", chat.ConversationId);
        messageService.setConversationId(chat.ConversationId);
      }
    }

    // Clear messages when switching chats
    setMessages([]);
    setIsLoadingHistory(false);
  }, [chat?.UserId, chat?.ConversationId]);

  /*
    Set up WebSocket event listeners
  */
  useEffect(() => {
    // Handle connection events
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

    // Handle disconnection events
    messageService.on("disconnected", (reason) => {
      setIsConnected(false);
      setIsLoadingHistory(false);
      if (reason) {
        setConnectionError(`Disconnected: ${reason}`);
      }
    });

    // Handle connection error events
    messageService.on("error", (error) => {
      setConnectionError(`Connection error: ${error}`);
      setIsConnecting(false);
      setIsLoadingHistory(false);
    });

    // Handle message history loaded event
    messageService.on("historyLoaded", (historyMessages) => {
      console.log("History loaded:", historyMessages.length, "messages");
      setIsLoadingHistory(false);

      /*
        Merge new messages with existing messages
        Only add messages that are not already in the list
      */
      setMessages((prevMessages: any[]) => {
        // Create a set of existing message IDs for comparison
        const existingIds = new Set(prevMessages.map((m) => m.id));

        // Filter out messages that are not already in the list
        const newMessages = historyMessages.filter(
          (m) => m.id && !existingIds.has(m.id)
        );

        // Sort messages by timestamp
        return [...prevMessages, ...newMessages].sort(
          (a, b) =>
            new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
        );
      });

      // Scroll to bottom after loading history
      // Derived from: https://reactnative.dev/docs/scrollview
      // Delay scroll to ensure messages are rendered
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: false });
      }, 100);

    });

    // Handle incoming messages
    messageService.on("message", (message) => {
      // Handle user message sent event

      if (message.type === "conversation_joined") {
        console.log("Initial message:", initialMessage);

        if (initialMessage) {
          setNewMessage(initialMessage as string);
          sendMessage();
        }
      }

      if (message.type === "user_message_sent") {
        if (!message.content && lastSentMessageRef.current) {
          message.content = lastSentMessageRef.current;
        }
        // Add user message to list
        setMessages((prev) => [...prev, { ...message, sender: "user", status: "sent" }]);

        lastSentMessageRef.current = "";
        return;
      }
      
      // Handle incoming chat messages
      if (message.type === "chat" && message.content) {
        // Determine sender based on user ID 
        const sender = message.from === chat?.UserId ? "user" : "other";
        
        /*
          Update message status based on sender
          If the message is from the user, update the status to "sent"
        */
        setMessages((prev: any[]) => {
          if (sender === "user") {
            const idx = prev.findIndex((m: { status: string; content: string | undefined; }) => m.status === "sending" && m.content === message.content);
            if (idx !== -1) {
              const newMessages = [...prev];
              newMessages[idx] = { ...newMessages[idx], ...message, status: "sent" };
              return newMessages;
            }
          }

          // Add new message
          // If the message doesn't have an ID, generate one
          // IDs are generated server-side so this is a local categorisation technique
          return [
            ...prev,
            {
              ...message,
              id: message.id,
              sender,
              status: sender === "user" ? "delivered" : undefined,
            },
          ];
        });
      } else if (message.type === "welcome" && message.content) {
        setMessages((prev: any) => [
          ...prev,
          { ...message, id: generateUniqueId(), sender: "system" },
        ]);
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

  /*
    Scroll to bottom when new messages are added
  */
  useEffect(() => {
    if (messages.length > 0 && !isLoadingHistory) {
      scrollViewRef.current?.scrollToEnd({ animated: false });
    }
  }, [messages.length, isLoadingHistory]);

  /*
    Send a message to the chat
  */  
  const sendMessage = () => {
    if (!newMessage.trim() || !isConnected) return;

    // Store last sent message before sending removing unnecessary whitespace
    lastSentMessageRef.current = newMessage.trim();

    const success = messageService.sendMessage(newMessage.trim());
    if (success) {
      setNewMessage("");
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  };

  /*
    MessageBubble
    Component for rendering chat messages
  */
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
          </View>
        </View>
      </View>
    );
  };

  return (
    /* 
      Note: Styling and class names are derived from Tailwind CSS docs
      https://tailwindcss.com/docs/
      Additional design elements have been generated using Figma -> React Native (Tailwind)
      https://www.figma.com/community/plugin/821138713091291738/figma-react-native
      https://www.figma.com/community/plugin/1283055580669946018/tailwind-react-code-generator-by-pagesloft
    */

    // KeyboardAvoidingView derived from: https://reactnative.dev/docs/keyboardavoidingview
    <ThemedSafeAreaView
      className={isDarkMode ? "flex-1 bg-slate-900" : "flex-1 bg-white"}
    >
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        keyboardVerticalOffset={80}
        className="flex-1"
      >
        { !chat ? (
          <View className="flex-1 items-center justify-center">
            <Text>Loading...</Text>
          </View>
        ) : (
          <>
            {/* Header */}
            <View className={`flex-row items-center p-4 border-b ${isDarkMode ? "border-slate-700" : "border-gray-200"}`}>
              <TouchableOpacity onPress={() => router.back()} className="mr-4">
                <FontAwesome5 name={icons.backArrow} size={24} color={isDarkMode ? "#FFF" : "#000"} />
              </TouchableOpacity>
              <View className="flex-row items-center flex-1">
                <View className={`w-10 h-10 rounded-full items-center justify-center mr-3 ${isDarkMode ? "bg-slate-700" : "bg-gray-100"}`}>
                  <FontAwesome5 name={chat.type === "support" ? icons.chat : icons.person} size={20} color="#2563EB" />
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
      
            <RNScrollView ref={scrollViewRef} className="flex-1 px-4" contentContainerStyle={{ paddingVertical: 20 }}>

              {/* History loading indicator */}
              {isLoadingHistory && (
                <View className="flex-row justify-center mb-4">
                  <ActivityIndicator size="small" color="#2563EB" />
                  <Text className="ml-2 text-gray-500">Loading message history...</Text>
                </View>
              )}
      
              {messages.filter(message => message.type !== "welcome" && message.content !== undefined).map((message: ChatMessage, index: any) => (
                <MessageBubble key={message.id || `msg-${index}-${message.timestamp}`} message={message} />
              ))}
            </RNScrollView>
      
            {/* Message Input */}
            <View className="p-4 border-t border-gray-200 flex-row items-center">
              <TextInput
                ref={inputRef}
                className={`flex-1 px-4 py-2 mr-2 rounded-full ${isDarkMode ? "bg-slate-700 text-white" : "bg-gray-100 text-black"}`}
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
          </>
        )}
      </KeyboardAvoidingView>
    </ThemedSafeAreaView>
  );
};

export default ChatDetail;
