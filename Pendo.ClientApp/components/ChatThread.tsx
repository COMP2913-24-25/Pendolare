import { FontAwesome5 } from "@expo/vector-icons";
import { View, TouchableOpacity } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { formatTimestamp } from "@/utils/formatTime";

interface ChatThreadProps {
  type: "support" | "driver";
  title: string;
  lastMessage: string;
  timestamp: number;
  unread: number;
  onPress: () => void;
}

/*
  ChatThread
  Thread item for chat list
*/
const ChatThread = ({
  type,
  title,
  lastMessage,
  timestamp,
  unread,
  onPress,
}: ChatThreadProps) => {
  const { isDarkMode } = useTheme();

  return (
    <TouchableOpacity
      className={`flex-row items-center p-4 rounded-xl mb-3 shadow-sm ${
        isDarkMode ? "bg-slate-800" : "bg-white"
      }`}
      onPress={onPress}
    >
      <View
        className={`w-12 h-12 rounded-full items-center justify-center mr-3 ${
          isDarkMode ? "bg-slate-700" : "bg-gray-100"
        }`}
      >
        <FontAwesome5
          name={type === "support" ? icons.chat : icons.person}
          size={24}
          color={isDarkMode ? "#FFF" : "#2563EB"}
        />
      </View>

      <View className="flex-1">
        <View className="flex-row justify-between items-center">
          <Text className="font-JakartaBold text-lg">{title}</Text>
          <Text style={{ fontSize: 12 }}>
            {formatTimestamp(timestamp)}
          </Text>
        </View>

        <View className="flex-row justify-between items-center mt-1">
          <Text
            className="flex-1 mr-2"
            numberOfLines={1}
          >
            {lastMessage}
          </Text>
          {unread > 0 && (
            <View className="bg-blue-600 rounded-full w-5 h-5 items-center justify-center">
              <Text className="text-white text-xs">{unread}</Text>
            </View>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );
};

export default ChatThread;
