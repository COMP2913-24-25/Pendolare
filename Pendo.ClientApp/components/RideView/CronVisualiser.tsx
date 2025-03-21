import React, { useMemo } from "react";
import { View, Text } from "react-native";
import { FontAwesome5 } from "@expo/vector-icons";
import cronParser from "cron-parser";

interface CronVisualizerProps {
  cron: string; // CRON expression (e.g., "0 9 * * 1,3,5")
  endDate: Date; // End date (ISO string)
  isDarkMode: boolean;
}

const dayMap: { [key: string]: string } = {
  "0": "Sunday",
  "1": "Monday",
  "2": "Tuesday",
  "3": "Wednesday",
  "4": "Thursday",
  "5": "Friday",
  "6": "Saturday",
};

const CronVisualizer: React.FC<CronVisualizerProps> = ({ cron, endDate, isDarkMode }) => {
  const humanReadable = useMemo(() => {
    try {
      const interval = cronParser.parse(cron);
      const nextDate = interval.next().toDate();

      const parts = cron.split(" ");
      const time = nextDate.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      const days = parts[4].split(",").map((d) => dayMap[d.trim()] || "").join(", ");
      
      let frequency = "Weekly"; // Default
      if (parts[2] !== "*") frequency = "Monthly"; // Runs on specific day of the month
      else if (parts[4].includes(",")) frequency = "Weekly"; // Multiple days
      else if (parts[4].match(/(0|1|2|3|4|5|6)/)) frequency = "Fortnightly"; // Every 2 weeks

      return `${frequency}, ${days ? `on ${days}` : "every day"} at ${time}`;
    } catch (error) {
      return "Invalid schedule";
    }
  }, [cron]);

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