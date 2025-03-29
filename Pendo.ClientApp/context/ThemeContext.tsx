import AsyncStorage from "@react-native-async-storage/async-storage";
import React, { createContext, useContext, useState, useEffect } from "react";

type ThemeContextType = {
  isDarkMode: boolean;
  toggleTheme: () => void;
};

const ThemeContext = createContext<ThemeContextType>({
  isDarkMode: false,
  toggleTheme: () => {},
});

/**
 * ThemeProvider
 * Provides the theme context to the app.
 * Loads and initialises the theme preference from AsyncStorage.
 */
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load theme preference on app load
  useEffect(() => {
    loadThemePreference();
  }, []);

  /*
    Load the theme preference from AsyncStorage
    Set isDarkMode to the saved value
  */
  const loadThemePreference = async () => {
    try {
      const savedTheme = await AsyncStorage.getItem("isDarkMode");
      if (savedTheme !== null) {
        setIsDarkMode(JSON.parse(savedTheme));
      }
    } catch (error) {
      console.error("Error loading theme preference:", error);
    } finally {
      setIsLoaded(true);
    }
  };

  /*
    Toggle the theme preference
    Save the new value to AsyncStorage
  */
  const toggleTheme = async () => {
    try {
      const newValue = !isDarkMode;
      setIsDarkMode(newValue);
      await AsyncStorage.setItem("isDarkMode", JSON.stringify(newValue));
    } catch (error) {
      console.error("Error saving theme preference:", error);
    }
  };

  if (!isLoaded) {
    return null; // Show loading spinner or splash screen
  }

  return (
    <ThemeContext.Provider value={{ isDarkMode, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
