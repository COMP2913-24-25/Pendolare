import { router, useSegments, useRootNavigationState } from "expo-router";
import React, { createContext, useContext, useEffect, useState } from "react";

import {
  isAuthenticated,
  logout as logoutService,
  getUserObject,
  getUser as apiGetUser,
  setUserData,
} from "@/services/authService";

type UserData = {
  firstName: string | null;
  lastName: string | null;
  rating: string | null;
};

type AuthContextType = {
  isLoggedIn: boolean;
  setIsLoggedIn: (value: boolean) => void;
  logout: () => Promise<void>;
  loading: boolean;
  userData: UserData;
  refreshUserData: () => Promise<void>;
  updateUserData: (firstName?: string, lastName?: string, rating?: string) => Promise<void>;
};

const AuthContext = createContext<AuthContextType>({
  isLoggedIn: false,
  setIsLoggedIn: () => {},
  logout: async () => {},
  loading: true,
  userData: { firstName: null, lastName: null, rating: null },
  refreshUserData: async () => {},
  updateUserData: async () => {},
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
  const [userData, setUserDataState] = useState<UserData>({ 
    firstName: null, 
    lastName: null, 
    rating: null 
  });
  const segments = useSegments();
  const navigationState = useRootNavigationState();

  // Fetch user data from storage
  const refreshUserData = async () => {
    try {
      if (isLoggedIn) {
        await apiGetUser();
        const data = await getUserObject();
        setUserDataState(data);
      }
    } catch (error) {
      console.error("Error refreshing user data:", error);
    }
  };

  // Update user data in context and storage
  const updateUserData = async (firstName?: string, lastName?: string, rating?: string) => {
    try {
      // Update storage using the same function signature
      await setUserData(firstName, lastName, rating);
      
      // Update local state with renamed setter
      setUserDataState(prevData => ({
        firstName: firstName !== undefined ? firstName : prevData.firstName,
        lastName: lastName !== undefined ? lastName : prevData.lastName,
        rating: rating !== undefined ? rating : prevData.rating,
      }));
    } catch (error) {
      console.error("Error updating user data:", error);
    }
  };

  /*
    Check authentication status on app start
  */
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const authenticated = await isAuthenticated();
        console.log("Auth status:", authenticated);
        setIsLoggedIn(authenticated);
        
        if (authenticated) {
          await refreshUserData();
        }
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
    setUserDataState({ firstName: null, lastName: null, rating: null });
    router.replace("/auth/signin");
  };

  return (
    <AuthContext.Provider
      value={{ 
        isLoggedIn, 
        setIsLoggedIn, 
        logout, 
        loading,
        userData,
        refreshUserData,
        updateUserData
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
