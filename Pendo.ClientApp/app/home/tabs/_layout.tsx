import { FontAwesome5 } from "@expo/vector-icons";
import { Tabs } from "expo-router";
import { View } from "react-native";

import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";

/* Layout & Design From: https://docs.expo.dev/router/advanced/tabs/ */

{
  /* Custom Tab Icon Component */
}
const TabIcon = ({ name, focused }: { name: string; focused: boolean }) => (
  <View
    style={{
      width: 60,
      height: 50,
      justifyContent: "center",
      alignItems: "center",
      backgroundColor: "transparent",
    }}
  >
    <View
      style={{
        width: 40,
        height: 40,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: focused ? "#2563EB" : "transparent",
        borderRadius: 20,
      }}
    >
      <FontAwesome5
        name={name}
        size={22}
        color={focused ? "#FFFFFF" : "#AAAAAA"}
      />
    </View>
  </View>
);

/*
    Layout
    Main layout for the app
    Contains the tab navigation
*/
export default function Layout() {
  const { isDarkMode } = useTheme();
  
  // Set background colors based on theme
  const backgroundColor = isDarkMode ? "#121212" : "#f5f5f5";

  return (
    <>
      {/* Tab Navigation */}
      <Tabs
        initialRouteName="home"
        screenOptions={{
          tabBarActiveTintColor: isDarkMode ? "#FFFFFF" : "#FFFFFF",
          tabBarInactiveTintColor: "#AAAAAA",
          tabBarShowLabel: false,
          tabBarStyle: {
            backgroundColor: isDarkMode ? "#374151" : "#333333",
            borderRadius: 25,
            marginHorizontal: 20,
            marginBottom: 40,
            height: 60,
            paddingVertical: 5,
            paddingHorizontal: 20,
            position: "absolute",
            bottom: 0,
            left: 0,
            right: 0,
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-between",
            alignItems: "center",
            borderTopWidth: 0,
          },
          headerShown: false,
          tabBarItemStyle: {
            height: 25,
            paddingVertical: 10,
            marginHorizontal: 5,
          }
        }}
      >
        {/* Home Tab */}
        <Tabs.Screen
          name="home"
          options={{
            title: "",
            tabBarIcon: ({ focused }: { focused: boolean }) => (
              <TabIcon name={icons.home} focused={focused} />
            ),
            headerShown: false,
          }}
        />

        {/* Book Tab */}
        <Tabs.Screen
          name="book"
          options={{
            title: "",
            tabBarIcon: ({ focused }: { focused: boolean }) => (
              <TabIcon name={icons.search} focused={focused} />
            ),
            headerShown: false,
          }}
        />

        {/* Chat Tab */}
        <Tabs.Screen
          name="chat"
          options={{
            title: "",
            tabBarIcon: ({ focused }: { focused: boolean }) => (
              <TabIcon name={icons.chat} focused={focused} />
            ),
            headerShown: false,
          }}
        />

        {/* Profile Tab */}
        <Tabs.Screen
          name="profile"
          options={{
            title: "",
            tabBarIcon: ({ focused }: { focused: boolean }) => (
              <TabIcon name={icons.profile} focused={focused} />
            ),
            headerShown: false,
          }}
        />
      </Tabs>
    </>
  );
}
