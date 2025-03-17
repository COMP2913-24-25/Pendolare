import { FontAwesome5 } from "@expo/vector-icons";
import { View } from "react-native";

import Map from "../Map/Map";

import { Text } from "@/components/common/ThemedText";
import { icons } from "@/constants";

interface Location {
  name: string;
  latitude: number;
  longitude: number;
}

interface ConfirmationStepProps {
  isDarkMode: boolean;
  pickup: Location | null;
  dropoff: Location | null;
  cost: string;
  seats: string;
  date: Date;
}

/*
  ConfirmationStep
  Step for confirming ride details
*/
const ConfirmationStep = ({
  isDarkMode,
  pickup,
  dropoff,
  cost,
  seats,
  date,
}: ConfirmationStepProps) => {
  return (
    <View className="flex-1">
      <View
        className={`h-[200px] rounded-xl shadow-sm mb-5 overflow-hidden ${
          isDarkMode ? "bg-slate-800" : "bg-white"
        }`}
      >
        <Map pickup={pickup} dropoff={dropoff} />
      </View>

      {/* Confirmation Details */}
      <View
        className={`p-5 rounded-xl shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
      >
        <Text className="text-lg font-JakartaBold mb-4">
          Confirm Ride Details
        </Text>

        <View className="mb-3">
          <View className="flex-row items-center">
            <FontAwesome5
              name={icons.marker}
              size={16}
              style={{ marginRight: 8 }}
            />
            <Text className="text-gray-500">
              From
            </Text>
          </View>
          <Text className="text-base ml-6">{pickup?.name}</Text>
        </View>

        <View className="mb-3">
          <View className="flex-row items-center">
            <FontAwesome5
              name={icons.target}
              size={16}
              style={{ marginRight: 8 }}
            />
            <Text className="text-gray-500">
              To
            </Text>
          </View>
          <Text className="text-base ml-6">{dropoff?.name}</Text>
        </View>

        <View className="mb-3">
          <View className="flex-row items-center">
            <FontAwesome5
              name="pound-sign"
              size={16}
              style={{ marginRight: 8 }}
            />
            <Text className="text-gray-500">
              Price per Seat
            </Text>
          </View>
          <Text className="text-base ml-6">£{cost}</Text>
        </View>

        <View className="mb-3">
          <View className="flex-row items-center">
            <FontAwesome5
              name="users"
              size={16}
              style={{ marginRight: 8 }}
            />
            <Text className="text-gray-500">
              Available Seats
            </Text>
          </View>
          <Text className="text-base ml-6">{seats}</Text>
        </View>

        <View className="mb-3">
          <View className="flex-row items-center">
            <FontAwesome5
              name="clock"
              size={16}
              style={{ marginRight: 8 }}
            />
            <Text className="text-gray-500">
              Date & Time
            </Text>
          </View>
          <Text className="text-base ml-6">{date.toLocaleString()}</Text>
        </View>
      </View>
    </View>
  );
};

export default ConfirmationStep;
