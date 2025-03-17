import { FontAwesome5 } from "@expo/vector-icons";
import { View, TouchableOpacity, Modal } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText";
import { createConversation } from "@/services/messageService";

const supportCategories = [
  { id: "billing", title: "Billing & Payments", icon: "dollar-sign" },
  { id: "auth", title: "Account & Authentication", icon: "user-shield" },
  { id: "disputes", title: "Disputes & Issues", icon: "exclamation-circle" },
  { id: "general", title: "General Enquiries", icon: "comment-dots" },
];

interface ContactSupportProps {
  visible: boolean;
  onClose: () => void;
  onSelectCategory: (category: string) => void;
}

/*
  ContactSupport
  Modal component for selecting a support category
*/
const ContactSupport = ({
  visible,
  onClose,
  onSelectCategory,
}: ContactSupportProps) => {
  const { isDarkMode } = useTheme();

  const handleCategorySelect = async (category: string) => {
    try {
      const response = await createConversation({
        UserId: "0", // Automatically appended through Kong
        ConversationType: "Support",
        name: category,
        participants: ["0"], // Support participant ID
      });
      console.log("Conversation created:", response);
      onSelectCategory(category);
    } catch (error) {
      console.error("Failed to create conversation:", error);
    }
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
    >
      <SafeAreaView
        className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
      >
        <View className="flex-1 px-5 pt-8 pb-4">
          <View className="flex-row items-center justify-between mb-6">
            <TouchableOpacity onPress={onClose} className="p-2 -ml-2 mt-4">
              <FontAwesome5
                name={icons.backArrow}
                size={24}
                color={isDarkMode ? "#FFF" : "#000"}
              />
            </TouchableOpacity>
            <Text className="text-2xl font-JakartaBold mt-4">
              Contact Support
            </Text>
            <View className="w-10 mt-4" />
          </View>

          <Text className="text-base mb-6">
            Please select a category for your enquiry
          </Text>

          {supportCategories.map((category) => (
            <TouchableOpacity
              key={category.id}
              className={`p-4 rounded-xl mb-4 flex-row items-center ${
                isDarkMode ? "bg-slate-800" : "bg-white"
              }`}
              onPress={() => handleCategorySelect(category.id)}
            >
              <View
                className={`w-10 h-10 rounded-full items-center justify-center mr-4 ${
                  isDarkMode ? "bg-slate-700" : "bg-blue-50"
                }`}
              >
                <FontAwesome5
                  name={category.icon}
                  size={20}
                  color={isDarkMode ? "#60A5FA" : "#2563EB"}
                />
              </View>
              <Text
                className={`text-lg font-JakartaMedium ${
                  isDarkMode ? "text-white" : "text-black"
                }`}
              >
                {category.title}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </SafeAreaView>
    </Modal>
  );
};

export default ContactSupport;
