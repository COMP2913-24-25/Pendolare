import { TouchableOpacity } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";

interface BookingCategoryProps {
  title: string;
  description: string;
  onPress: () => void;
  isSelected: boolean;
}

/*
  BookingCategory
  Category item for booking screen
*/
const BookingCategory = ({
  title,
  description,
  onPress,
  isSelected,
}: BookingCategoryProps) => {
  const { isDarkMode } = useTheme();

  return (
    <TouchableOpacity
      className={`p-4 mb-4 rounded-xl ${
        isSelected
          ? isDarkMode
            ? "bg-blue-900"
            : "bg-blue-100"
          : isDarkMode
            ? "bg-slate-800"
            : "bg-white"
      }`}
      onPress={onPress}
    >
      <Text
        className={`text-lg font-JakartaBold ${
          isSelected
            ? isDarkMode
              ? "text-blue-200"
              : "text-blue-600"
            : undefined
        }`}
      >
        {title}
      </Text>
      <Text>{description}</Text>
    </TouchableOpacity>
  );
};

export default BookingCategory;
