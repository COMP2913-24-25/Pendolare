import { FontAwesome5 } from "@expo/vector-icons";
import { View, TouchableOpacity } from "react-native";
import { Text } from "@/components/common/ThemedText"; // updated import
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { Rating } from "react-native-ratings";
import CronVisualiser from "./CronVisualiser";

interface RideEntryCardProps {
  ride: {
    driverName: string;
    rating: number;
    price: string;
    departureTime: string;
    pickup: { name: string };
    dropoff: { name: string };
    recurrence?: string;
    repeatUntil: Date;
  };
  onPress: () => void;
}

/**
 * RideEntryCard
 * Card component for displaying a ride entry with details
 */
const RideEntryCard = ({ ride, onPress }: RideEntryCardProps) => {
  const { isDarkMode } = useTheme();

  const formattedDate = new Date(Date.parse(ride.departureTime)).toLocaleString();

  /* 
    Note: Styling and class names are derived from Tailwind CSS docs
    https://tailwindcss.com/docs/
    Additional design elements have been generated using Figma -> React Native (Tailwind)
    https://www.figma.com/community/plugin/821138713091291738/figma-react-native
    https://www.figma.com/community/plugin/1283055580669946018/tailwind-react-code-generator-by-pagesloft
  */
  return (
    <TouchableOpacity
      className={`p-4 rounded-xl mb-4 shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
      onPress={onPress}
    >
      <View className="flex-row justify-between items-center mb-3">
        <View className="flex-row items-center">
          <View
            className={`w-10 h-10 rounded-full items-center justify-center mr-2 ${isDarkMode ? "bg-slate-700" : "bg-gray-100"}`}
          >
            <FontAwesome5
              name={icons.person}
              size={20}
              color={isDarkMode ? "#FFF" : "#666666"}
            />
          </View>
          <View>
            <Text className="font-JakartaBold">{ride.driverName}</Text>
            <View className="flex-row items-center mt-1">
              {ride.rating === -1 ? (
                <Text className="text-xs font-Jakarta">No driver rating yet!</Text>
              ) : (
                <Rating startingValue={ride.rating} readonly imageSize={16} />
              )}
            </View>
          </View>
        </View>
        <Text className="font-JakartaBold text-blue-600">{ride.price}</Text>
      </View>

      <View>
        <View className="flex-row items-center mb-2">
          <FontAwesome5
            name={icons.time}
            size={16}
            color={isDarkMode ? "#FFF" : "#666666"}
            style={{ marginRight: 8 }}
          />
          <Text className={`font-JakartaBold ${isDarkMode ? "text-white-600" : "text-gray-600"}`}>
            {formattedDate}
          </Text>
        </View>
        <View className="flex-row items-center mb-2">
          <FontAwesome5
            name={icons.to}
            size={16}
            color="#2563EB"
            style={{ marginRight: 8 }}
          />
          <Text className={`${isDarkMode ? "text-white-600" : "text-gray-600"}`}>
            {ride.pickup.name}
          </Text>
        </View>
        <View className="flex-row items-center">
          <FontAwesome5
            name={icons.target}
            size={16}
            color="#DC2626"
            style={{ marginRight: 8 }}
          />
          <Text className={`${isDarkMode ? "text-white-600" : "text-gray-600"}`}>
            {ride.dropoff.name}
          </Text>
        </View>
      </View>
      <View className="mt-2">
        {ride.recurrence && (
            <CronVisualiser cron={ride.recurrence} endDate={ride.repeatUntil} isDarkMode={isDarkMode} />
        )}
      </View>
    </TouchableOpacity>
  );
};

export default RideEntryCard;
