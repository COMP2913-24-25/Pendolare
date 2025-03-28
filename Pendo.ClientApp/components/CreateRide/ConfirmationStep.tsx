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
  bootHeight: string;
  bootWidth: string;
  isCommuter?: boolean;
  selectedDiscount?: any;
}

/*
  ConfirmationStep
  Step for confirming ride details including boot dimensions
*/
const ConfirmationStep = ({
  isDarkMode,
  pickup,
  dropoff,
  cost,
  seats,
  date,
  bootHeight,
  bootWidth,
  isCommuter = false,
  selectedDiscount = null,
}: ConfirmationStepProps) => {
  // Calculate discounted price if a discount is selected
  const originalPrice = parseFloat(cost);
  const discountPercentage = selectedDiscount?.percentage || 0;
  const discountedPrice = originalPrice * (1 - discountPercentage);
  const hasDiscount = discountPercentage > 0;

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
          {hasDiscount ? (
            <View className="ml-6">
              <View className="flex-row items-center">
                <Text className="text-base line-through text-gray-500 mr-2">£{originalPrice.toFixed(2)}</Text>
                <Text className="text-base text-green-600">£{discountedPrice.toFixed(2)}</Text>
              </View>
              <Text className="text-xs text-green-600">
                {discountPercentage * 100}% discount applied
              </Text>
            </View>
          ) : (
            <Text className="text-base ml-6">£{cost}</Text>
          )}
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
              name="truck"
              size={16}
              style={{ marginRight: 8 }}
            />
            <Text className="text-gray-500">
              Boot Dimensions
            </Text>
          </View>
          <Text className="text-base ml-6">
            {bootHeight || bootWidth
              ? `${bootHeight || "N/A"}cm x ${bootWidth || "N/A"}cm`
              : "N/A"}
          </Text>
        </View>

        <View className="mb-3">
          <View className="flex-row items-center">
            <FontAwesome5
              name="clock"
              size={16}
              style={{ marginRight: 8 }}
            />
            <Text className="text-gray-500">
              {isCommuter ? "Start Time" : "Date & Time"}
            </Text>
          </View>
          <Text className="text-base ml-6">{date.toLocaleString()}</Text>
        </View>

        {isCommuter && selectedDiscount && selectedDiscount.value && (
          <View className="mb-3">
            <View className="flex-row items-center">
              <FontAwesome5
                name="tag"
                size={16}
                style={{ marginRight: 8 }}
              />
              <Text className="text-gray-500">
                Discount
              </Text>
            </View>
            <Text className="text-base ml-6">{selectedDiscount.label}</Text>
          </View>
        )}

        {isCommuter && (
          <View className="mt-2 p-2 bg-blue-100 rounded-lg">
            <Text className="text-blue-800 text-center">
              This is a commuter journey. It will repeat according to your selected schedule.
            </Text>
          </View>
        )}
      </View>
    </View>
  );
};

export default ConfirmationStep;
