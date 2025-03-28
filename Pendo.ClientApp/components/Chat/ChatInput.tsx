import React, { useRef } from 'react';
import { View, TextInput, TouchableOpacity } from 'react-native';
import { FontAwesome5 } from '@expo/vector-icons';
import { useTheme } from '@/context/ThemeContext';

interface ChatInputProps {
  message: string;
  onChangeMessage: (text: string) => void;
  onSendMessage: () => void;
  onShowAmendmentModal: () => void;
  isConnected: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({
  message,
  onChangeMessage,
  onSendMessage,
  onShowAmendmentModal,
  isConnected
}) => {
  const { isDarkMode } = useTheme();
  const inputRef = useRef<TextInput>(null);

  return (
    <View className="p-4 border-t border-gray-200 flex-row items-center">
      {/* Plus button for booking amendment */}
      <TouchableOpacity
        className={`w-10 h-10 rounded-full items-center justify-center mr-2 ${
          isDarkMode ? "bg-slate-700" : "bg-gray-100"
        }`}
        onPress={onShowAmendmentModal}
      >
        <FontAwesome5 name="plus" size={18} color={isDarkMode ? "#FFF" : "#000"} />
      </TouchableOpacity>
      
      <TextInput
        ref={inputRef}
        className={`flex-1 px-4 py-2 mr-2 rounded-full ${isDarkMode ? "bg-slate-700 text-white" : "bg-gray-100 text-black"}`}
        placeholder="Type a message..."
        placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
        value={message}
        onChangeText={onChangeMessage}
        multiline
      />
      
      <TouchableOpacity
        className={`w-10 h-10 rounded-full items-center justify-center ${
          !message.trim() || !isConnected ? "bg-blue-300" : "bg-blue-600"
        }`}
        disabled={!message.trim() || !isConnected}
        onPress={onSendMessage}
      >
        <FontAwesome5 name="paper-plane" size={18} color="#FFF" />
      </TouchableOpacity>
    </View>
  );
};

export default ChatInput;
