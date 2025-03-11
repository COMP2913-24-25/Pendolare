import React from "react";
import { Text as RNText, TextProps } from "react-native";

import { useTheme } from "@/context/ThemeContext";

/*
  Text
  Themed text component that uses the current theme
*/
export function Text({ style, ...props }: TextProps) {
  const { isDarkMode } = useTheme();
  return (
    <RNText
      style={[{ color: isDarkMode ? "#FFFFFF" : "#000000" }, style]}
      {...props}
    />
  );
}
