import * as React from "react";
import { View, TextInput, TouchableOpacity } from "react-native";
import { Text } from "@/components/common/ThemedText";

interface Location {
  name: string;
  latitude: number;
  longitude: number;
}

interface LocationStepProps {
  isDarkMode: boolean;
  pickupSearch: string;
  dropoffSearch: string;
  searching: string;
  searchResults: Location[];
  setPickupSearch: (text: string) => void;
  setDropoffSearch: (text: string) => void;
  searchLocation: (text: string, type: "pickup" | "dropoff") => void;
  handleLocationSelect: (location: Location) => void;
}

const LocationStep = ({
  isDarkMode,
  pickupSearch,
  dropoffSearch,
  searching,
  searchResults,
  setPickupSearch,
  setDropoffSearch,
  searchLocation,
  handleLocationSelect,
}: LocationStepProps) => {
  const renderSearchResults = () => {
    if (searchResults.length === 0) return null;

    return (
      <View
        className={`absolute left-0 right-0 ${
          searching === "pickup" ? "top-[90px]" : "top-[190px]"
        } ${isDarkMode ? "bg-slate-800" : "bg-white"} rounded-lg shadow-lg z-50`}
        style={{ maxHeight: 200 }}
      >
        {searchResults.map((item, index) => (
          <TouchableOpacity
            key={`${item.name}-${index}`}
            className={`p-3 border-b ${isDarkMode ? "border-slate-700" : "border-slate-100"}`}
            onPress={() => handleLocationSelect(item)}
          >
            <Text>{item.name}</Text>
          </TouchableOpacity>
        ))}
      </View>
    );
  };

  return (
    <View className="flex-1">
      <View
        className={`p-5 rounded-xl shadow-sm mb-5 ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
      >
        <Text className="text-lg font-JakartaBold mb-3">Pickup Location</Text>
        <TextInput
          value={pickupSearch}
          onChangeText={(text) => {
            setPickupSearch(text);
            searchLocation(text, "pickup");
          }}
          placeholder="Where are you starting from?"
          className={`h-[45px] border rounded-lg px-3 ${
            isDarkMode
              ? "bg-slate-700 border-slate-600 text-white"
              : "bg-white border-slate-200 text-black"
          }`}
          placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
          style={{ color: isDarkMode ? "#FFFFFF" : "#000000" }}
        />

        <Text className="text-lg font-JakartaBold mb-3 mt-5">
          Dropoff Location
        </Text>
        <TextInput
          value={dropoffSearch}
          onChangeText={(text) => {
            setDropoffSearch(text);
            searchLocation(text, "dropoff");
          }}
          placeholder="Where are you heading to?"
          className={`h-[45px] border rounded-lg px-3 ${
            isDarkMode
              ? "bg-slate-700 border-slate-600 text-white"
              : "bg-white border-slate-200 text-black"
          }`}
          placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
          style={{ color: isDarkMode ? "#FFFFFF" : "#000000" }}
        />

        {searching && renderSearchResults()}
      </View>
    </View>
  );
};

export default LocationStep;
