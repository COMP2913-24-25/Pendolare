import { Redirect } from "expo-router";
import { View, ActivityIndicator } from "react-native";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";

/*
  Index
  Redirects users based on auth state
  Redirects to onboarding if logged in (for now)
  Shows a loading indicator while checking auth state
*/
export default function Index() {
  const { isLoggedIn, loading } = useAuth();
  const { isDarkMode } = useTheme();

  // Show a loading screen while checking auth state
  if (loading) {
    return (
      <View className="flex-1 items-center justify-center">
        <ActivityIndicator 
          size="large" 
          color={isDarkMode ? "#FFFFFF" : "#0066CC"} 
          className="mb-2"
        />
      </View>
    );
  }

  // Redirect based on auth state
  return isLoggedIn ? (
    <Redirect href="/auth/onboarding" />
  ) : (
    <Redirect href="/auth/sign-in" />
  );
}