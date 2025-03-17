import { Redirect } from "expo-router";
import { View } from "react-native";

import { useAuth } from "@/context/AuthContext";

/*
  Index
  Redirects users based on auth state
  Redirects to onboarding if logged in (for now)
*/
export default function Index() {
  const { isLoggedIn, loading } = useAuth();

  // Show a blank screen while loading
  if (loading) {
    return null;
  }

  // Redirect based on auth state
  return isLoggedIn ? (
    <Redirect href="/auth/onboarding" />
  ) : (
    <Redirect href="/auth/sign-in" />
  );
}
