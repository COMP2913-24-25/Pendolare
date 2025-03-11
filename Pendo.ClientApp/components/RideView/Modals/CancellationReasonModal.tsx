import React from "react";
import { View, Text, TouchableOpacity, Modal } from "react-native";

import { cancelReasons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";

interface CancellationReasonModalProps {
  visible: boolean;
  onCancel: () => void;
  onReasonSelect: (reason: string) => void;
}

/*
    CancellationReasonModal
    Modal component for selecting a reason when cancelling a ride
*/
const CancellationReasonModal = ({
  visible,
  onCancel,
  onReasonSelect,
}: CancellationReasonModalProps) => {
  const { isDarkMode } = useTheme();

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="fade"
      onRequestClose={onCancel}
    >
      <View className="flex-1 bg-black/50 justify-center items-center">
        <View
          className={`p-6 rounded-xl w-[90%] max-w-[400px] ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
        >
          <Text
            className={`text-xl font-JakartaBold mb-4 ${isDarkMode ? "text-white" : "text-black"}`}
          >
            Cancel Ride
          </Text>
          <Text
            className={`mb-4 ${isDarkMode ? "text-gray-300" : "text-gray-600"}`}
          >
            Please select a reason for cancellation:
          </Text>

          {cancelReasons.map((reason) => (
            <TouchableOpacity
              key={reason}
              className={`py-3 border-b ${isDarkMode ? "border-slate-700" : "border-gray-100"}`}
              onPress={() => onReasonSelect(reason)}
            >
              <Text className="text-blue-600">{reason}</Text>
            </TouchableOpacity>
          ))}

          <TouchableOpacity className="mt-4 py-3" onPress={onCancel}>
            <Text
              className={
                isDarkMode
                  ? "text-gray-300 text-center"
                  : "text-gray-500 text-center"
              }
            >
              Never mind
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
};

export default CancellationReasonModal;
