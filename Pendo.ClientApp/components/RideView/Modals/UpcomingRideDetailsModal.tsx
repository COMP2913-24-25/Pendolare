import { FontAwesome5 } from "@expo/vector-icons";
import { View, TouchableOpacity, Modal } from "react-native";

import Map from "../../Map/Map";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { formatTimestamp } from "@/utils/formatTime";
import { Text } from "@/components/common/ThemedText"; // updated

interface UpcomingRideDetailsModalProps {
  ride: {
    pickup: any;
    dropoff: any;
    departureTime: number;
    price: string;
  };
  visible: boolean;
  onClose: () => void;
  onContactDriver: () => void;
  onCancel: () => void;
  onComplete: () => void;
  isPastRide: boolean;
}

/*
    UpcomingRideDetailsModal
    Modal component for viewing upcoming ride details
*/
const UpcomingRideDetailsModal = ({
  ride,
  visible,
  onClose,
  onContactDriver,
  onCancel,
  onComplete,
  isPastRide,
}: UpcomingRideDetailsModalProps) => {
  const { isDarkMode } = useTheme();

  /* 
    Note: Styling and class names are derived from Tailwind CSS docs
    https://tailwindcss.com/docs/
    Additional design elements have been generated using Figma -> React Native (Tailwind)
    https://www.figma.com/community/plugin/821138713091291738/figma-react-native
    https://www.figma.com/community/plugin/1283055580669946018/tailwind-react-code-generator-by-pagesloft
  */
  return (
    <Modal visible={visible} animationType="slide" onRequestClose={onClose}>
      <View className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-white"}`}>
        <View className="h-1/3">
          <Map pickup={ride.pickup} dropoff={ride.dropoff} />
          <TouchableOpacity
            onPress={onClose}
            className={`absolute top-12 left-4 z-10 p-2 rounded-full ${
              isDarkMode ? "bg-slate-800" : "bg-white"
            }`}
          >
            <FontAwesome5
              name={icons.backArrow}
              size={24}
              color={isDarkMode ? "#FFF" : "#000"}
            />
          </TouchableOpacity>
        </View>

        <View className="p-5 flex-1">
          {/* Removed inline dark mode text colors */}
          <Text className="text-2xl font-JakartaBold mt-8 mb-4">Ride Details</Text>

          <View
            className={`p-4 rounded-xl mb-4 ${
              isDarkMode ? "bg-slate-800" : "bg-gray-50"
            }`}
          >
            <View className="mb-3">
              <Text>From</Text>
              <Text className="font-JakartaMedium">{ride.pickup.name}</Text>
            </View>
            <View className="mb-3">
              <Text>To</Text>
              <Text className="font-JakartaMedium">{ride.dropoff.name}</Text>
            </View>
            <View className="mb-3">
              <Text>Departure</Text>
              <Text className="font-JakartaMedium">{formatTimestamp(ride.departureTime)}</Text>
            </View>
            <View>
              <Text>Price</Text>
              <Text className="font-JakartaMedium">{ride.price}</Text>
            </View>
          </View>

          <View className="flex-row gap-4 mt-auto">
            <TouchableOpacity
              onPress={onContactDriver}
              className="flex-1 bg-blue-600 p-4 rounded-xl"
            >
              <Text className="text-white text-center font-JakartaBold">
                Contact Driver
              </Text>
            </TouchableOpacity>

            {isPastRide ? (
              <TouchableOpacity
                onPress={onComplete}
                className="flex-1 bg-green-600 p-4 rounded-xl"
              >
                <Text className="text-white text-center font-JakartaBold">
                  Confirm Completion
                </Text>
              </TouchableOpacity>
            ) : (
              <TouchableOpacity
                onPress={onCancel}
                className="flex-1 bg-red-600 p-4 rounded-xl"
              >
                <Text className="text-white text-center font-JakartaBold">
                  Cancel Ride
                </Text>
              </TouchableOpacity>
            )}
          </View>
        </View>
      </View>
    </Modal>
  );
};

export default UpcomingRideDetailsModal;
