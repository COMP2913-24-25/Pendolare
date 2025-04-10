import React, { useState, useEffect } from 'react';
import { Modal, View, TouchableOpacity, ScrollView, Alert, Platform } from 'react-native';
import { Text } from '@/components/common/ThemedText';
import { FontAwesome5 } from '@expo/vector-icons';
import { useTheme } from '@/context/ThemeContext';
import { AddBookingAmmendmentRequest, addBookingAmmendment, approveBookingAmmendment, BookingDetails, User } from '@/services/bookingService';
import DateTimePicker from '@react-native-community/datetimepicker';
import { getCurrentUserId } from '@/services/authService';
import { Picker } from '@react-native-picker/picker';
import { messageService } from '@/services/messageService';
import { toHumanReadable, toCronString } from '@/utils/cronTools';

interface CommuterScheduleAmendmentModalProps {
  visible: boolean;
  onClose: () => void;
  booking: BookingDetails;
  isDriver?: boolean;
}

/*
  CommuterScheduleAmendmentModal
  Modal for requesting amendments to a commuter schedule
*/
const CommuterScheduleAmendmentModal: React.FC<CommuterScheduleAmendmentModalProps> = ({
  visible,
  onClose,
  booking,
  isDriver = false
}) => {
  const { isDarkMode } = useTheme();
  const [loading, setLoading] = useState(false);
  const [currentUserId, setCurrentUserId] = useState<string>("");
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [datePickerMode, setDatePickerMode] = useState<'date' | 'time'>('date');
  
  // Safely extract journey and booking data with proper null checks
  const journey = booking?.Journey || {};
  const rideDetails = booking?.Booking || {};
  
  // Initialise with a default Date object to ensure it's never undefined
  const defaultDate = new Date();
  
  // Safely initialise frequency with a fallback
  const [frequency, setFrequency] = useState<'weekly' | 'fortnightly' | 'monthly'>(
    journey.Recurrance?.includes('*/14') ? 'fortnightly' : 
    journey.Recurrance?.includes('*') ? 'weekly' : 'monthly'
  );
  
  const [days, setDays] = useState<string[]>([]);
  
  // Safely initialise dates with fallbacks
  const [endDate, setEndDate] = useState<Date>(
    journey.RepeatUntil instanceof Date ? journey.RepeatUntil :
    typeof journey.RepeatUntil === 'string' ? new Date(journey.RepeatUntil) :
    defaultDate
  );
  
  // Always ensure startTime has a valid Date object
  const [startTime, setStartTime] = useState<Date>(() => {
    if (rideDetails.RideTime instanceof Date) {
      return rideDetails.RideTime;
    } else if (typeof rideDetails.RideTime === 'string') {
      try {
        return new Date(rideDetails.RideTime);
      } catch (e) {
        console.error("Error parsing ride time:", e);
        return defaultDate;
      }
    } else {
      return defaultDate;
    }
  });
  
  // Weekday selection
  const [selectedDays, setSelectedDays] = useState<{[key: string]: boolean}>({
    '0': false, // Sunday
    '1': false, // Monday
    '2': false, // Tuesday
    '3': false, // Wednesday
    '4': false, // Thursday
    '5': false, // Friday
    '6': false  // Saturday
  });
  
  // Get current user ID
  useEffect(() => {
    const getUserId = async () => {
      try {
        const userId = await getCurrentUserId();
        if (userId) {
          setCurrentUserId(userId);
        }
      } catch (error) {
        console.error("Failed to get user ID:", error);
      }
    };

    getUserId();
  }, []);
  
  // Parse existing cron expression when modal opens
  useEffect(() => {
    if (visible && journey.Recurrance) {
      try {
        parseCronExpression(journey.Recurrance);
      } catch (error) {
        console.error("Error parsing cron expression:", error);
      }
    }
  }, [visible, journey.Recurrance]);
  
  // Parse the cron expression to set initial form values
  const parseCronExpression = (cronExpression: string) => {
    const parts = cronExpression.split(' ');
    
    // Parse minutes and hours for time
    const minutes = parseInt(parts[0]);
    const hours = parseInt(parts[1]);
    const newTime = new Date();
    newTime.setHours(hours, minutes, 0, 0);
    setStartTime(newTime);
    
    // Determine frequency
    if (parts[2].includes('*/14')) {
      setFrequency('fortnightly');
    } else if (parts[2] !== '*') {
      setFrequency('monthly');
    } else {
      setFrequency('weekly');
    }
    
    // Parse days of week if weekly
    if (parts[4] !== '*') {
      const daysList = parts[4].split(',');
      setDays(daysList);
      
      // Update selected days
      const newSelectedDays = { ...selectedDays };
      daysList.forEach(day => {
        newSelectedDays[day] = true;
      });
      setSelectedDays(newSelectedDays);
    }
  };
  
  // Toggle a weekday selection
  const toggleDay = (day: string) => {
    const newSelectedDays = { ...selectedDays };
    newSelectedDays[day] = !newSelectedDays[day];
    setSelectedDays(newSelectedDays);
    
    // Update days array based on selection
    const newDays = Object.keys(newSelectedDays).filter(key => newSelectedDays[key]);
    setDays(newDays);
  };
  
  // Handle date picker changes
  const handleDateChange = (event: any, selectedDate?: Date) => {
    setShowDatePicker(Platform.OS === 'ios');
    
    if (selectedDate) {
      if (datePickerMode === 'date') {
        const newDate = new Date(endDate);
        newDate.setFullYear(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());
        setEndDate(newDate);
      } else {
        const newTime = new Date(startTime);
        newTime.setHours(selectedDate.getHours(), selectedDate.getMinutes(), 0, 0);
        setStartTime(newTime);
      }
    }
  };
  
  // Show date picker
  const showPicker = (mode: 'date' | 'time') => {
    setDatePickerMode(mode);
    setShowDatePicker(true);
  };
  
  // Generate the new cron expression based on form values
  const generateCronExpression = () => {
    // Ensure at least one day is selected for weekly frequency
    const daysList = Object.keys(selectedDays).filter(key => selectedDays[key]);
    
    if (frequency === 'weekly' && daysList.length === 0) {
      // Default to the current day if none selected
      const currentDay = new Date().getDay().toString();
      daysList.push(currentDay);
    }
    
    return toCronString(frequency, daysList, startTime);
  };
  
  // Preview the human-readable schedule
  const getSchedulePreview = () => {
    try {
      const cronExpression = generateCronExpression();
      return toHumanReadable(cronExpression);
    } catch (error) {
      return "Invalid schedule";
    }
  };
  
  // Submit the schedule amendment
  const handleSubmit = async () => {
    try {
      setLoading(true);
      
      // Generate new cron expression
      const newCronExpression = generateCronExpression();
      
      // Create schedule amendment request
      const amendmentRequest: AddBookingAmmendmentRequest = {
        BookingId: rideDetails.BookingId,
        CancellationRequest: false,
        // Standard fields set to null as they are not needed for schedule amendments
        ProposedPrice: null,
        StartName: null,
        StartLat: null,
        StartLong: null,
        EndName: null,
        EndLat: null,
        EndLong: null,
        StartTime: null,
        // Set approval flags based on who is creating the amendment
        DriverApproval: isDriver,
        PassengerApproval: !isDriver,
        // Add schedule-specific fields
        ScheduleAmendment: true,
        RecurrenceCron: newCronExpression,
        RepeatUntil: endDate.toISOString()
      };
      
      // Save the amendment
      const result = await addBookingAmmendment(amendmentRequest);
      
      if (result.success || result.Status === "Success") {
        // Get the amendment ID
        const amendmentId = result.id || result.BookingAmmendmentId || "";
        
        // Auto-approve for the requester
        const approvalResult = await approveBookingAmmendment(
          amendmentId,
          false,
          isDriver
        );
        
        if (!approvalResult.success) {
          console.error("Failed to auto-approve schedule amendment:", approvalResult.message);
        }
        
        // Get driver ID from the journey
        const user = journey.User as User;
        const driverId = user.UserId;
        
        // Create a special message for the chat
        const amendmentMessage = {
          type: "booking_amendment",
          from: currentUserId,
          conversation_id: driverId, // Use driver ID as conversation ID
          content: JSON.stringify(amendmentRequest),
          amendmentId: amendmentId,
          timestamp: new Date().toISOString(),
          requesterApproved: true
        };
        
        // Send message to chat if there is a connection
        if (messageService && messageService.sendMessage) {
          messageService.sendMessage(JSON.stringify(amendmentMessage));
        }
        
        // Close modal and show success alert
        setLoading(false);
        onClose();
        Alert.alert(
          "Schedule Amendment Requested",
          "Your schedule amendment request has been sent successfully.",
          [{ text: "OK" }]
        );
      } else {
        throw new Error(result.message || "Unknown error");
      }
    } catch (error) {
      setLoading(false);
      Alert.alert(
        "Error",
        `Failed to request schedule amendment: ${error instanceof Error ? error.message : "Unknown error"}`,
        [{ text: "OK" }]
      );
    }
  };
  
  // Render weekday buttons
  const renderWeekdayButtons = () => {
    const weekdays = [
      { key: '0', label: 'S', fullName: 'Sunday' },
      { key: '1', label: 'M', fullName: 'Monday' },
      { key: '2', label: 'T', fullName: 'Tuesday' },
      { key: '3', label: 'W', fullName: 'Wednesday' },
      { key: '4', label: 'T', fullName: 'Thursday' },
      { key: '5', label: 'F', fullName: 'Friday' },
      { key: '6', label: 'S', fullName: 'Saturday' }
    ];
    
    return (
      <View className="flex-row justify-between my-3">
        {weekdays.map(day => (
          <TouchableOpacity
            key={day.key}
            className={`w-10 h-10 rounded-full justify-center items-center ${
              selectedDays[day.key]
                ? 'bg-blue-600'
                : isDarkMode
                  ? 'bg-slate-700'
                  : 'bg-gray-200'
            }`}
            onPress={() => toggleDay(day.key)}
          >
            <Text
              className={`text-center ${
                selectedDays[day.key] ? 'text-white' : ''
              }`}
            >
              {day.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    );
  };

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="slide"
      onRequestClose={onClose}
    >
      <View className="flex-1 justify-end">
        <View className={`rounded-t-3xl p-5 ${isDarkMode ? 'bg-slate-800' : 'bg-white'}`}> 
          <View className="flex-row justify-between items-center mb-5">
            <Text className="text-xl font-JakartaBold">
              Amend Commuter Schedule
            </Text>
            <TouchableOpacity onPress={onClose}>
              <FontAwesome5 name="times" size={24} color={isDarkMode ? '#FFF' : '#000'} />
            </TouchableOpacity>
          </View>
          
          {/* User role indicator */}
          <View className={`mb-3 py-1 px-3 self-start rounded-full ${
            isDriver ? 'bg-blue-500' : 'bg-green-500'
          }`}>
            <Text className="text-white text-sm">
              {isDriver ? 'Driver Amendment' : 'Passenger Amendment'}
            </Text>
          </View>
          
          <ScrollView className="max-h-[70vh]">
            {/* Current schedule */}
            <View className="mb-4">
              <Text className="font-JakartaMedium mb-2">Current Schedule</Text>
              <View className={`p-3 rounded-lg ${isDarkMode ? 'bg-slate-700' : 'bg-gray-100'}`}>
                <Text>{journey.Recurrance ? toHumanReadable(journey.Recurrance) : 'No recurring schedule'}</Text>
                {journey.RepeatUntil && (
                  <Text className="mt-1">
                    Until {new Date(journey.RepeatUntil).toLocaleDateString()}
                  </Text>
                )}
              </View>
            </View>
            
            {/* Frequency selection */}
            <View className="mb-4">
              <Text className="font-JakartaMedium mb-2">Frequency</Text>
              <View className={`border rounded-lg ${isDarkMode ? 'border-slate-600 bg-slate-700' : 'border-gray-300 bg-gray-50'}`}>
                <Picker
                  selectedValue={frequency}
                  onValueChange={(itemValue) => setFrequency(itemValue)}
                  style={{ color: isDarkMode ? '#FFF' : '#000' }}
                >
                  <Picker.Item label="Weekly" value="weekly" />
                  <Picker.Item label="Fortnightly" value="fortnightly" />
                  <Picker.Item label="Monthly" value="monthly" />
                </Picker>
              </View>
            </View>
            
            {/* Day selection for weekly/fortnightly */}
            {frequency !== 'monthly' && (
              <View className="mb-4">
                <Text className="font-JakartaMedium mb-2">Days of Week</Text>
                {renderWeekdayButtons()}
              </View>
            )}
            
            {/* Time picker */}
            <View className="mb-4">
              <Text className="font-JakartaMedium mb-2">Departure Time</Text>
              <TouchableOpacity 
                className={`p-3 rounded-lg flex-row justify-between ${isDarkMode ? 'bg-slate-700 border-slate-600' : 'bg-gray-50 border-gray-300'} border`}
                onPress={() => showPicker('time')}
              >
                <Text>
                  {startTime ? 
                    startTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 
                    "Select time"}
                </Text>
                <FontAwesome5 name="clock" size={18} color={isDarkMode ? '#FFF' : '#000'} />
              </TouchableOpacity>
            </View>
            
            {/* End date picker */}
            <View className="mb-4">
              <Text className="font-JakartaMedium mb-2">Repeat Until</Text>
              <TouchableOpacity 
                className={`p-3 rounded-lg flex-row justify-between ${isDarkMode ? 'bg-slate-700 border-slate-600' : 'bg-gray-50 border-gray-300'} border`}
                onPress={() => showPicker('date')}
              >
                <Text>{endDate.toLocaleDateString()}</Text>
                <FontAwesome5 name="calendar-alt" size={18} color={isDarkMode ? '#FFF' : '#000'} />
              </TouchableOpacity>
            </View>
            
            {/* Schedule preview */}
            <View className="mb-4">
              <Text className="font-JakartaMedium mb-2">New Schedule Preview</Text>
              <View className={`p-3 rounded-lg ${isDarkMode ? 'bg-indigo-900' : 'bg-indigo-100'}`}>
                <Text className={isDarkMode ? 'text-white' : 'text-indigo-900'}>
                  {getSchedulePreview()}
                </Text>
                <Text className={`mt-1 ${isDarkMode ? 'text-white' : 'text-indigo-900'}`}>
                  Until {endDate.toLocaleDateString()}
                </Text>
              </View>
            </View>
            
            {/* Submit button */}
            <TouchableOpacity
              className={`bg-blue-600 p-4 rounded-xl mb-4 ${loading ? 'opacity-70' : ''}`}
              onPress={handleSubmit}
              disabled={loading}
            >
              <Text className="text-white text-center font-JakartaBold">
                {loading ? 'Submitting...' : 'Request Schedule Amendment'}
              </Text>
            </TouchableOpacity>
          </ScrollView>
          
          {/* Date/Time picker for iOS */}
          {showDatePicker && Platform.OS === 'ios' && (
            <View>
              <DateTimePicker
                value={datePickerMode === 'date' ? 
                  (endDate || defaultDate) : 
                  (startTime || defaultDate)}
                mode={datePickerMode}
                display="spinner"
                onChange={handleDateChange}
              />
              <TouchableOpacity
                onPress={() => setShowDatePicker(false)}
                className="mt-2 p-2 bg-blue-600 rounded-lg"
              >
                <Text className="text-white text-center">Done</Text>
              </TouchableOpacity>
            </View>
          )}
          
          {/* Date/Time picker for Android */}
          {showDatePicker && Platform.OS === 'android' && (
            <DateTimePicker
              value={datePickerMode === 'date' ? 
                (endDate || defaultDate) : 
                (startTime || defaultDate)}
              mode={datePickerMode}
              display="default"
              onChange={handleDateChange}
            />
          )}
        </View>
      </View>
    </Modal>
  );
};

export default CommuterScheduleAmendmentModal;
