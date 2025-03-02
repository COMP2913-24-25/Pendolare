import { Redirect } from "expo-router";
import { View } from "react-native";

import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";

export default function Index() {
  const { isDarkMode } = useTheme();
  const { isLoggedIn, loading } = useAuth();

  // Show a blank screen while loading
  if (loading) {
    return null;
  }

  // Redirect based on auth state
  return isLoggedIn ? (
    <Redirect href="/home/tabs/home" />
  ) : (
    <Redirect href="/auth/sign-in" />
  );
}
