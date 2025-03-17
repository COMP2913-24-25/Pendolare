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

/* 
  AuthProvider
  Provides the auth context to the app
  Redirects to auth if not logged in
  Redirects to home if logged in
*/
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const segments = useSegments();
  const navigationState = useRootNavigationState();

  // Check auth status on app load
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

  useEffect(() => {
    if (loading || !navigationState?.key) return;

    const inAuthGroup = segments[0] === "auth";
    const isOnboarding = segments.length > 1 && segments[1] === "onboarding";

    if (!isLoggedIn && !inAuthGroup) {
      // Redirect to auth if not logged in
      console.log("Redirecting to auth");
      router.replace("/auth/sign-in");
    } else if (isLoggedIn && inAuthGroup && !isOnboarding) {
      // If user is logged in and in auth group but NOT in onboarding,
      // we need to check if they should see onboarding first
      
      // For now, always show onboarding after login
      if (segments.length > 1 && segments[1] === "sign-in") {
        console.log("Redirecting to onboarding");
        router.replace("/auth/onboarding");
      }
    }
  }, [isLoggedIn, loading, segments, navigationState?.key]);

  // Logout user
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
