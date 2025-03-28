import React, { forwardRef } from 'react';
import { ScrollView, View, ActivityIndicator } from 'react-native';
import { Text } from '@/components/common/ThemedText';
import { ChatMessage } from '@/services/messageService';
import MessageBubble from './MessageBubble';

interface ChatMessagesProps {
  messages: ChatMessage[];
  isLoadingHistory: boolean;
  currentUserId: string;
  isDriverMode: boolean;
  onApproveAmendment: (amendmentId: string) => void;
}

const ChatMessages = forwardRef<ScrollView, ChatMessagesProps>(({
  messages,
  isLoadingHistory,
  currentUserId,
  isDriverMode,
  onApproveAmendment
}, ref) => {
  return (
    <ScrollView 
      ref={ref} 
      className="flex-1 px-4" 
      contentContainerStyle={{ paddingVertical: 20 }}
    >
      {/* History loading indicator */}
      {isLoadingHistory && (
        <View className="flex-row justify-center mb-4">
          <ActivityIndicator size="small" color="#2563EB" />
          <Text className="ml-2 text-gray-500">Loading message history...</Text>
        </View>
      )}

      {messages
        .filter(message => message.type !== "welcome" && message.content !== undefined)
        .map((message: ChatMessage, index: number) => (
          <MessageBubble 
            key={message.id || `msg-${index}-${message.timestamp}`} 
            message={message}
            currentUserId={currentUserId}
            isDriverMode={isDriverMode}
            onApproveAmendment={onApproveAmendment}
          />
        ))}
    </ScrollView>
  );
});

export default ChatMessages;
