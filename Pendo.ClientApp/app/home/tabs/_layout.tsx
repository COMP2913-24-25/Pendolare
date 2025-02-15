import { Tabs } from "expo-router";
import { Image, ImageSourcePropType, View } from "react-native";

import { icons } from "@/constants";

const TabIcon = ({
  source,
  focused,
}: {
  source: ImageSourcePropType;
  focused: boolean;
}) => (
  <View
    style={{
      width: 40,
      height: 40,
      justifyContent: "center",
      alignItems: "center",
      backgroundColor: focused ? "#2563EB" : "transparent",
      borderRadius: 20,
      marginVertical: "auto", // Add vertical auto margin
    }}
  >
    <Image
      source={source}
      style={{
        width: 22,
        height: 22,
        tintColor: focused ? "#FFFFFF" : "#AAAAAA",
      }}
      resizeMode="contain"
    />
  </View>
);

export default function Layout() {
  return (
    <Tabs
      initialRouteName="home"
      screenOptions={{
        tabBarActiveTintColor: "white",
        tabBarInactiveTintColor: "#AAAAAA",
        tabBarShowLabel: false,
        tabBarStyle: {
          backgroundColor: "#333333",
          borderRadius: 25,
          marginHorizontal: 20,
          marginBottom: 20,
          height: 65,
          paddingBottom: 40, // Add bottom padding
          paddingVertical: 10, // Add vertical padding
          paddingHorizontal: 20,
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center", // Center items vertically
          borderTopWidth: 0,
        },
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="home"
        options={{
          title: "Home",
          tabBarIcon: ({ focused }) => (
            <TabIcon source={icons.home} focused={focused} />
          ),
        }}
      />
      <Tabs.Screen
        name="chat"
        options={{
          title: "Chat",
          tabBarIcon: ({ focused }) => (
            <TabIcon source={icons.chat} focused={focused} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          tabBarIcon: ({ focused }) => (
            <TabIcon source={icons.profile} focused={focused} />
          ),
        }}
      />
    </Tabs>
  );
}
