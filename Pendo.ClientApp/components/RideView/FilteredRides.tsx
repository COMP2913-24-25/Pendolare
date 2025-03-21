import React, { useState, useEffect } from "react";
import { View, Text, TextInput, TouchableOpacity, LayoutAnimation } from "react-native";
import Slider from "@react-native-community/slider";
import DateTimePicker from "@react-native-community/datetimepicker";
import RideEntry from "./RideEntry";
import { FontAwesome5 } from "@expo/vector-icons";
import { getJourneys } from "@/services/journeyService";

interface FilteredRidesProps {
  isDarkMode: boolean;
  journeyType: number;
}

const FilteredRides = ({ isDarkMode, journeyType }: FilteredRidesProps) => {
  const [collapsed, setCollapsed] = useState(true);
  const [pickupLocation, setPickupLocation] = useState("");
  const [pickupRadius, setPickupRadius] = useState(5);
  const [dropoffLocation, setDropoffLocation] = useState("");
  const [dropoffRadius, setDropoffRadius] = useState(5);
  const [startDateTime, setStartDateTime] = useState(new Date());
  const [filteredRides, setFilteredRides] = useState<any[]>([]);
  const [showRecurrence, setShowRecurrence] = useState(journeyType === 2);

  const getRides = async () => {
    console.log("Getting available rides");
    try {
      const response = await getJourneys();
      if (response.success) {
        console.log("found available rides");
        setFilteredRides(response.journeys);
      }
    } catch (error) {
      console.error("Failed to fetch journeys:", error);
    }
  }

  useEffect(() => {
    getRides();
  }, []);

  const toggleCollapse = () => {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setCollapsed(!collapsed);
  };

  return (
    <View>
      <TouchableOpacity onPress={toggleCollapse} className="flex-row items-center mb-4">
        <FontAwesome5
          name={collapsed ? "chevron-right" : "chevron-down"}
          size={24}
          color={isDarkMode ? "#fff" : "#000"}
        />
        <Text className={`text-xl font-JakartaBold ml-2 ${isDarkMode ? "text-white" : "text-black"}`}>
          Filter Rides
        </Text>
      </TouchableOpacity>
      {!collapsed && (
        <View className={`mb-4 p-4 rounded-xl ${isDarkMode ? "bg-slate-800" : "bg-white"} shadow-md`}>
          <View className="mb-3">
            <Text className={`${isDarkMode ? "text-white" : "text-black"} mb-1`}>Pickup Location</Text>
            <TextInput
              placeholder="Enter pickup location"
              placeholderTextColor={isDarkMode ? "#ccc" : "#555"}
              value={pickupLocation}
              onChangeText={setPickupLocation}
              className={`p-2 border rounded-lg ${
                isDarkMode
                  ? "bg-slate-700 text-white border-gray-600"
                  : "bg-gray-50 text-black border-gray-300"
              }`}
            />
            <Text className={`${isDarkMode ? "text-white" : "text-black"} mt-2`}>Pickup Radius: {pickupRadius} km</Text>
            <Slider
              value={pickupRadius}
              onValueChange={setPickupRadius}
              minimumValue={1}
              maximumValue={50}
              step={1}
              minimumTrackTintColor={isDarkMode ? "#fff" : "#000"}
              maximumTrackTintColor={isDarkMode ? "#aaa" : "#888"}
            />
          </View>
          <View className="mb-3">
            <Text className={`${isDarkMode ? "text-white" : "text-black"} mb-1`}>Dropoff Location</Text>
            <TextInput
              placeholder="Enter dropoff location"
              placeholderTextColor={isDarkMode ? "#ccc" : "#555"}
              value={dropoffLocation}
              onChangeText={setDropoffLocation}
              className={`p-2 border rounded-lg ${
                isDarkMode
                  ? "bg-slate-700 text-white border-gray-600"
                  : "bg-gray-50 text-black border-gray-300"
              }`}
            />
            <Text className={`${isDarkMode ? "text-white" : "text-black"} mt-2`}>Dropoff Radius: {dropoffRadius} km</Text>
            <Slider
              value={dropoffRadius}
              onValueChange={setDropoffRadius}
              minimumValue={1}
              maximumValue={50}
              step={1}
              minimumTrackTintColor={isDarkMode ? "#fff" : "#000"}
              maximumTrackTintColor={isDarkMode ? "#aaa" : "#888"}
            />
          </View>
          <View className="mb-3">
            <Text className={`${isDarkMode ? "text-white" : "text-black"} mb-1`}>Journey Time</Text>
            <View style={{ marginLeft: -10}}>
              <DateTimePicker
                minimumDate={new Date()}
                value={startDateTime}
                mode="datetime"
                display="default"
                themeVariant={isDarkMode ? "dark" : "light"}
                textColor={isDarkMode ? "#ffffff" : "#000000"}
              />
            </View>
          </View>
        </View>
      )}
      <Text className={`text-xl font-JakartaBold mb-4 ${isDarkMode ? "text-white" : "text-black"}`}>
        Available Rides
      </Text>
      {filteredRides.map((ride, index) => (
        <RideEntry key={ride.BookingId || index} ride={ride} />
      ))}
    </View>
  );
};

export default FilteredRides;