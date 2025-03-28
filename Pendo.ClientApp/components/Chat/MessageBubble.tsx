import React from 'react';
import { View } from 'react-native';
import { Text } from '@/components/common/ThemedText';
import { useTheme } from '@/context/ThemeContext';
import { formatTimestamp } from '@/utils/formatTime';
import { ChatMessage } from '@/services/messageService';
import AmendmentRequestBubble from './AmendmentRequestBubble';

interface MessageBubbleProps {
  message: ChatMessage;
  currentUserId: string;
  isDriverMode: boolean;
  onApproveAmendment: (amendmentId: string) => void;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ 
  message, 
  currentUserId, 
  isDriverMode,
  onApproveAmendment 
}) => {
  const { isDarkMode } = useTheme();
  const isUser = message.sender === "user";
  const isSystem = message.sender === "system";
  
  // Enhanced logging for all messages to help debug
  console.log(`Rendering message: type=${message.type}, amendmentId=${message.amendmentId}`, message);
  
  // Improved detection of booking amendment messages
  if (message.type === "booking_amendment" || message.amendmentId) {
    try {
      console.log("Processing amendment message:", message);
      
      // Parse the content if it's a stringified JSON
      let amendmentData = message.content;
      
      // Handle different message formats
      if (typeof amendmentData === 'string') {
        try {
          // First try direct parsing
          amendmentData = JSON.parse(amendmentData);
        } catch (e) {
          console.error("Failed to parse amendment data:", e);
          return (
            <View className="flex-row justify-center mb-4">
              <View className={`rounded-2xl px-4 py-2 max-w-[90%] ${isDarkMode ? "bg-red-800" : "bg-red-100"}`}>
                <Text className={`text-center ${isDarkMode ? "text-white" : "text-red-600"}`}>
                  Booking amendment request (Unable to display details)
                </Text>
                <Text className={`text-center text-xs ${isDarkMode ? "text-white" : "text-red-600"}`}>
                  Raw content: {typeof amendmentData === 'string' ? amendmentData.substring(0, 50) : 'Non-string content'}
                </Text>
              </View>
            </View>
          );
        }
      }
      
      console.log("Processed amendment data:", amendmentData);
      console.log("Current user is in driver mode:", isDriverMode);
      
      // Render amendment request bubble with the parsed data
      return (
        <AmendmentRequestBubble 
          amendment={amendmentData}
          amendmentId={message.amendmentId || ''}
          isFromCurrentUser={isUser}
          timestamp={message.timestamp}
          onApprove={onApproveAmendment}
          isDriverView={isDriverMode}
        />
      );
    } catch (error) {
      console.error("Error rendering amendment message:", error);
      // Return a fallback UI for errors
      return (
        <View className="flex-row justify-center mb-4">
          <View className={`rounded-2xl px-4 py-2 max-w-[90%] ${isDarkMode ? "bg-red-800" : "bg-red-100"}`}>
            <Text className={`text-center ${isDarkMode ? "text-white" : "text-red-600"}`}>
              Error displaying booking amendment
            </Text>
            <Text className={`text-center text-xs ${isDarkMode ? "text-white" : "text-red-600"}`}>
              Error: {error.message}
            </Text>
          </View>
        </View>
      );
    }
  }

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

export default MessageBubble;
