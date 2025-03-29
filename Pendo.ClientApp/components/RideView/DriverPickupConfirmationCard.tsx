import { View, TouchableOpacity } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";

interface DriverPickupConfirmationCardProps {
  passenger: any;
  onConfirmArrival: () => void;
}

/*
    DriverPickupConfirmationCard
    Card for a driver to confirm they are at the pickup location
*/
const DriverPickupConfirmationCard = ({
  passenger,
  onConfirmArrival,
}: DriverPickupConfirmationCardProps) => {
  const { isDarkMode } = useTheme();

  return (
    <View className={`p-4 rounded-lg shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}>
      <View className="items-center justify-between">
        {/* Text Section */}
        <View className="flex-1">
          <Text className="text-lg font-JakartaBold mb-1">
            Confirm Pickup Location
          </Text>
          <Text className="text-base font-JakartaRegular">
            Let {passenger ?? "your passenger"} know you are at the pickup location!
          </Text>
        </View>
        {/* Confirmation Button */}
        <TouchableOpacity
          onPress={onConfirmArrival}
          className="bg-green-500 rounded-lg px-4 py-2 items-center justify-center"
        >
          <Text className="text-white font-JakartaBold text-center">
            Confirm at pickup location
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default DriverPickupConfirmationCard;