import { Redirect } from "expo-router";
import { View } from "react-native";

import { useTheme } from "@/context/ThemeContext";

export default function Index() {
  const { isDarkMode } = useTheme();

  // Add console.log for debugging
  console.log("Index rendering, isDarkMode:", isDarkMode);

  // Return just the Redirect without wrapping View
  return <Redirect href="/auth/sign-in" />;
}
