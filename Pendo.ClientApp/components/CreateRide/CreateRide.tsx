import { FontAwesome5 } from "@expo/vector-icons";
import { useState, useCallback } from "react";
import { View, TouchableOpacity, ScrollView } from "react-native";
import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";

import ConfirmationStep from "./ConfirmationStep";
import CostAndSeatsStep from "./CostAndSeatsStep";
import DateTimeStep from "./DateTimeStep";
import LocationStep from "./LocationStep";
import StepIndicator from "./StepIndicator";

import { Text } from "@/components/common/ThemedText";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { createJourney } from "@/services/journeyService";
import { validateRegPlate } from "@/services/dvlaService";
import { toCronString } from "@/utils/cronTools";
import { searchLocations } from "@/services/locationService";
import { costValidator, integerValidator, stringLengthValidator } from "@/utils/validators";
import { Alert } from "react-native";

interface Location {
  name: string;
  latitude: number;
  longitude: number;
}

interface CreateRideProps {
  onClose: () => void;
}

/*
  CreateRide
  Screen for creating a new ride
*/
const CreateRide = ({ onClose }: CreateRideProps) => {
  const { isDarkMode } = useTheme();
  const [step, setStep] = useState(1);
  
  // Location states
  const [pickup, setPickup] = useState<Location | null>(null);
  const [dropoff, setDropoff] = useState<Location | null>(null);
  const [pickupSearch, setPickupSearch] = useState("");
  const [dropoffSearch, setDropoffSearch] = useState("");
  
  // Ride details states
  const [cost, setCost] = useState("");
  const [costValidationMessage, setCostValidationMessage] = useState<string | null>(null);

  const [seats, setSeats] = useState("");

  const [regPlate, setRegPlate] = useState("");
  const [regPlateValidationMessage, setRegPlateValidationMessage] = useState<string | null>(null);

  const [bootHeight, setBootHeight] = useState("");
  const [bootHeightValidationMessage, setBootHeightValidationMessage] = useState<string | null>(null);

  const [bootWidth, setBootWidth] = useState("");
  const [bootWidthValidationMessage, setBootWidthValidationMessage] = useState<string | null>(null);
  
  // Date and time states
  const [date, setDate] = useState(new Date());
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(() => {
    const futureDate = new Date();
    futureDate.setMonth(futureDate.getMonth() + 3); // Default 3 months ahead
    return futureDate;
  });
  const [showDatePicker, setShowDatePicker] = useState(false);
  
  // Commuter journey states
  const [isCommuter, setIsCommuter] = useState(false);
  const [selectedDays, setSelectedDays] = useState<string[]>([]);
  const [frequency, setFrequency] = useState<"weekly" | "fortnightly" | "monthly">("weekly");
  const [selectedDiscount, setSelectedDiscount] = useState({ label: "No Discount", value: null, percentage: 0 });
  
  // Search states
  const [searchResults, setSearchResults] = useState<Location[]>([]);
  const [searching, setSearching] = useState("");

  // Update date with memoized callback to prevent unnecessary re-renders
  const updateDate = useCallback((newDate: Date) => {
    console.log(`Date updated: ${newDate.toLocaleString()}`);
    setDate(newDate);
  }, []);

  // Handle location selection from search results
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

  // Handle navigation between steps
  const handleNext = () => {
    if (step < 4) {
      if (step === 3) {
        // Log date when moving to confirmation
        console.log(`Moving to confirmation with date: ${date.toLocaleString()}`);
      }
      setStep(step + 1);
    } else {
      handleCreateRide();
    }
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
    else onClose();
  };

  const canGoNext = () => {
    switch (step) {
      case 1:
        return pickup && dropoff;
      case 2:
        return cost && regPlate;
      case 3:
        return isCommuter ? selectedDays.length > 0 : true;
      default:
        return true;
    }
  };

  // Create a new ride
  const handleCreateRide = async () => {
    try {
      // Prepare payload
      const payload: any = {
        AdvertisedPrice: parseFloat(cost),
        StartName: pickup?.name || "",
        StartLat: pickup?.latitude,
        StartLong: pickup?.longitude,
        EndName: dropoff?.name || "",
        EndLat: dropoff?.latitude,
        EndLong: dropoff?.longitude,
        StartDate: date.toISOString(),
        StartTime: date.toISOString(),
        MaxPassengers: parseInt(seats, 10),
        JourneyStatusId: 1,
        RegPlate: regPlate,
        BootHeight: Number(bootHeight),
        BootWidth: Number(bootWidth),
        JourneyType: isCommuter ? 2 : 1,
        Recurrance: isCommuter ? toCronString(frequency, selectedDays, date) : undefined,
        RepeatUntil: isCommuter ? endDate.toISOString() : new Date(9999, 9, 9).toISOString()
      }

      // Add discount ID directly from selection if available
      if (isCommuter && selectedDiscount && selectedDiscount.value) {
        payload.DiscountID = selectedDiscount.value;
      }

      console.log("Creating ride with payload:", payload);
      const result = await createJourney(payload);
      console.log("Journey created:", result);
      onClose();
    } catch (error) {
      console.error("Failed to create journey:", error);
      alert("Failed to create journey. Please try again.");
    }
  };

  return (
    <ThemedSafeAreaView className="flex-1" style={{ flex: 1 }}>
      <View className="flex-1">
        <View className="px-5 pt-8">
          <View className="flex-row items-center justify-between mb-6">
            <TouchableOpacity onPress={handleBack} className="p-2 -ml-2">
              <FontAwesome5
                name={icons.backArrow}
                size={24}
                color={isDarkMode ? "#FFF" : "#000"}
              />
            </TouchableOpacity>
            <Text className="text-2xl font-JakartaBold">Create a Ride</Text>
            <View className="w-10" />
          </View>

          <StepIndicator currentStep={step} />
        </View>

        {/* Ride Creation Steps */}
        <ScrollView
          className="flex-1 px-5"
          showsVerticalScrollIndicator={false}
          contentContainerStyle={{ paddingBottom: 100 }}
        >
          {step === 1 && (
            <LocationStep
              isDarkMode={isDarkMode}
              pickupSearch={pickupSearch}
              dropoffSearch={dropoffSearch}
              searching={searching}
              searchResults={searchResults}
              setPickupSearch={setPickupSearch}
              setDropoffSearch={setDropoffSearch}
              searchLocation={(query, type) => searchLocations(query, type, setSearching, setSearchResults)}
              handleLocationSelect={handleLocationSelect}
            />
          )}
          
          {step === 2 && (
            <CostAndSeatsStep
              isDarkMode={isDarkMode}
              cost={cost}
              seats={seats}
              setCost={(value) => {costValidator(setCost, value, 1, 100, setCostValidationMessage); }}
              costValidationMessage={costValidationMessage}
              setSeats={(value) => integerValidator(setSeats, value, 1, 7)}
              regPlate={regPlate}
              setRegPlate={(value) => stringLengthValidator(setRegPlate, value, 0, 7, setRegPlateValidationMessage)}
              regPlateValidationMessage={regPlateValidationMessage}
              bootHeight={bootHeight}
              setBootHeight={(value) => {integerValidator(setBootHeight, value, null, 200, setBootHeightValidationMessage); }}
              bootHeightValidationMessage={bootHeightValidationMessage}
              bootWidth={bootWidth}
              setBootWidth={(value) => {integerValidator(setBootWidth, value, null, 200, setBootWidthValidationMessage); }}
              bootWidthValidationMessage={bootWidthValidationMessage}
            />
          )}
          
          {step === 3 && (
            <DateTimeStep
              isDarkMode={isDarkMode}
              isCommuter={isCommuter}
              setIsCommuter={setIsCommuter}
              frequency={frequency}
              setFrequency={setFrequency}
              selectedDays={selectedDays}
              setSelectedDays={setSelectedDays}
              date={date}
              setDate={updateDate}
              showDatePicker={showDatePicker}
              setShowDatePicker={setShowDatePicker}
              startDate={startDate}
              endDate={endDate}
              setStartDate={setStartDate}
              setEndDate={setEndDate}
              selectedDiscount={selectedDiscount}
              setSelectedDiscount={setSelectedDiscount}
            />
          )}
          
          {step === 4 && (
            <ConfirmationStep
              isDarkMode={isDarkMode}
              pickup={pickup}
              dropoff={dropoff}
              cost={cost}
              seats={seats}
              date={date}
              bootHeight={bootHeight}
              bootWidth={bootWidth}
              isCommuter={isCommuter}
              selectedDiscount={selectedDiscount}
            />
          )}
        </ScrollView>

        {/* Next Button */}
        <View className="px-5 py-4">
          <TouchableOpacity
            className={`bg-blue-600 p-4 rounded-xl ${(!pickup || !dropoff) ? "opacity-50" : ""}`}
            onPress={() => canGoNext() ? handleNext() : Alert.alert("Please fill in all required fields.")}
            disabled={!pickup || !dropoff}
          >
            <Text className="text-white text-center font-JakartaBold text-lg">
              {step === 4 ? "Create Ride" : "Next"}
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </ThemedSafeAreaView>
  );
};

export default CreateRide;
