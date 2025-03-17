import { Stack } from "expo-router";

/*
  Layout
  Layout for the auth screens
  Contains the sign-in, sign-up, and onboarding screens
*/
const Layout = () => {
  return (
    <Stack initialRouteName="sign-in">
      <Stack.Screen name="sign-in" options={{ headerShown: false }} />
      <Stack.Screen name="onboarding" options={{ headerShown: false, gestureEnabled: false }} />
    </Stack>
  );
};

export default Layout;
