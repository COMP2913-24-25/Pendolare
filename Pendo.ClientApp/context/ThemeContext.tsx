import AsyncStorage from "@react-native-async-storage/async-storage";
import React, { createContext, useContext, useState, useEffect } from "react";
import { useColorScheme } from "react-native";

type ThemeMode = 'light' | 'dark' | 'system';

type ThemeContextType = {
  isDarkMode: boolean;
  themeMode: ThemeMode;
  setTheme: (mode: ThemeMode) => void;
};

const ThemeContext = createContext<ThemeContextType>({
  isDarkMode: false,
  themeMode: 'light',
  setTheme: () => {},
});

/**
 * ThemeProvider
 * Provides the theme context to the app.
 * Loads and initialises the theme preference from AsyncStorage.
 */
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [themeMode, setThemeMode] = useState<ThemeMode>('light');
  const [isLoaded, setIsLoaded] = useState(false);
  const systemColorScheme = useColorScheme();
  
  // Compute isDarkMode based on themeMode and system preference
  const isDarkMode = 
    themeMode === 'dark' || 
    (themeMode === 'system' && systemColorScheme === 'dark');

  // Load theme preference on app load
  useEffect(() => {
    loadThemePreference();
  }, []);

  // Listen for system theme changes when in system mode
  useEffect(() => {
    if (themeMode === 'system') {
      // No need to update state, isDarkMode will be recalculated
    }
  }, [systemColorScheme]);

  /*
    Load the theme preference from AsyncStorage
    Set themeMode to the saved value
  */
  const loadThemePreference = async () => {
    try {
      const savedTheme = await AsyncStorage.getItem("themePreference");
      if (savedTheme !== null) {
        setThemeMode(savedTheme as ThemeMode);
      }
    } catch (error) {
      console.error("Error loading theme preference:", error);
    } finally {
      setIsLoaded(true);
    }
  };

  /*
    Set the theme preference
    Save the value to AsyncStorage
  */
  const setTheme = async (mode: ThemeMode) => {
    try {
      setThemeMode(mode);
      await AsyncStorage.setItem("themePreference", mode);
    } catch (error) {
      console.error("Error saving theme preference:", error);
    }
  };

  // For backward compatibility
  const toggleTheme = () => {
    setTheme(isDarkMode ? 'light' : 'dark');
  };

  if (!isLoaded) {
    return null; // Show loading spinner or splash screen
  }

  return (
    <ThemeContext.Provider value={{ isDarkMode, themeMode, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
