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
  Redirects to authentication if not logged in
  Redirects to home if logged in
*/
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const segments = useSegments();
  const navigationState = useRootNavigationState();

  /*
    Check authentication status on app start
  */
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const authenticated = await isAuthenticated();
        console.log("Auth status:", authenticated);
        setIsLoggedIn(authenticated);
      } catch (error) {
        console.error("Error checking authentication status:", error);
      } finally {
        setLoading(false);
      }
    };

    if (navigationState?.key) {
      checkAuthStatus();
    }
  }, [navigationState?.key]);

  /*
    Redirect based on authentication status
  */
  useEffect(() => {
    if (loading || !navigationState?.key) return;
    const segmentsArr = segments as string[];

    const inAuthGroup = segmentsArr[0] === "auth";
    const isOnboarding = segmentsArr.length > 1 && segmentsArr[1] === "onboarding";

    if (!isLoggedIn && !inAuthGroup) {
      console.log("Redirecting to authentication");
      router.replace("/auth/signin");
    } else if (isLoggedIn && inAuthGroup && !isOnboarding) {
      // Redirect to home if logged in and not undergoing onboarding
      if (segmentsArr.length > 1 && segmentsArr[1] === "signin") {
        console.log("Redirecting to onboarding");
        router.replace("/auth/onboarding");
      }
    }
  }, [isLoggedIn, loading, segments, navigationState?.key]);

  /*
    Logout the user
  */
  const logout = async () => {
    await logoutService();
    setIsLoggedIn(false);
    router.replace("/auth/signin");
  };

  return (
    <AuthContext.Provider
      value={{ isLoggedIn, setIsLoggedIn, logout, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
}
