import * as React from "react";
import { SafeAreaView, SafeAreaViewProps } from "react-native-safe-area-context";
import { useTheme } from "@/context/ThemeContext";

const ThemedSafeAreaView = (props: SafeAreaViewProps) => {
  const { isDarkMode } = useTheme();
  return (
    <SafeAreaView 
      {...props} 
      style={[{ backgroundColor: isDarkMode ? "#1E293B" : "#F3F4F6" }, props.style]} 
    />
  );
};

export default ThemedSafeAreaView;
