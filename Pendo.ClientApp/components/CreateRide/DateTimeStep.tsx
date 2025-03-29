import { FontAwesome5 } from "@expo/vector-icons";
import DateTimePicker from "@react-native-community/datetimepicker";
import { useState, useEffect } from "react";
import { Platform, View, TouchableOpacity, ScrollView, ActivityIndicator } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { getDiscounts } from "@/services/paymentService";

const frequencies = [
  { label: "Weekly", value: "weekly" },
  { label: "Fortnightly", value: "fortnightly" },
  { label: "Monthly", value: "monthly" },
];

const weekDays = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];

const defaultDiscountOption = { label: "No Discount", value: null, percentage: 0, weeklyJourneys: 0 };

interface DateTimeStepProps {
  isDarkMode: boolean;
  isCommuter: boolean;
  setIsCommuter: (value: boolean) => void;
  frequency: string;
  setFrequency: (value: any) => void;
  selectedDays: string[];
  setSelectedDays: (value: string[]) => void;
  date: Date;
  setDate: (value: Date) => void;
  showDatePicker: boolean;
  setShowDatePicker: (value: boolean) => void;
  startDate: Date;
  endDate: Date;
  setStartDate: (date: Date) => void;
  setEndDate: (date: Date) => void;
  selectedDiscount: any;
  setSelectedDiscount: (discount: any) => void;
}

