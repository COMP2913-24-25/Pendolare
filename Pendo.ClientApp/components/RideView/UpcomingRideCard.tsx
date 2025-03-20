import { View, TouchableOpacity } from "react-native";
import { Text } from "@/components/common/ThemedText"; // updated
import { useTheme } from "@/context/ThemeContext";
import { Ride } from "@/constants";
import StatusBadge from "./StatusBadge";

interface UpcomingRideCardProps {
  ride : Ride;
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
        <Text className="text-lg font-JakartaBold">{ride.Dropoff.name}</Text>
        <Text className="text-blue-600 font-JakartaBold">£{ride.Price.toFixed(2)}</Text>
      </View>
      <View className="flex-row justify-between items-center mb-2">
        <Text className="text-gray-500">{ride.RideTime.toUTCString()}</Text>
        <Text className="text-gray-500">With {ride.DriverName}</Text>
      </View>
      <StatusBadge statusText={ride.Status} />
    </TouchableOpacity>
  );
};

export default UpcomingRideCard;
