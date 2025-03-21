import { View, TouchableOpacity } from "react-native";
import { Text } from "@/components/common/ThemedText"; // updated
import { useTheme } from "@/context/ThemeContext";
import { formatTimestamp } from "@/utils/formatTime";

interface UpcomingRideCardProps {
  ride: {
    driverName: string;
    departureTime: number;
    price: string;
    dropoff: { name: string };
  };
  onPress: () => void;
}

/*
    UpcomingRideCard
    Card for upcoming ride in ride view
*/
const UpcomingRideCard = ({ ride, onPress }: UpcomingRideCardProps) => {
  const { isDarkMode } = useTheme();

  /* 
    Note: Styling and class names are derived from Tailwind CSS docs
    https://tailwindcss.com/docs/
    Additional design elements have been generated using Figma -> React Native (Tailwind)
    https://www.figma.com/community/plugin/821138713091291738/figma-react-native
    https://www.figma.com/community/plugin/1283055580669946018/tailwind-react-code-generator-by-pagesloft
  */
  return (
    <TouchableOpacity
      className={`p-4 rounded-lg shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
      onPress={onPress}
    >
      <View className="flex-row justify-between items-center mb-2">
        <Text className="text-lg font-JakartaBold">{ride.dropoff.name}</Text>
        <Text className="text-blue-600 font-JakartaBold">{ride.price}</Text>
      </View>
      <View className="flex-row justify-between items-center">
        <Text className="text-gray-500">{formatTimestamp(ride.departureTime)}</Text>
        <Text className="text-gray-500">with {ride.driverName}</Text>
      </View>
    </TouchableOpacity>
  );
};

export default UpcomingRideCard;
