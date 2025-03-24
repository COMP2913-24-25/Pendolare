import React from "react";
import { View } from "react-native";
import { FontAwesome5 } from "@expo/vector-icons";
import { Text } from "@/components/common/ThemedText";

interface StatusBadgeProps {
  statusText: string;
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ statusText }) => {
  let badgeStyle = "bg-gray-100";
  let textStyle = "text-gray-800";
  let iconName: string | null = null;
  let iconColor = "#6B7280";

  switch (statusText) {
    case "Pending":
      badgeStyle = "bg-yellow-100";
      textStyle = "text-yellow-800";
      iconName = "clock";
      iconColor = "#F59E0B";
      break;

    case "Confirmed":
      badgeStyle = "bg-green-100";
      textStyle = "text-green-800";
      iconName = "check-circle";
      iconColor = "#10B981";
      break;

    case "Cancelled":
      badgeStyle = "bg-red-100";
      textStyle = "text-red-800";
      iconName = "times-circle";
      iconColor = "#EF4444";
      break;

    case "PendingCompletion":
        statusText = "Pending Completion";
        badgeStyle = "bg-orange-100";
        textStyle = "text-orange-800";
        iconName = "clock";
        iconColor = "#F59E0B";
        break;

    case "NotCompleted":
        statusText = "Not Completed";
        badgeStyle = "bg-red-100";
        textStyle = "text-red-800";
        iconName = "times-circle";
        iconColor = "#EF4444";
        break;

    case "Completed":
        badgeStyle = "bg-dark-800";
        textStyle = "text-light-800";
        iconName = "check-circle";
        iconColor = "#10B981";
        break;

      break;
    default:
      break;
  }

  return (
    <View
      className={`flex-row items-center px-2 py-1 rounded-full ${badgeStyle}`}
    >
      {iconName && (
        <FontAwesome5
          name={iconName}
          size={20}
          color={iconColor}
          style={{ marginRight: 4 }}
        />
      )}
      <Text className={`font-JakartaMedium text-md ${textStyle}`}>
        {statusText}
      </Text>
    </View>
  );
};

export default StatusBadge;