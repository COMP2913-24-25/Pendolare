import { FontAwesome5 } from "@expo/vector-icons";
import { View, TouchableOpacity, Modal } from "react-native";

import RatingStars from "@/components/RatingStars";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { Text } from "@/components/common/ThemedText"; // updated

interface RideCompletionModalProps {
  visible: boolean;
  driverName: string;
  rating: number;
  setRating: (rating: number) => void;
  onClose: () => void;
  onSubmit: () => void;
  onDispute: () => void;
}

/*
    RideCompletionModal
    Modal component for confirming ride completion and providing rating
*/
const RideCompletionModal = ({
  visible,
  driverName,
  rating,
  setRating,
  onClose,
  onSubmit,
  onDispute,
}: RideCompletionModalProps) => {
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
          <Text className="text-xl font-JakartaBold mb-2 text-center">How was your ride?</Text>
          <View className="mb-8">
            <Text className="mb-4 text-center">Rate your ride with {driverName}</Text>
            <RatingStars rating={rating} setRating={setRating} size={10} />
          </View>

          <View className="flex-row justify-between items-center">
            <TouchableOpacity onPress={onDispute} className="flex-row items-center">
              <FontAwesome5 name={icons.close} size={20} color="#DC2626" style={{ marginRight: 8 }}/>
              <Text className="font-JakartaMedium">Report an Issue</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={onSubmit} disabled={rating === 0} className={`py-2 px-4 rounded-lg ${rating > 0 ? "bg-blue-600" : "bg-gray-300"}`}>
              <Text className="text-white">Submit</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

export default RideCompletionModal;
