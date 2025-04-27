import React, { useState, useEffect, useCallback } from "react";
import { View, Text, TextInput, TouchableOpacity, LayoutAnimation } from "react-native";
import Slider from "@react-native-community/slider";
import DateTimePicker from "@react-native-community/datetimepicker";
import RideEntry from "./RideEntry";
import { FontAwesome5 } from "@expo/vector-icons";
import { getJourneys, GetJourneysRequest } from "@/services/journeyService";
import { searchLocations } from "@/services/locationService";

interface FilteredRidesProps {
  resetFilters: boolean;
  onFiltersReset: () => void;
  isDarkMode: boolean;
  journeyType: number;
  onBookingSuccess?: () => void;
}

interface Location {
  name: string;
  latitude: number;
  longitude: number;
}

const FilteredRides = ({
  resetFilters,
  onFiltersReset,
  isDarkMode,
  journeyType,
  onBookingSuccess
}: FilteredRidesProps) => {

  const [collapsed, setCollapsed] = useState(true);

  const [fieldPickupLocation, setFieldPickupLocation] = useState("");
  const [pickupCoords, setPickupCoords] = useState({ lat: 0.0, lon: 0.0 });
  const [pickupLocation, setPickupLocation] = useState("");
  const [pickupRadius, setPickupRadius] = useState(5);
  const [dropoffCoords, setDropoffCoords] = useState({ lat: 0.0, lon: 0.0 });

  const [fieldDropoffLocation, setFieldDropoffLocation] = useState("");
  const [dropoffLocation, setDropoffLocation] = useState("");
  const [dropoffRadius, setDropoffRadius] = useState(5);
  const [startDateTime, setStartDateTime] = useState(new Date());
  const [filteredRides, setFilteredRides] = useState<any[]>([]);

  const [pickupSearchResults, setPickupSearchResults] = useState<any[]>([]);
  const [dropoffSearchResults, setDropoffSearchResults] = useState<any[]>([]);

  const handleLocationSelect = (searching: string, location: Location) => {
    if (searching === "pickup") {
      setPickupCoords({ lat: location.latitude, lon: location.longitude });
      setPickupLocation(location.name);
      setFieldPickupLocation(location.name);
      setPickupSearchResults([]);
    } else {
      setDropoffCoords({ lat: location.latitude, lon: location.longitude });
      setDropoffLocation(location.name);
      setFieldDropoffLocation(location.name);
      setDropoffSearchResults([]);
    }
  };

  const getRides = useCallback(async (forceReset = false) => {
    let filters: GetJourneysRequest = {
      DriverView: false,
      StartDate: new Date().toISOString(),
      JourneyType: journeyType,
    };

    if (pickupLocation.length > 0 && pickupCoords.lat !== 0.0) {
      filters.DistanceRadius = pickupRadius;
      filters.StartLat = pickupCoords.lat;
      filters.StartLong = pickupCoords.lon;
    }

    if (dropoffLocation.length > 0 && dropoffCoords.lat !== 0.0) {
      filters.DistanceRadius = pickupRadius;
      filters.EndLat = dropoffCoords.lat;
      filters.EndLong = dropoffCoords.lon;
    }

    if (startDateTime.toDateString() !== new Date().toDateString()) {
      filters.StartDate = startDateTime.toISOString();
    }

    console.log("Getting available rides");
    try {
      if (forceReset) {
        console.log("Resetting filters and fetching all rides for type:", journeyType);
        filters = { DriverView: false, JourneyType: journeyType, StartDate: new Date().toISOString() };
        setFieldDropoffLocation("");
        setFieldPickupLocation("");
        setDropoffLocation("");
        setPickupLocation("");
        setPickupCoords({ lat: 0.0, lon: 0.0 });
        setDropoffCoords({ lat: 0.0, lon: 0.0 });
        setStartDateTime(new Date());
        setPickupRadius(5);
        onFiltersReset();
      }

      console.log("Fetching journeys with filters:", filters);

      const response = await getJourneys(filters);
      if (response.success) {
        console.log(`Found ${response.journeys.length} available rides`);
        setFilteredRides(response.journeys);
      } else {
        console.error("Failed to fetch journeys:", response.message);
        setFilteredRides([]);
      }
    } catch (error) {
      console.error("Error during fetch journeys:", error);
      setFilteredRides([]);
    }
  }, [journeyType, pickupLocation, pickupCoords, pickupRadius, dropoffLocation, dropoffCoords, startDateTime, onFiltersReset]);

  useEffect(() => {
    if (resetFilters) {
      getRides(true);
    } else {
      getRides();
    }
  }, [resetFilters, getRides]);

  const toggleCollapse = () => {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setCollapsed(!collapsed);
  };

  const renderSearchResults = (searchResults: Location[], searching: string) => {
    if (searchResults.length === 0) return null;

    return (
      <View
        className={`relative left-0 right-0 ${isDarkMode ? "bg-slate-800" : "bg-white"} rounded-lg shadow-lg z-50`}
        style={{ maxHeight: 200 }}
      >
        {searchResults.slice(0, 3).map((item, index) => (
          <TouchableOpacity
            key={`${item.name}-${index}`}
            className={`p-3 border-b ${isDarkMode ? "border-slate-700" : "border-slate-100"}`}
            onPress={() => handleLocationSelect(searching, item)}
          >
            <Text>{item.name}</Text>
          </TouchableOpacity>
        ))}
      </View>
    );
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
              value={fieldPickupLocation}
              onChangeText={(text) => {
                setFieldPickupLocation(text);
                searchLocations(text, "pickup", null, setPickupSearchResults);
              }}
              className={`p-2 border rounded-lg ${
                isDarkMode
                  ? "bg-slate-700 text-white border-gray-600"
                  : "bg-gray-50 text-black border-gray-300"
              }`}
            />
            {renderSearchResults(pickupSearchResults, "pickup")}
            <Text className={`${isDarkMode ? "text-white" : "text-black"} mt-2`}>Search Radius: {pickupRadius} km</Text>
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
              value={fieldDropoffLocation}
              onChangeText={(text) => {
                setFieldDropoffLocation(text);
                searchLocations(text, "dropoff", null, setDropoffSearchResults);
              }}
              className={`p-2 border rounded-lg ${
                isDarkMode
                  ? "bg-slate-700 text-white border-gray-600"
                  : "bg-gray-50 text-black border-gray-300"
              }`}
            />
            {renderSearchResults(dropoffSearchResults, "dropoff")}
          </View>
          <View className="mb-3">
            <Text className={`${isDarkMode ? "text-white" : "text-black"} mb-1`}>Journey Time</Text>
            <View style={{ marginLeft: -16 }}>
              <DateTimePicker
                minimumDate={new Date()}
                value={startDateTime}
                mode="datetime"
                display="default"
                themeVariant={isDarkMode ? "dark" : "light"}
                textColor={isDarkMode ? "#ffffff" : "#000000"}
                onChange={(_, date) => {
                  console.log(date);
                  if (typeof date !== "undefined") {
                    setStartDateTime(date);
                  }
                }}
              />
            </View>
          </View>
          <View>
            <TouchableOpacity
              className="bg-blue-500 p-4 rounded-lg mb-5"
              onPress={() => getRides()}
            >
              <Text className="text-md font-JakartaSemiBold text-white text-center">Filter Rides</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}
      <Text className={`text-xl font-JakartaBold mb-4 ${isDarkMode ? "text-white" : "text-black"}`}>
        Available Rides
      </Text>
      {filteredRides.length > 0 ? (
        filteredRides.map((ride, index) => (
          <RideEntry
            key={ride.BookingId || index}
            ride={ride}
            onBookingSuccess={onBookingSuccess}
          />
        ))
      ) : (
        <Text className={`text-center mt-4 ${isDarkMode ? "text-gray-400" : "text-gray-600"}`}>
          No rides found matching your criteria.
        </Text>
      )}
    </View>
  );
};

export default FilteredRides;