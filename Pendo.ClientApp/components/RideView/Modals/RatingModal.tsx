import { View, TouchableOpacity, Modal } from "react-native";
import RatingStars from "@/components/RatingStars";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText"; // updated

interface RatingModalProps {
  visible: boolean;
  driverName: string;
  rating: number;
  setRating: (rating: number) => void;
  onClose: () => void;
  onSubmit: () => void;
}

/*
    RatingModal
    Modal component for rating a driver
*/
const RatingModal = ({
  visible,
  driverName,
  rating,
  setRating,
  onClose,
  onSubmit,
}: RatingModalProps) => {
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
          <Text className="text-xl font-JakartaBold mb-2 text-center">
            Rate your driver
          </Text>
          <Text className="mb-4 text-center">
            How was your ride with {driverName}?
          </Text>

          <RatingStars rating={rating} setRating={setRating} />

          <View className="flex-row justify-end gap-4 mt-4">
            <TouchableOpacity onPress={onClose} className="py-2 px-4">
              <Text>Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={onSubmit}
              disabled={rating === 0}
              className={`py-2 px-4 rounded-lg ${
                rating > 0 ? "bg-blue-600" : "bg-gray-300"
              }`}
            >
              <Text className="text-white">Submit Rating</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

export default RatingModal;
