import { View, TextInput } from "react-native";
import { Text } from "@/components/common/ThemedText";

interface CostAndSeatsStepProps {
  isDarkMode: boolean;
  cost: string;
  seats: string;
  setCost: (value: string) => void;
  setSeats: (value: string) => void;
  regPlate: string;
  setRegPlate: (value: string) => void;
  bootHeight: string;
  setBootHeight: (value: string) => void;
  bootWidth: string;
  setBootWidth: (value: string) => void;
}

/*
  CostAndSeatsStep
  Step for entering cost, seats, vehicle reg plate, and boot dimensions
*/
const CostAndSeatsStep = ({
  isDarkMode,
  cost,
  seats,
  setCost,
  setSeats,
  regPlate,
  setRegPlate,
  bootHeight,
  setBootHeight,
  bootWidth,
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
          className={`h-[45px] border rounded-lg px-3 ${
            isDarkMode
              ? "bg-slate-700 border-slate-600 text-white"
              : "bg-white border-slate-200 text-black"
          }`}
          placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
          placeholder="Enter cost per seat"
        />
      </View>

      <View className="mb-4">
        <Text className="text-lg font-JakartaBold mb-2">Available Seats</Text>
        <TextInput
          value={seats}
          onChangeText={setSeats}
          keyboardType="numeric"
          className={`h-[45px] border rounded-lg px-3 ${
            isDarkMode
              ? "bg-slate-700 border-slate-600 text-white"
              : "bg-white border-slate-200 text-black"
          }`}
          placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
          placeholder="Enter number of seats"
        />
      </View>

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
          keyboardType="numeric"
          className={`h-[45px] border rounded-lg px-3 ${
            isDarkMode
              ? "bg-slate-700 border-slate-600 text-white"
              : "bg-white border-slate-200 text-black"
          }`}
          placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
          placeholder="Enter boot height (optional)"
        />
      </View>
      <View className="mb-4">
        <Text className="text-lg font-JakartaBold mb-2">Boot Width</Text>
        <TextInput
          value={bootWidth}
          onChangeText={setBootWidth}
          keyboardType="numeric"
          className={`h-[45px] border rounded-lg px-3 ${
            isDarkMode
              ? "bg-slate-700 border-slate-600 text-white"
              : "bg-white border-slate-200 text-black"
          }`}
          placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
          placeholder="Enter boot width (optional)"
        />
      </View>
    </View>
  );
};

export default CostAndSeatsStep;
