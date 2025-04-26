import { FontAwesome5 } from "@expo/vector-icons";
import DateTimePicker from "@react-native-community/datetimepicker";
import { useState, useEffect } from "react";
import { Platform, View, TouchableOpacity, ScrollView, ActivityIndicator } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { Discount, getDiscounts } from "@/services/paymentService";

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

interface DiscountOption {
  label: string;
  value: string | null;
  percentage: number;
  weeklyJourneys: number;
}

const defaultDiscountOption: DiscountOption = {
  label: "No Discount",
  value: null,
  percentage: 0,
  weeklyJourneys: 0,
};

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
    setSelectedDiscount,
  } = props;

  const [pickerMode, setPickerMode] = useState<"date" | "time" | "datetime">("datetime");
  const [currentPicker, setCurrentPicker] = useState<"regular" | "start" | "end" | "time">("regular");
  const [displayDate, setDisplayDate] = useState("");
  const [displayStartDate, setDisplayStartDate] = useState("");
  const [displayEndDate, setDisplayEndDate] = useState("");
  const [displayTime, setDisplayTime] = useState("");

  useEffect(() => {
    const fmtDate = (d: Date) =>
      d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
    const fmtTime = (d: Date) =>
      d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
    setDisplayDate(`${fmtDate(date)} at ${fmtTime(date)}`);
    setDisplayStartDate(fmtDate(startDate));
    setDisplayEndDate(fmtDate(endDate));
    setDisplayTime(fmtTime(date));
  }, [date, startDate, endDate]);

  const showPicker = (pickerType: "regular" | "start" | "end" | "time") => {
    setCurrentPicker(pickerType);
    if (pickerType === "time") setPickerMode("time");
    else if (pickerType === "regular") setPickerMode("datetime");
    else setPickerMode("date");
    setShowDatePicker(true);
  };

  const handleDateChange = (_: any, selected?: Date) => {
    if (Platform.OS === "android") setShowDatePicker(false);
    if (!selected) return;
    if (currentPicker === "regular") setDate(new Date(selected));
    else if (currentPicker === "start") setStartDate(selected);
    else if (currentPicker === "end") setEndDate(selected);
    else {
      const t = new Date(date);
      t.setHours(selected.getHours(), selected.getMinutes());
      setDate(t);
    }
  };

  const closePicker = () => {
    setShowDatePicker(false);
    setCurrentPicker("regular");
  };

  const toggleDay = (day: string) =>
    selectedDays.includes(day)
      ? setSelectedDays(selectedDays.filter(d => d !== day))
      : setSelectedDays([...selectedDays, day]);

  const [discountOptions, setDiscountOptions] = useState([defaultDiscountOption]);
  const [loadingDiscounts, setLoadingDiscounts] = useState(false);

  useEffect(() => {
    const fetch = async () => {
      setLoadingDiscounts(true);
      try {
        const discounts = await getDiscounts();
        if (discounts?.length) {
          const formatted = discounts
            .map<DiscountOption | null>(d =>
              d &&
              typeof d.WeeklyJourneys === "number" &&
              typeof d.DiscountPercentage === "number"
                ? {
                    label: `${d.WeeklyJourneys} Journeys/Week (${d.DiscountPercentage * 100}% off)`,
                    value: d.DiscountId,
                    percentage: d.DiscountPercentage,
                    weeklyJourneys: d.WeeklyJourneys,
                  }
                : null
            )
            .filter((d): d is DiscountOption => !!d);
          setDiscountOptions(formatted.length ? [defaultDiscountOption, ...formatted] : [defaultDiscountOption]);
        }
      } finally {
        setLoadingDiscounts(false);
      }
    };
    fetch();
  }, []);

  const renderDiscountOptions = () => (
    <>
      <Text className="mt-4 mb-2">Discount Options</Text>
      <View className={`border rounded-lg mb-4 ${isDarkMode ? "border-slate-600" : "border-slate-200"}`}>
        {loadingDiscounts ? (
          <View className="p-4 flex items-center">
            <ActivityIndicator size="small" color={isDarkMode ? "#FFF" : "#2563EB"} />
            <Text className="mt-2">Loading discount options...</Text>
          </View>
        ) : (
          discountOptions.map((disc, i) => (
            <TouchableOpacity
              key={disc.value ?? `discount-${i}`}
              onPress={() => setSelectedDiscount(disc)}
              className={`p-3 flex-row justify-between items-center border-b ${
                isDarkMode ? "border-slate-600" : "border-slate-200"
              } ${
                selectedDiscount?.value === disc.value
                  ? isDarkMode
                    ? "bg-slate-700"
                    : "bg-blue-50"
                  : ""
              }`}
            >
              <View>
                <Text>{disc.label}</Text>
                {disc.percentage > 0 && (
                  <Text className="text-xs text-gray-500">
                    Save {disc.percentage * 100}% on your journeys
                  </Text>
                )}
              </View>
              {selectedDiscount?.value === disc.value && (
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

      <View className="flex-row items-center mb-4">
        <Text className="mr-2">Commuter Journey</Text>
        <TouchableOpacity
          onPress={() => setIsCommuter(!isCommuter)}
          className={`w-12 h-6 rounded-full ${isCommuter ? "bg-blue-600" : "bg-gray-300"} justify-center`}
        >
          <View className={`w-5 h-5 bg-white rounded-full ${isCommuter ? "ml-6" : "ml-1"}`} />
        </TouchableOpacity>
      </View>

      {isCommuter ? (
        <View className="mb-4">
          <Text className="mb-2">Frequency</Text>
          <View className={`border rounded-lg mb-4 ${isDarkMode ? "border-slate-600" : "border-slate-200"}`}>
            {frequencies.map(item => (
              <TouchableOpacity
                key={item.value}
                onPress={() => setFrequency(item.value)}
                className={`p-3 flex-row justify-between items-center border-b ${
                  isDarkMode ? "border-slate-600" : "border-slate-200"
                } ${frequency === item.value ? (isDarkMode ? "bg-slate-700" : "bg-blue-50") : ""}`}
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
            onPress={() => showPicker("start")}
            className={`h-[45px] border rounded-lg px-3 justify-center mb-2 ${
              isDarkMode ? "bg-slate-700 border-slate-600" : "bg-white border-slate-200"
            }`}
          >
            <Text>{displayStartDate}</Text>
          </TouchableOpacity>
          {showDatePicker && currentPicker === "start" && (
            <View>
              {Platform.OS === "android" ? (
                <DateTimePicker
                  key={`picker-${currentPicker}-${Date.now()}`}
                  testID="dateTimePicker"
                  value={startDate}
                  mode="date"
                  is24Hour={true}
                  display="default"
                  onChange={handleDateChange}
                  minimumDate={new Date()}
                />
              ) : (
                <>
                  <DateTimePicker
                    style={{ padding: 10 }}
                    testID="dateTimePicker"
                    value={startDate}
                    themeVariant={isDarkMode ? "dark" : "light"}
                    textColor={isDarkMode ? "#ffffff" : "#000000"}
                    mode="date"
                    display="inline"
                    onChange={handleDateChange}
                    minimumDate={new Date()}
                  />
                  <TouchableOpacity onPress={closePicker} className="p-1 bg-blue-600 rounded-full mb-1">
                    <Text className="text-white text-center">Done</Text>
                  </TouchableOpacity>
                </>
              )}
            </View>
          )}

          <Text className="mb-2">End Date</Text>
          <TouchableOpacity
            onPress={() => showPicker("end")}
            className={`h-[45px] border rounded-lg px-3 justify-center mb-2 ${
              isDarkMode ? "bg-slate-700 border-slate-600" : "bg-white border-slate-200"
            }`}
          >
            <Text>{displayEndDate}</Text>
          </TouchableOpacity>
          {showDatePicker && currentPicker === "end" && (
            <View>
              {Platform.OS === "android" ? (
                <DateTimePicker
                  key={`picker-${currentPicker}-${Date.now()}`}
                  testID="dateTimePicker"
                  value={endDate}
                  mode="date"
                  is24Hour={true}
                  display="default"
                  onChange={handleDateChange}
                  minimumDate={startDate}
                />
              ) : (
                <>
                  <DateTimePicker
                    style={{ padding: 10 }}
                    testID="dateTimePicker"
                    value={endDate}
                    themeVariant={isDarkMode ? "dark" : "light"}
                    textColor={isDarkMode ? "#ffffff" : "#000000"}
                    mode="date"
                    display="inline"
                    onChange={handleDateChange}
                    minimumDate={startDate}
                  />
                  <TouchableOpacity onPress={closePicker} className="p-1 bg-blue-600 rounded-full mb-1">
                    <Text className="text-white text-center">Done</Text>
                  </TouchableOpacity>
                </>
              )}
            </View>
          )}

          <Text className="mb-2">Time</Text>
          <TouchableOpacity
            onPress={() => showPicker("time")}
            className={`h-[45px] border rounded-lg px-3 justify-center mb-2 ${
              isDarkMode ? "bg-slate-700 border-slate-600" : "bg-white border-slate-200"
            }`}
          >
            <Text>{displayTime}</Text>
          </TouchableOpacity>
          {showDatePicker && currentPicker === "time" && (
            <View>
              {Platform.OS === "android" ? (
                <DateTimePicker
                  key={`picker-${currentPicker}-${Date.now()}`}
                  testID="dateTimePicker"
                  value={date}
                  mode="time"
                  is24Hour={true}
                  display="default"
                  onChange={handleDateChange}
                />
              ) : (
                <>
                  <DateTimePicker
                    style={{ padding: 10 }}
                    testID="dateTimePicker"
                    value={date}
                    themeVariant={isDarkMode ? "dark" : "light"}
                    textColor={isDarkMode ? "#ffffff" : "#000000"}
                    mode="time"
                    display="spinner"
                    onChange={handleDateChange}
                  />
                  <TouchableOpacity onPress={closePicker} className="p-1 bg-blue-600 rounded-full mb-1">
                    <Text className="text-white text-center">Done</Text>
                  </TouchableOpacity>
                </>
              )}
            </View>
          )}

          <Text className="mb-2">Select Days</Text>
          {weekDays.map(day => (
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
                  <FontAwesome5 name="check" size={12} color="white" style={{ margin: 2 }} />
                )}
              </View>
              <Text>{day}</Text>
            </TouchableOpacity>
          ))}

          {renderDiscountOptions()}
        </View>
      ) : (
        <>
          <TouchableOpacity
            onPress={() => showPicker("regular")}
            className={`h-[45px] border rounded-lg px-3 justify-center ${
              isDarkMode ? "bg-slate-700 border-slate-600" : "bg-white border-slate-200"
            }`}
          >
            <Text>{displayDate}</Text>
          </TouchableOpacity>
          {showDatePicker && (
            <View>
              {Platform.OS === "android" ? (
                <DateTimePicker
                  key={`picker-${currentPicker}-${Date.now()}`}
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
                  minimumDate={currentPicker === "end" ? endDate : new Date()}
                />
              ) : (
                <>
                  <DateTimePicker
                    style={{ padding: 10 }}
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
                    themeVariant={isDarkMode ? "dark" : "light"}
                    textColor={isDarkMode ? "#ffffff" : "#000000"}
                    mode={pickerMode}
                    display="inline"
                    onChange={handleDateChange}
                    minimumDate={currentPicker === "end" ? endDate : new Date()}
                  />
                  <TouchableOpacity onPress={closePicker} className="p-1 bg-blue-600 rounded-full mb-1">
                    <Text className="text-white text-center">Done</Text>
                  </TouchableOpacity>
                </>
              )}
            </View>
          )}
        </>
      )}
    </ScrollView>
  );
};

export default DateTimeStep;
