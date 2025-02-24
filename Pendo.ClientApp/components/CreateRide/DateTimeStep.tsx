import { FontAwesome5 } from "@expo/vector-icons";
import DateTimePicker from "@react-native-community/datetimepicker";
import React, { useState } from "react";
import { View, TouchableOpacity, ScrollView } from "react-native";

import { Text } from "@/components/ThemedText";

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
}

const DateTimeStep = ({
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
}: DateTimeStepProps) => {
  const [datePickerMode, setDatePickerMode] = useState<
    "time" | "date" | "datetime"
  >("datetime");
  const [activeDatePicker, setActiveDatePicker] = useState<
    "time" | "start" | "end" | null
  >(null);

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

  const handleDatePickerShow = (type: "time" | "start" | "end") => {
    setActiveDatePicker(type);
    setDatePickerMode(type === "time" ? "time" : "date");
    setShowDatePicker(true);
  };

  const handleDatePickerChange = (event: any, selectedDate?: Date) => {
    setShowDatePicker(false);
    if (selectedDate) {
      switch (activeDatePicker) {
        case "time":
          setDate(selectedDate);
          break;
        case "start":
          setStartDate(selectedDate);
          break;
        case "end":
          setEndDate(selectedDate);
          break;
      }
    }
    setActiveDatePicker(null);
  };

  return (
    <ScrollView
      className={`rounded-xl shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
      contentContainerStyle={{ padding: 20 }}
      showsVerticalScrollIndicator={false}
    >
      <Text className="text-lg font-JakartaBold mb-2">Date and Time</Text>

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

      {isCommuter ? (
        <View className="mb-4">
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

          <Text className="mb-2">Start Date</Text>
          <TouchableOpacity
            onPress={() => handleDatePickerShow("start")}
            className={`h-[45px] border rounded-lg px-3 justify-center mb-4 ${
              isDarkMode
                ? "bg-slate-700 border-slate-600"
                : "bg-white border-slate-200"
            }`}
          >
            <Text className={isDarkMode ? "text-white" : "text-black"}>
              {startDate.toLocaleDateString()}
            </Text>
          </TouchableOpacity>

          <Text className="mb-2">End Date</Text>
          <TouchableOpacity
            onPress={() => handleDatePickerShow("end")}
            className={`h-[45px] border rounded-lg px-3 justify-center mb-4 ${
              isDarkMode
                ? "bg-slate-700 border-slate-600"
                : "bg-white border-slate-200"
            }`}
          >
            <Text className={isDarkMode ? "text-white" : "text-black"}>
              {endDate.toLocaleDateString()}
            </Text>
          </TouchableOpacity>

          <Text className="mb-2">Time</Text>
          <TouchableOpacity
            onPress={() => handleDatePickerShow("time")}
            className={`h-[45px] border rounded-lg px-3 justify-center mb-4 ${
              isDarkMode
                ? "bg-slate-700 border-slate-600"
                : "bg-white border-slate-200"
            }`}
          >
            <Text className={isDarkMode ? "text-white" : "text-black"}>
              {date.toLocaleTimeString()}
            </Text>
          </TouchableOpacity>

          <Text className="mb-2">Select Days</Text>
          {weekDays.map((day) => (
            <TouchableOpacity
              key={day}
              onPress={() => {
                setSelectedDays(
                  selectedDays.includes(day)
                    ? selectedDays.filter((d) => d !== day)
                    : [...selectedDays, day],
                );
              }}
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
        </View>
      ) : (
        <TouchableOpacity
          onPress={() => setShowDatePicker(true)}
          className={`h-[45px] border rounded-lg px-3 justify-center ${
            isDarkMode
              ? "bg-slate-700 border-slate-600"
              : "bg-white border-slate-200"
          }`}
        >
          <Text className={isDarkMode ? "text-white" : "text-black"}>
            {date.toLocaleString()}
          </Text>
        </TouchableOpacity>
      )}

      {showDatePicker && (
        <DateTimePicker
          value={
            activeDatePicker === "time"
              ? date
              : activeDatePicker === "start"
                ? startDate
                : endDate
          }
          mode={datePickerMode}
          display="default"
          onChange={handleDatePickerChange}
          minimumDate={activeDatePicker === "end" ? startDate : undefined}
        />
      )}
    </ScrollView>
  );
};

export default DateTimeStep;
