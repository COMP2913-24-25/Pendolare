import * as React from "react";
import { View, ViewProps } from "react-native";
import { useTheme } from "@/context/ThemeContext";

interface ThemedViewProps extends ViewProps {
  lightStyle?: string;
  darkStyle?: string;
}

const ThemedView = ({ lightStyle = "bg-white", darkStyle = "bg-slate-800", style, ...props }: ThemedViewProps) => {
  const { isDarkMode } = useTheme();

  const themeClass = isDarkMode ? darkStyle : lightStyle;
  return <View {...props} style={[{ }, style]} className={`${themeClass} ${props.className || ""}`} />;
};

export default ThemedView;
