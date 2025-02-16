import { TouchableOpacity, Text } from "react-native";

interface BookingCategoryProps {
  title: string;
  description: string;
  onPress: () => void;
  isSelected: boolean;
}

const BookingCategory = ({
  title,
  description,
  onPress,
  isSelected,
}: BookingCategoryProps) => (
  <TouchableOpacity
    onPress={onPress}
    className={`p-5 rounded-xl mb-4 ${isSelected ? "bg-blue-600" : "bg-white"}`}
  >
    <Text
      className={`text-xl font-JakartaBold ${isSelected ? "text-white" : "text-black"}`}
    >
      {title}
    </Text>
    <Text className={`mt-2 ${isSelected ? "text-white" : "text-gray-600"}`}>
      {description}
    </Text>
  </TouchableOpacity>
);

export default BookingCategory;
