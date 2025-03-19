import { TouchableOpacity, View } from "react-native";
import { FontAwesome5 } from "@expo/vector-icons";
import { useTheme } from "@/context/ThemeContext";


interface RatingStarsProps {
  rating: number;
  setRating: (rating: number) => void;
  size?: number;
}

const RatingStars = ({ rating, setRating, size = 20 }: RatingStarsProps) => {
  // WIP
  const starColor = "#FFC107";
  return (
    <View className="flex-row">
      {[1, 2, 3, 4, 5].map((star) => (
        <TouchableOpacity key={star} onPress={() => setRating(star)}>
          <FontAwesome5
            name={star <= rating ? "star" : "star-o"}
            size={size}
            color={starColor}
          />
        </TouchableOpacity>
      ))}
    </View>
  );
};

export default RatingStars;
