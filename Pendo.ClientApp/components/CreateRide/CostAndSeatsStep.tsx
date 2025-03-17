import { View, TextInput } from "react-native";
import { Text } from "@/components/common/ThemedText";

interface CostAndSeatsStepProps {
  isDarkMode: boolean;
  cost: string;
  seats: string;
  setCost: (value: string) => void;
  setSeats: (value: string) => void;
}


/*
  CostAndSeatsStep
  Step for entering cost and seats
*/
const CostAndSeatsStep = ({
  isDarkMode,
  cost,
  seats,
  setCost,
  setSeats,
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
    </View>
  );
};

export default CostAndSeatsStep;
