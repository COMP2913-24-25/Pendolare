import { FontAwesome5 } from "@expo/vector-icons";
import React from "react";
import { View, TouchableOpacity } from "react-native";

import { icons } from "@/constants";

interface RatingStarsProps {
  rating: number;
  setRating: (rating: number) => void;
  size?: number;
}

const RatingStars = ({ rating, setRating, size = 24 }: RatingStarsProps) => {
  return (
    <View className="flex-row justify-center">
      {[1, 2, 3, 4, 5].map((star) => (
        <TouchableOpacity
          key={star}
          onPress={() => setRating(star)}
          className="mx-1"
        >
          <FontAwesome5
            name={icons.star}
            size={size}
            color={star <= rating ? "#F59E0B" : "#D1D5DB"}
          />
        </TouchableOpacity>
      ))}
    </View>
  );
};

export default RatingStars;
