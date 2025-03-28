import React from 'react';
import { View, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Text } from '@/components/common/ThemedText';
import { FontAwesome5 } from '@expo/vector-icons';
import { useTheme } from '@/context/ThemeContext';
import { router } from 'expo-router';
import { icons } from '@/constants';

interface ChatHeaderProps {
  title: string;
  chatType: string;
  isConnecting: boolean;
  isConnected: boolean;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ 
  title, 
  chatType, 
  isConnecting, 
  isConnected 
}) => {
  const { isDarkMode } = useTheme();

  return (
    <View className={`flex-row items-center p-4 border-b ${isDarkMode ? "border-slate-700" : "border-gray-200"}`}>
      <TouchableOpacity onPress={() => router.back()} className="mr-4">
        <FontAwesome5 name={icons.backArrow} size={24} color={isDarkMode ? "#FFF" : "#000"} />
      </TouchableOpacity>
      <View className="flex-row items-center flex-1">
        <View className={`w-10 h-10 rounded-full items-center justify-center mr-3 ${isDarkMode ? "bg-slate-700" : "bg-gray-100"}`}>
          <FontAwesome5 name={chatType === "support" ? icons.chat : icons.person} size={20} color="#2563EB" />
        </View>
        <Text className="font-JakartaBold text-lg">{title}</Text>
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
  );
};

export default ChatHeader;
