import { Stack } from "expo-router";

/*
  Layout
  Layout for the auth screens
  Contains the signin and onboarding screens
*/
const Layout = () => {
  return (
    <Stack initialRouteName="signin">
      <Stack.Screen name="signin" options={{ headerShown: false }} />
      <Stack.Screen name="onboarding" options={{ headerShown: false, gestureEnabled: false }} />
      <Stack.Screen name="newuser" options={{ headerShown: false }} />
    </Stack>
  );
};

export default Layout;
