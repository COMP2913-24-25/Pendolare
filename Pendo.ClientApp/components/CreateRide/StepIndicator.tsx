import * as React from "react";
import { View } from "react-native";
import { Text } from "@/components/common/ThemedText";

interface StepIndicatorProps {
  currentStep: number;
}

const StepIndicator = ({ currentStep }: StepIndicatorProps) => {
  return (
    <View className="flex-row items-center justify-between mb-8 px-4 relative">
      <View
        className="absolute top-4 h-[2px] bg-gray-300"
        style={{
          left: "15%",
          right: "15%",
          zIndex: 1,
        }}
      />
      {[1, 2, 3, 4].map((stepNumber) => (
        <View key={stepNumber} className="flex-row items-center z-10">
          <View
            className={`w-8 h-8 rounded-full ${
              currentStep >= stepNumber ? "bg-blue-600" : "bg-gray-300"
            } items-center justify-center`}
          >
            <Text className="text-white font-JakartaBold">{stepNumber}</Text>
          </View>
        </View>
      ))}
    </View>
  );
};

export default StepIndicator;
