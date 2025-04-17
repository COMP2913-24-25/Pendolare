import { View, TextInput } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { SeatSlider } from "./SeatsSlider";

interface CostAndSeatsStepProps {
  isDarkMode: boolean;
  cost: string;
  costValidationMessage: string | null;
  seats: string;
  setCost: (value: string) => void;
  setSeats: (value: string) => void;
  regPlate: string;
  setRegPlate: (value: string) => void;
  bootHeight: string;
  bootHeightValidationMessage: string | null;
  setBootHeight: (value: string) => void;
  bootWidth: string;
  bootWidthValidationMessage: string | null;
  setBootWidth: (value: string) => void;
}

/*
  CostAndSeatsStep
  Step for entering cost, seats, vehicle reg plate, and boot dimensions
*/
const CostAndSeatsStep = ({
  isDarkMode,
  cost,
  costValidationMessage,
  seats,
  setCost,
  setSeats,
  regPlate,
  setRegPlate,
  bootHeight,
  bootHeightValidationMessage,
  setBootHeight,
  bootWidth,
  bootWidthValidationMessage,
  setBootWidth,
}: CostAndSeatsStepProps) => {
  return (
    <View
      className={`p-5 rounded-xl shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
    >
      <View className="mb-4">
        <Text className="text-lg font-JakartaBold mb-2">Cost (£)</Text>
        <TextInput
          value={cost}
          onChangeText={setCost}
          keyboardType="numeric"
          returnKeyType="done"
          className={`h-[45px] border rounded-lg px-3 ${
            isDarkMode
              ? "bg-slate-700 border-slate-600 text-white"
              : "bg-white border-slate-200 text-black"
          }`}
          placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
          placeholder="Enter cost per seat"
        />
        {costValidationMessage !== null && (
          <Text className="mt-1 text-sm text-red-500">
            {costValidationMessage}
          </Text>
        )}
      </View>

      <SeatSlider
        seats={seats}
        setSeats={setSeats}
        minSeats={1}
        maxSeats={7}
        isDarkMode={isDarkMode}
      />

      <View className="mb-4">
        <Text className="text-lg font-JakartaBold mb-2">Vehicle Registration Plate</Text>
        <TextInput
          value={regPlate}
          onChangeText={setRegPlate}
          autoCapitalize="characters"
          className={`h-[45px] border rounded-lg px-3 ${
            isDarkMode
              ? "bg-slate-700 border-slate-600 text-white"
              : "bg-white border-slate-200 text-black"
          }`}
          placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
          placeholder="Enter reg plate (e.g., AB12CDE)"
        />
      </View>

      <View className="mb-4">
        <Text className="text-lg font-JakartaBold mb-2">Boot Height</Text>
        <TextInput
          value={bootHeight}
          onChangeText={setBootHeight}
          keyboardType="number-pad"
          className={`h-[45px] border rounded-lg px-3 ${
            isDarkMode
              ? "bg-slate-700 border-slate-600 text-white"
              : "bg-white border-slate-200 text-black"
          }`}
          placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
          placeholder="Enter boot height (cm, optional)"
        />
        {bootHeightValidationMessage !== null && (
          <Text className="mt-1 text-sm text-red-500">
            {bootHeightValidationMessage}
          </Text>
        )}
      </View>
      <View className="mb-4">
        <Text className="text-lg font-JakartaBold mb-2">Boot Width</Text>
        <TextInput
          value={bootWidth}
          onChangeText={setBootWidth}
          keyboardType="number-pad"
          className={`h-[45px] border rounded-lg px-3 ${
            isDarkMode
              ? "bg-slate-700 border-slate-600 text-white"
              : "bg-white border-slate-200 text-black"
          }`}
          placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
          placeholder="Enter boot width (cm, optional)"
        />
        {bootWidthValidationMessage !== null && (
          <Text className="mt-1 text-sm text-red-500">
            {bootWidthValidationMessage}
          </Text>
        )}
      </View>
    </View>
  );
};

export default CostAndSeatsStep;
