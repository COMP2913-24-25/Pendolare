import { View, TouchableOpacity } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import { FontAwesome5 } from "@expo/vector-icons";

interface RideConfirmationCardProps {
  ride: any;
  onConfirmComplete: () => void;
  onConfirmIncomplete: () => void;
}

/*
    RideConfirmationCard
    Card for confirming whether a ride was completed or not
*/
const RideConfirmationCard = ({
  ride,
  onConfirmComplete,
  onConfirmIncomplete,
}: RideConfirmationCardProps) => {
  const { isDarkMode } = useTheme();

  return (
    <View className={`p-4 rounded-lg shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}>
      <View className="flex-row items-center justify-between">
        {/* Text Section */}
        <View className="flex-1">
          <Text className="text-lg font-JakartaBold mb-1">
            Confirm Ride Completion
          </Text>
          <Text className="text-base font-JakartaRegular">
            Did you complete the ride with {ride.DriverName}?
          </Text>
        </View>
        {/* Buttons Section */}
        <View className="flex-row space-x-2">
          <TouchableOpacity
            className="bg-green-500 items-center justify-center rounded-lg w-12 h-12"
            onPress={onConfirmComplete}
          >
            <FontAwesome5 name="check" size={20} color="white" />
          </TouchableOpacity>
          <TouchableOpacity
            className="bg-red-500 items-center justify-center rounded-lg w-12 h-12"
            onPress={onConfirmIncomplete}
          >
            <FontAwesome5 name="times" size={20} color="white" />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

export default RideConfirmationCard;