/*
  DateTimeStep
  Step for selecting date and time
*/
const DateTimeStep = (props: DateTimeStepProps) => {
  const {
    isDarkMode,
    isCommuter,
    setIsCommuter,
    frequency,
    setFrequency,
    selectedDays,
    setSelectedDays,
    date,
    setDate,
    showDatePicker,
    setShowDatePicker,
    startDate,
    endDate,
    setStartDate,
    setEndDate,
    selectedDiscount,
    setSelectedDiscount
  } = props;

  // Local state to track what picker is currently open
  const [pickerMode, setPickerMode] = useState<"date" | "time" | "datetime">("datetime");
  const [currentPicker, setCurrentPicker] = useState<"regular" | "start" | "end" | "time">("regular");
  
  // Display formatted values
  const [displayDate, setDisplayDate] = useState("");
  const [displayStartDate, setDisplayStartDate] = useState("");
  const [displayEndDate, setDisplayEndDate] = useState("");
  const [displayTime, setDisplayTime] = useState("");
  
  // Update display formats when dates change
  useEffect(() => {
    setDisplayDate(formatDateTime(date));
    setDisplayStartDate(formatDate(startDate));
    setDisplayEndDate(formatDate(endDate));
    setDisplayTime(formatTime(date));
  }, [date, startDate, endDate]);

  // Formatting functions
  const formatDate = (date: Date) => {
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString(undefined, {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDateTime = (date: Date) => {
    return `${formatDate(date)} at ${formatTime(date)}`;
  };

  // Open date picker with specific mode
  const showPicker = (pickerType: "regular" | "start" | "end" | "time") => {
    setCurrentPicker(pickerType);
    
    // Set correct picker mode
    if (pickerType === "time") {
      setPickerMode("time");
    } else if (pickerType === "regular") {
      setPickerMode("datetime");
    } else {
      setPickerMode("date");
    }
    
    setShowDatePicker(true);
  };

  // Handle date selection
  const handleDateChange = (event: any, selectedDate?: Date) => {
    try {
      // Always hide the date picker on Android after a selection or cancellation
      if (Platform.OS === 'android') {
        setShowDatePicker(false);
      }
      
      // If no date selected (user cancelled), just return
      if (!selectedDate) return;
      
      // Handle different date picker modes
      switch (currentPicker) {
        case "regular":
          // For non-commuter journey, set the full date+time
          const newDate = new Date(selectedDate);
          console.log(`Setting regular date to: ${newDate.toLocaleString()}`);
          setDate(newDate);
          break;
          
        case "start":
          console.log(`Setting start date to: ${selectedDate.toLocaleString()}`);
          setStartDate(selectedDate);
          break;
          
        case "end":
          console.log(`Setting end date to: ${selectedDate.toLocaleString()}`);
          setEndDate(selectedDate);
          break;
          
        case "time":
          // For commuter journey - update only time part
          const newTimeDate = new Date(date);
          newTimeDate.setHours(selectedDate.getHours());
          newTimeDate.setMinutes(selectedDate.getMinutes());
          console.log(`Setting time to: ${newTimeDate.toLocaleString()}`);
          setDate(newTimeDate);
          break;
      }
    } catch (error) {
      // If any error occurs during the date picker handling, ensure it's hidden
      console.error("Error in date picker:", error);
      setShowDatePicker(false);
    }
  };
  
  // Close date picker (iOS only)
  const closePicker = () => {
    setShowDatePicker(false);
    setCurrentPicker("regular");
  };

  // Toggle day selection
  const toggleDay = (day: string) => {
    if (selectedDays.includes(day)) {
      setSelectedDays(selectedDays.filter(d => d !== day));
    } else {
      setSelectedDays([...selectedDays, day]);
    }
  };

  const [discountOptions, setDiscountOptions] = useState([defaultDiscountOption]);
  const [loadingDiscounts, setLoadingDiscounts] = useState(false);
  
  // Fetch discount options when component mounts
  useEffect(() => {
    const fetchDiscounts = async () => {
      setLoadingDiscounts(true);
      try {
        const discounts = await getDiscounts();
        
        if (discounts && discounts.length > 0) {
          const formattedDiscounts = discounts.map(discount => {
            // Make sure the discount has valid values
            if (!discount || typeof discount.WeeklyJourneys !== 'number' || typeof discount.DiscountPercentage !== 'number') {
              console.warn("Invalid discount data:", discount);
              return null;
            }
            
            return {
              label: `${discount.WeeklyJourneys} Journeys/Week (${discount.DiscountPercentage * 100}% off)`,
              value: discount.DiscountId,
              percentage: discount.DiscountPercentage,
              weeklyJourneys: discount.WeeklyJourneys
            };
          }).filter(Boolean); // Filter out null values
          
          setDiscountOptions([defaultDiscountOption, ...formattedDiscounts]);
        }
      } catch (error) {
        console.error("Error fetching discounts:", error);
      } finally {
        setLoadingDiscounts(false);
      }
    };
    
    fetchDiscounts();
  }, []);

  const renderDiscountOptions = () => (
    <>
      <Text className="mt-4 mb-2">Discount Options</Text>
      <View
        className={`border rounded-lg mb-4 ${
          isDarkMode ? "border-slate-600" : "border-slate-200"
        }`}
      >
        {loadingDiscounts ? (
          <View className="p-4 flex items-center">
            <ActivityIndicator size="small" color={isDarkMode ? "#FFF" : "#2563EB"} />
            <Text className="mt-2">Loading discount options...</Text>
          </View>
        ) : (
          discountOptions.map((discount, index) => (
            <TouchableOpacity
              key={discount.value ? discount.value : `discount-${index}`}
              onPress={() => setSelectedDiscount(discount)}
              className={`p-3 flex-row justify-between items-center border-b ${
                isDarkMode ? "border-slate-600" : "border-slate-200"
              } ${
                selectedDiscount?.value === discount.value
                  ? isDarkMode
                    ? "bg-slate-700"
                    : "bg-blue-50"
                  : ""
              }`}
            >
              <View>
                <Text>{discount.label}</Text>
                {discount.percentage > 0 && (
                  <Text className="text-xs text-gray-500">
                    Save {discount.percentage * 100}% on your journeys
                  </Text>
                )}
              </View>
              {selectedDiscount?.value === discount.value && (
                <FontAwesome5
                  name="check"
                  size={16}
                  color={isDarkMode ? "#FFFFFF" : "#2563EB"}
                />
              )}
            </TouchableOpacity>
          ))
        )}
      </View>
    </>
  );

  return (
    <ScrollView
      className={`rounded-xl shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
      contentContainerStyle={{ padding: 20 }}
      showsVerticalScrollIndicator={false}
    >
      <Text className="text-lg font-JakartaBold mb-2">Date and Time</Text>

      {/* Commuter toggle switch */}
      <View className="flex-row items-center mb-4">
        <Text className="mr-2">Commuter Journey</Text>
        <TouchableOpacity
          onPress={() => setIsCommuter(!isCommuter)}
          className={`w-12 h-6 rounded-full ${
            isCommuter ? "bg-blue-600" : "bg-gray-300"
          } justify-center`}
        >
          <View
            className={`w-5 h-5 bg-white rounded-full ${
              isCommuter ? "ml-6" : "ml-1"
            }`}
          />
        </TouchableOpacity>
      </View>

      {/* COMMUTER JOURNEY FORM */}
      {isCommuter ? (
        <View className="mb-4">
          {/* Frequency selection */}
          <Text className="mb-2">Frequency</Text>
          <View
            className={`border rounded-lg mb-4 ${
              isDarkMode ? "border-slate-600" : "border-slate-200"
            }`}
          >
            {frequencies.map((item) => (
              <TouchableOpacity
                key={item.value}
                onPress={() => setFrequency(item.value)}
                className={`p-3 flex-row justify-between items-center border-b ${
                  isDarkMode ? "border-slate-600" : "border-slate-200"
                } ${
                  frequency === item.value
                    ? isDarkMode
                      ? "bg-slate-700"
                      : "bg-blue-50"
                    : ""
                }`}
              >
                <Text>{item.label}</Text>
                {frequency === item.value && (
                  <FontAwesome5
                    name="check"
                    size={16}
                    color={isDarkMode ? "#FFFFFF" : "#2563EB"}
                  />
                )}
              </TouchableOpacity>
            ))}
          </View>

          {/* Start date */}
          <Text className="mb-2">Start Date</Text>
          <TouchableOpacity
            onPress={() => showPicker("start")}
            className={`h-[45px] border rounded-lg px-3 justify-center mb-4 ${
              isDarkMode
                ? "bg-slate-700 border-slate-600"
                : "bg-white border-slate-200"
            }`}
          >
            <Text>{displayStartDate}</Text>
          </TouchableOpacity>

          {/* End date */}
          <Text className="mb-2">End Date</Text>
          <TouchableOpacity
            onPress={() => showPicker("end")}
            className={`h-[45px] border rounded-lg px-3 justify-center mb-4 ${
              isDarkMode
                ? "bg-slate-700 border-slate-600"
                : "bg-white border-slate-200"
            }`}
          >
            <Text>{displayEndDate}</Text>
          </TouchableOpacity>

          {/* Time */}
          <Text className="mb-2">Time</Text>
          <TouchableOpacity
            onPress={() => showPicker("time")}
            className={`h-[45px] border rounded-lg px-3 justify-center mb-4 ${
              isDarkMode
                ? "bg-slate-700 border-slate-600"
                : "bg-white border-slate-200"
            }`}
          >
            <Text>{displayTime}</Text>
          </TouchableOpacity>

          {/* Day selection */}
          <Text className="mb-2">Select Days</Text>
          {weekDays.map((day) => (
            <TouchableOpacity
              key={day}
              onPress={() => toggleDay(day)}
              className={`flex-row items-center p-2 border-b ${
                isDarkMode ? "border-slate-700" : "border-slate-200"
              }`}
            >
              <View
                className={`w-5 h-5 border rounded mr-2 ${
                  selectedDays.includes(day)
                    ? "bg-blue-600 border-blue-600"
                    : isDarkMode
                    ? "border-slate-600"
                    : "border-slate-300"
                }`}
              >
                {selectedDays.includes(day) && (
                  <FontAwesome5
                    name="check"
                    size={12}
                    color="white"
                    style={{ margin: 2 }}
                  />
                )}
              </View>
              <Text>{day}</Text>
            </TouchableOpacity>
          ))}

          {/* Discount selection */}
          {renderDiscountOptions()}
        </View>
      ) : (
        // NON-COMMUTER SINGLE JOURNEY DATE/TIME
        <TouchableOpacity
          onPress={() => showPicker("regular")}
          className={`h-[45px] border rounded-lg px-3 justify-center ${
            isDarkMode
              ? "bg-slate-700 border-slate-600"
              : "bg-white border-slate-200"
          }`}
        >
          <Text>{displayDate}</Text>
        </TouchableOpacity>
      )}

      {/* Date Time Picker - Only create the component when it's needed */}
      {showDatePicker && (
        <View>
          {Platform.OS === 'android' ? (
            // On Android, create a fresh instance every time to avoid dismiss errors
            <DateTimePicker
              key={`picker-${currentPicker}-${Date.now()}`} // Force re-creation of component
              testID="dateTimePicker"
              value={
                currentPicker === "regular"
                  ? date
                  : currentPicker === "start"
                  ? startDate
                  : currentPicker === "end"
                  ? endDate
                  : date
              }
              mode={pickerMode}
              is24Hour={true}
              display="default"
              onChange={handleDateChange}
              minimumDate={currentPicker === "end" ? startDate : undefined}
            />
          ) : (
            // iOS picker works fine with the standard approach
            <>
              <DateTimePicker
                testID="dateTimePicker"
                value={
                  currentPicker === "regular"
                    ? date
                    : currentPicker === "start"
                    ? startDate
                    : currentPicker === "end"
                    ? endDate
                    : date
                }
                mode={pickerMode}
                is24Hour={true}
                display="spinner"
                onChange={handleDateChange}
                minimumDate={currentPicker === "end" ? startDate : undefined}
              />
              <TouchableOpacity
                onPress={closePicker}
                className="mt-2 p-2 bg-blue-600 rounded-lg"
              >
                <Text className="text-white text-center">Done</Text>
              </TouchableOpacity>
            </>
          )}
        </View>
      )}
    </ScrollView>
  );
};

export default DateTimeStep;
