import React, { useMemo } from "react";
import { View, Text } from "react-native";
import { FontAwesome5 } from "@expo/vector-icons";
import { toHumanReadable } from "@/utils/cronTools";

interface CronVisualizerProps {
  cron: string; // CRON expression (e.g., "0 9 * * 1,3,5")
  endDate: Date;
  isDarkMode: boolean;
}

const CronVisualizer = ({ cron, endDate, isDarkMode } : CronVisualizerProps) => {
  const humanReadable = useMemo(() => {return toHumanReadable(cron)}, [cron]);

  console.log(humanReadable);

  return (
    <View className={`items-center p-2 rounded-lg ${isDarkMode ? "bg-slate-500" : "bg-slate-100"} shadow-sm`}>
      <View className="flex-row items-center mb-2">
        <FontAwesome5
          name="calendar-alt"
          size={16}
          color={isDarkMode ? "#FFF" : "#666"}
          style={{ marginRight: 8 }}
        />
        <Text className={`text-md font-JakartaBold ${isDarkMode ? "text-white" : "text-black"}`}>
          Recurring Journey
        </Text>
      </View>
      <Text className={`text-gray-500 ${isDarkMode ? "text-gray-300" : "text-gray-600"}`}>
        {humanReadable}
      </Text>
      <Text className={`text-gray-500 ${isDarkMode ? "text-gray-300" : "text-gray-600"}`}>
        Until {new Date(endDate).toLocaleDateString()}
      </Text>
    </View>
  );
};

export default CronVisualizer;