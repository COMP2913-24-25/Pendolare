import { View, Modal, TouchableOpacity } from "react-native";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText"; // updated

interface LateCancellationModalProps {
  visible: boolean;
  onClose: () => void;
  onConfirm: () => void;
}

/*
    LateCancellationModal
    Modal component that warns users of cancellation fees for cancelling close to departure time
*/
const LateCancellationModal = ({
  visible,
  onClose,
  onConfirm,
}: LateCancellationModalProps) => {
  const { isDarkMode } = useTheme();

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="fade"
      onRequestClose={onClose}
    >
      <View className="flex-1 bg-black/50 justify-center items-center">
        <View
          className={`p-6 rounded-xl w-[90%] max-w-[400px] ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
        >
          <Text className="text-xl font-JakartaBold mb-4">Late Cancellation Fee</Text>
          <Text className="mb-6">
            Cancelling within 15 minutes of departure will incur a fee of 75% of
            the ride cost. Do you want to proceed?
          </Text>

          <View className="flex-row justify-end gap-4">
            <TouchableOpacity onPress={onClose} className="py-2 px-4">
              <Text>Never mind</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={onConfirm}
              className="bg-red-600 py-2 px-4 rounded-lg"
            >
              <Text className="text-white">Yes, Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

export default LateCancellationModal;
