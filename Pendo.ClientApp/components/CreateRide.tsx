import DateTimePicker from "@react-native-community/datetimepicker";
import axios from "axios";
import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Image,
  FlatList,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import Map from "./Map";

import { icons } from "@/constants";

interface Location {
  name: string;
  latitude: number;
  longitude: number;
}

interface CreateRideProps {
  onClose: () => void;
}

const CreateRide = ({ onClose }: CreateRideProps) => {
  const [step, setStep] = useState(1);
  const [pickup, setPickup] = useState<Location | null>(null);
  const [dropoff, setDropoff] = useState<Location | null>(null);
  const [cost, setCost] = useState("");
  const [seats, setSeats] = useState("");
  const [date, setDate] = useState(new Date());
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [searchResults, setSearchResults] = useState<Location[]>([]);
  const [pickupSearch, setPickupSearch] = useState("");
  const [dropoffSearch, setDropoffSearch] = useState("");
  const [searching, setSearching] = useState(""); // 'pickup' or 'dropoff'

  interface Feature {
    properties: {
      label: string;
    };
    geometry: {
      coordinates: number[];
    };
  }

  const searchLocation = async (query: string, type: "pickup" | "dropoff") => {
    if (query.length < 3) return;
    setSearching(type);

    try {
      const response = await axios.get(
        `https://api.openrouteservice.org/geocode/search?api_key=${process.env.EXPO_PUBLIC_OSR_KEY}&text=${query}`,
      );

      if (response.data.features) {
        setSearchResults(
          response.data.features.map((feature: Feature) => ({
            name: feature.properties.label,
            latitude: feature.geometry.coordinates[1],
            longitude: feature.geometry.coordinates[0],
          })),
        );
      }
    } catch (error) {
      console.error("Location search error:", error);
    }
  };

  const handleLocationSelect = (location: Location) => {
    if (searching === "pickup") {
      setPickup(location);
      setPickupSearch(location.name);
    } else {
      setDropoff(location);
      setDropoffSearch(location.name);
    }
    setSearchResults([]);
    setSearching("");
  };

  const handleNext = () => {
    if (step < 4) setStep(step + 1);
    else handleCreateRide();
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
    else onClose();
  };

  const handleCreateRide = () => {
    const newRide = {
      id: Date.now(),
      driverName: "Alex McCall",
      availableSeats: parseInt(seats, 10),
      departureTime: date.toLocaleTimeString(),
      destination: dropoff?.name || "Unknown",
      price: `£${cost}`,
      rating: 5.0,
      pickup,
      dropoff,
    };
    onClose();
  };

  const renderLocationSearch = () => (
    <View className="absolute left-5 right-5 top-[120px] bg-white rounded-lg shadow-lg z-50">
      <FlatList
        data={searchResults}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity
            className="p-3 border-b border-slate-100"
            onPress={() => handleLocationSelect(item)}
          >
            <Text>{item.name}</Text>
          </TouchableOpacity>
        )}
        style={{ maxHeight: 200 }}
      />
    </View>
  );

  const renderStep1 = () => (
    <View className="flex-1">
      <View className="bg-white p-5 rounded-xl shadow-sm mb-5">
        <Text className="text-lg font-JakartaBold mb-3">Pickup Location</Text>
        <TextInput
          value={pickupSearch}
          onChangeText={(text) => {
            setPickupSearch(text);
            searchLocation(text, "pickup");
          }}
          placeholder="Where are you starting from?"
          className="h-[45px] border border-slate-200 rounded-lg px-3"
        />
        {searching === "pickup" &&
          searchResults.length > 0 &&
          renderLocationSearch()}

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
          className="h-[45px] border border-slate-200 rounded-lg px-3"
        />
        {searching === "dropoff" &&
          searchResults.length > 0 &&
          renderLocationSearch()}
      </View>
    </View>
  );

  const renderStep2 = () => (
    <View className="bg-white p-5 rounded-xl shadow-sm">
      <View className="mb-4">
        <Text className="text-lg font-JakartaBold mb-2">Cost (£)</Text>
        <TextInput
          value={cost}
          onChangeText={setCost}
          keyboardType="numeric"
          className="h-[45px] border border-slate-200 rounded-lg px-3"
          placeholder="Enter cost per seat"
        />
      </View>

      <View className="mb-4">
        <Text className="text-lg font-JakartaBold mb-2">Available Seats</Text>
        <TextInput
          value={seats}
          onChangeText={setSeats}
          keyboardType="numeric"
          className="h-[45px] border border-slate-200 rounded-lg px-3"
          placeholder="Enter number of seats"
        />
      </View>
    </View>
  );

  const renderStep3 = () => (
    <View className="bg-white p-5 rounded-xl shadow-sm">
      <Text className="text-lg font-JakartaBold mb-2">Date and Time</Text>
      <TouchableOpacity
        onPress={() => setShowDatePicker(true)}
        className="h-[45px] border border-slate-200 rounded-lg px-3 justify-center"
      >
        <Text>{date.toLocaleString()}</Text>
      </TouchableOpacity>
      {showDatePicker && (
        <DateTimePicker
          value={date}
          mode="datetime"
          display="default"
          onChange={(event, selectedDate) => {
            setShowDatePicker(false);
            if (selectedDate) {
              setDate(selectedDate);
            }
          }}
        />
      )}
    </View>
  );

  const renderStep4 = () => (
    <View className="flex-1">
      <View className="h-[200px] bg-white rounded-xl shadow-sm mb-5">
        <Map pickup={pickup} dropoff={dropoff} />
      </View>

      <View className="bg-white p-5 rounded-xl shadow-sm">
        <Text className="text-lg font-JakartaBold mb-4">
          Confirm Ride Details
        </Text>

        <View className="mb-3">
          <Text className="text-sm text-gray-500">From</Text>
          <Text className="text-base">{pickup?.name}</Text>
        </View>

        <View className="mb-3">
          <Text className="text-sm text-gray-500">To</Text>
          <Text className="text-base">{dropoff?.name}</Text>
        </View>

        <View className="mb-3">
          <Text className="text-sm text-gray-500">Price per Seat</Text>
          <Text className="text-base">£{cost}</Text>
        </View>

        <View className="mb-3">
          <Text className="text-sm text-gray-500">Available Seats</Text>
          <Text className="text-base">{seats}</Text>
        </View>

        <View className="mb-3">
          <Text className="text-sm text-gray-500">Date & Time</Text>
          <Text className="text-base">{date.toLocaleString()}</Text>
        </View>
      </View>
    </View>
  );

  return (
    <SafeAreaView className="flex-1 bg-general-500" edges={["top", "bottom"]}>
      <View className="flex-1 px-5 pt-8 pb-4">
        <View className="flex-row items-center justify-between mb-6">
          <TouchableOpacity onPress={handleBack} className="p-2 -ml-2 mt-4">
            <Image source={icons.backArrow} className="w-6 h-6" />
          </TouchableOpacity>
          <Text className="text-2xl font-JakartaBold mt-4">Create a Ride</Text>
          <View className="w-10 mt-4" />
        </View>
        <View className="flex-row justify-between mb-8 px-4">
          {[1, 2, 3, 4].map((stepNumber) => (
            <View key={stepNumber} className="flex-row items-center">
              <View
                className={`w-8 h-8 rounded-full ${
                  step >= stepNumber ? "bg-blue-600" : "bg-gray-300"
                } items-center justify-center`}
              >
                <Text className="text-white font-JakartaBold">
                  {stepNumber}
                </Text>
              </View>
              {stepNumber < 4 && (
                <View
                  className={`h-[2px] w-[30px] ${
                    step > stepNumber ? "bg-blue-600" : "bg-gray-300"
                  }`}
                />
              )}
            </View>
          ))}
        </View>
        <View className="flex-1">
          {step === 1 && renderStep1()}
          {step === 2 && renderStep2()}
          {step === 3 && renderStep3()}
          {step === 4 && renderStep4()}
        </View>
        <View className="mt-4">
          <TouchableOpacity
            className="bg-blue-600 p-4 rounded-xl mb-2"
            onPress={handleNext}
            disabled={!pickup || !dropoff}
          >
            <Text className="text-white text-center font-JakartaBold text-lg">
              {step === 4 ? "Create Ride" : "Next"}
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
};

export default CreateRide;
