import { router, useSegments, useRootNavigationState } from "expo-router";
import React, { createContext, useContext, useEffect, useState } from "react";

import {
  isAuthenticated,
  logout as logoutService,
} from "@/services/authService";

type AuthContextType = {
  isLoggedIn: boolean;
  setIsLoggedIn: (value: boolean) => void;
  logout: () => Promise<void>;
  loading: boolean;
};

const AuthContext = createContext<AuthContextType>({
  isLoggedIn: false,
  setIsLoggedIn: () => {},
  logout: async () => {},
  loading: true,
});

export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const segments = useSegments();
  const navigationState = useRootNavigationState();

  // Check authentication status on app load
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const authenticated = await isAuthenticated();
        console.log("Auth status:", authenticated);
        setIsLoggedIn(authenticated);
      } catch (error) {
        console.error("Error checking auth status:", error);
      } finally {
        setLoading(false);
      }
    };

    if (navigationState?.key) {
      checkAuthStatus();
    }
  }, [navigationState?.key]);

  // Handle routing based on auth state
  useEffect(() => {
    if (loading || !navigationState?.key) return;

    const inAuthGroup = segments[0] === "auth";

    if (!isLoggedIn && !inAuthGroup) {
      // Redirect to sign-in if not logged in
      console.log("Redirecting to auth");
      router.replace("/auth/sign-in");
    } else if (isLoggedIn && inAuthGroup) {
      // Redirect to home if already logged in
      console.log("Redirecting to home");
      router.replace("/home/tabs/home");
    }
  }, [isLoggedIn, loading, segments, navigationState?.key]);

  // Logout function
  const logout = async () => {
    await logoutService();
    setIsLoggedIn(false);
    router.replace("/auth/sign-in");
  };

  return (
    <AuthContext.Provider
      value={{ isLoggedIn, setIsLoggedIn, logout, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
}
