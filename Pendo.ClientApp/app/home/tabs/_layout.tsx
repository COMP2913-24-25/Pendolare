import { FontAwesome5 } from "@expo/vector-icons";
import { Tabs } from "expo-router";
import { View } from "react-native";

import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";

const TabIcon = ({ name, focused }: { name: string; focused: boolean }) => (
  <View
    style={{
      width: 60,
      height: 50, // Reduced to match tab bar height
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

export default function Layout() {
  const { isDarkMode } = useTheme();

  return (
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
          height: 60, // Adjusted height
          paddingVertical: 5, // Reduced padding
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
          height: 25, // Adjusted to match new container height
          paddingVertical: 10, // Added padding
          marginHorizontal: 5, // Added margin
        },
      }}
    >
      <Tabs.Screen
        name="home"
        options={{
          title: "Home",
          tabBarIcon: ({ focused }) => (
            <TabIcon name={icons.home} focused={focused} />
          ),
          headerShown: false, // Ensure header is not shown for this tab
        }}
      />
      <Tabs.Screen
        name="book"
        options={{
          title: "Book",
          tabBarIcon: ({ focused }) => (
            <TabIcon name={icons.search} focused={focused} />
          ),
          headerShown: false, // Ensure header is not shown for this tab
        }}
      />
      <Tabs.Screen
        name="chat"
        options={{
          title: "Chat",
          tabBarIcon: ({ focused }) => (
            <TabIcon name={icons.chat} focused={focused} />
          ),
          headerShown: false, // Ensure header is not shown for this tab
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          tabBarIcon: ({ focused }) => (
            <TabIcon name={icons.profile} focused={focused} />
          ),
          headerShown: false, // Ensure header is not shown for this tab
        }}
      />
    </Tabs>
  );
}
