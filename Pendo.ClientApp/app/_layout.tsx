import { ClerkLoaded, ClerkProvider } from "@clerk/clerk-expo";
import { StatusBar } from "expo-status-bar";
import { useFonts } from "expo-font";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { useEffect } from "react";
import { View, Platform } from "react-native";
import { SafeAreaProvider } from "react-native-safe-area-context";

import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider, useTheme } from "@/context/ThemeContext";

SplashScreen.preventAutoHideAsync();

const publishableKey = process.env.EXPO_PUBLIC_PUBLISH_KEY;

function AppLayout() {
  const { isDarkMode } = useTheme();
  
  return (
    <View style={{ flex: 1, backgroundColor: isDarkMode ? '#121212' : '#ffffff' }}>
      {/* StatusBar styling based on theme */}
      <StatusBar 
        style={isDarkMode ? "light" : "dark"} 
        backgroundColor={isDarkMode ? "bg-slate-900" : "bg-general-500"}
        translucent={true}
      />
      
      <Stack 
        screenOptions={{
          headerStyle: {
            backgroundColor: isDarkMode ? '#121212' : '#ffffff',
          },
          headerTintColor: isDarkMode ? '#ffffff' : '#000000',
          contentStyle: {
            backgroundColor: isDarkMode ? '#121212' : '#f5f5f5',
          },
          // Add top padding to account for translucent status bar
        }}
      >
        <Stack.Screen name="index" />
        <Stack.Screen name="auth" />
        <Stack.Screen name="home" />
      </Stack>
    </View>
  );
}

/*
  RootLayout
  Main layout for the app
*/
export default function RootLayout() {
  const [loaded] = useFonts({
    "Jakarta-Bold": require("../assets/fonts/PlusJakartaSans-Bold.ttf"),
    "Jakarta-ExtraBold": require("../assets/fonts/PlusJakartaSans-ExtraBold.ttf"),
    "Jakarta-ExtraLight": require("../assets/fonts/PlusJakartaSans-ExtraLight.ttf"),
    "Jakarta-Light": require("../assets/fonts/PlusJakartaSans-Light.ttf"),
    "Jakarta-Medium": require("../assets/fonts/PlusJakartaSans-Medium.ttf"),
    Jakarta: require("../assets/fonts/PlusJakartaSans-Regular.ttf"),
    "Jakarta-SemiBold": require("../assets/fonts/PlusJakartaSans-SemiBold.ttf"),
  });

  useEffect(() => {
    if (loaded) {
      SplashScreen.hideAsync();
    }
  }, [loaded]);

  if (!loaded) {
    return null;
  }

  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <AuthProvider>
          <ClerkProvider publishableKey={publishableKey as string}>
            <ClerkLoaded>
              <AppLayout />
            </ClerkLoaded>
          </ClerkProvider>
        </AuthProvider>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}
