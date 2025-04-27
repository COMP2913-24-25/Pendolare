import { GestureHandlerRootView } from "react-native-gesture-handler";
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
import ThemedView from "@/components/common/ThemedView";

SplashScreen.preventAutoHideAsync();

const logLevel = process.env.EXPO_PUBLIC_LOG_LEVEL || "info";

console.log("Log level set to:", logLevel);

switch (logLevel) {
  case "info":
    console.debug = () => {};
    break;
  case "warn":
    console.debug = () => {};
    console.info = () => {};
    console.log = () => {};
    break;
  case "error":
    console.debug = () => {};
    console.info = () => {};
    console.log = () => {};
    console.warn = () => {};
    break;
}

const publishableKey = process.env.EXPO_PUBLIC_PUBLISH_KEY;

const Header = ({ className }: { className?: string }) => {
  return (
    <ThemedView className={`h-14 ${className}`}  />
  );
};

function AppLayout() {
  const { isDarkMode } = useTheme();

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
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
          }}
        >
          <Stack.Screen name="index" options={{ headerShown: false }}/>
          <Stack.Screen name="auth" options={{ headerShown: false }}/>
          <Stack.Screen name="home" options={{ headerShown: false }}/>
        </Stack>
      </View>
    </GestureHandlerRootView>
  );
}

/*
  RootLayout
  Main layout for the app
*/
export default function RootLayout() {

  const { isDarkMode } = useTheme();

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
              <Header className={isDarkMode ? "bg-slate-900" : "bg-general-500"}/>
              <AppLayout />
            </ClerkLoaded>
          </ClerkProvider>
        </AuthProvider>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}
