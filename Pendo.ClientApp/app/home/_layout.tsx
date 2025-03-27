import { Stack } from "expo-router";

/*
  Home Layout
  Layout for the home screens
  Contains the tabs and chat screens
*/
export default function HomeLayout() {
  return (
    <Stack
      screenOptions={{
        headerShown: false,
        animation: "slide_from_right",
      }}
    >
      <Stack.Screen name="tabs" />
      <Stack.Screen
        name="chat/[id]"
        options={{
          presentation: "card",
          animation: "slide_from_right",
        }}
      />
      <Stack.Screen
        name="settings"
        options={{
          presentation: "card",
          animation: "slide_from_right",
        }}
      />
    </Stack>
  );
}
