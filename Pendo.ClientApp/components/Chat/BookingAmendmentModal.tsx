import React, { useState, useEffect } from 'react';
import { Modal, View, TouchableOpacity, TextInput, ScrollView, Switch, Platform } from 'react-native';
import { Text } from '@/components/common/ThemedText';
import { FontAwesome5 } from '@expo/vector-icons';
import { useTheme } from '@/context/ThemeContext';
import { AddBookingAmmendmentRequest } from '@/services/bookingService';
import DateTimePicker from '@react-native-community/datetimepicker';
import { getBookings } from '@/services/bookingService';
import { Picker } from '@react-native-picker/picker';

interface BookingAmendmentModalProps {
  visible: boolean;
  onClose: () => void;
  onSubmit: (amendment: AddBookingAmmendmentRequest) => void;
}

const BookingAmendmentModal: React.FC<BookingAmendmentModalProps> = ({
  visible,
  onClose,
  onSubmit
}) => {
  const { isDarkMode } = useTheme();
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [showDatePicker, setShowDatePicker] = useState(false);
  
  // Amendment form state
  const [selectedBookingId, setSelectedBookingId] = useState<string>('');
  const [isCancellation, setIsCancellation] = useState(false);
  const [newPrice, setNewPrice] = useState<string>('');
  const [newStartName, setNewStartName] = useState<string>('');
  const [newStartLat, setNewStartLat] = useState<string>('');
  const [newStartLong, setNewStartLong] = useState<string>('');
  const [newEndName, setNewEndName] = useState<string>('');
  const [newEndLat, setNewEndLat] = useState<string>('');
  const [newEndLong, setNewEndLong] = useState<string>('');
  const [newStartTime, setNewStartTime] = useState<Date>(new Date());
  
  // Load user's bookings when modal opens
  useEffect(() => {
    if (visible) {
      fetchUserBookings();
    }
  }, [visible]);
  
  const fetchUserBookings = async () => {
    setLoading(true);
    try {
      const result = await getBookings();
      if (result.success) {
        // Filter only pending or confirmed bookings
        const activeBookings = result.bookings.filter(
          b => b.BookingStatus.Status === 'Pending' || b.BookingStatus.Status === 'Confirmed'
        );
        setBookings(activeBookings);
        if (activeBookings.length > 0) {
          setSelectedBookingId(activeBookings[0].Booking.BookingId);
        }
      }
    } catch (error) {
      console.error('Error fetching bookings:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleSubmit = () => {
    if (!selectedBookingId) {
      return;
    }
    
    // Format the datetime without timezone information
    let formattedStartTime = null;
    if (newStartTime) {
      // Format as YYYY-MM-DDTHH:MM:SS format without timezone (Z)
      formattedStartTime = newStartTime.toISOString().split('.')[0];
    }
    
    const amendment: AddBookingAmmendmentRequest = {
      BookingId: selectedBookingId,
      CancellationRequest: isCancellation,
      ProposedPrice: newPrice ? parseFloat(newPrice) : null,
      StartName: newStartName || null,
      StartLat: newStartLat ? parseFloat(newStartLat) : null,
      StartLong: newStartLong ? parseFloat(newStartLong) : null,
      EndName: newEndName || null,
      EndLat: newEndLat ? parseFloat(newEndLat) : null,
      EndLong: newEndLong ? parseFloat(newEndLong) : null,
      StartTime: formattedStartTime,
      DriverApproval: false,
      PassengerApproval: true // Passenger is making the request
    };
    
    onSubmit(amendment);
  };
  
  const resetForm = () => {
    setIsCancellation(false);
    setNewPrice('');
    setNewStartName('');
    setNewStartLat('');
    setNewStartLong('');
    setNewEndName('');
    setNewEndLat('');
    setNewEndLong('');
    setNewStartTime(new Date());
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
            <Text className="text-xl font-JakartaBold">Request Booking Amendment</Text>
            <TouchableOpacity onPress={onClose}>
              <FontAwesome5 name="times" size={24} color={isDarkMode ? '#FFF' : '#000'} />
            </TouchableOpacity>
          </View>
          
          <ScrollView className="max-h-[70vh]">
            {loading ? (
              <Text className="text-center py-4">Loading bookings...</Text>
            ) : bookings.length === 0 ? (
              <Text className="text-center py-4">No active bookings found</Text>
            ) : (
              <>
                {/* Booking Selection */}
                <View className="mb-4">
                  <Text className="mb-2 font-JakartaMedium">Select Booking</Text>
                  <View className={`border rounded-lg ${isDarkMode ? 'border-slate-600 bg-slate-700' : 'border-gray-300 bg-gray-50'}`}>
                    <Picker
                      selectedValue={selectedBookingId}
                      onValueChange={(itemValue) => setSelectedBookingId(itemValue)}
                      style={{ color: isDarkMode ? '#FFF' : '#000' }}
                    >
                      {bookings.map((booking) => (
                        <Picker.Item 
                          key={booking.Booking.BookingId} 
                          label={`${booking.Journey.StartName} to ${booking.Journey.EndName}`} 
                          value={booking.Booking.BookingId} 
                        />
                      ))}
                    </Picker>
                  </View>
                </View>
                
                {/* Cancellation Switch */}
                <View className="mb-4 flex-row justify-between items-center">
                  <Text className="font-JakartaMedium">Request Cancellation</Text>
                  <Switch
                    value={isCancellation}
                    onValueChange={setIsCancellation}
                    trackColor={{ false: '#767577', true: '#81b0ff' }}
                    thumbColor={isCancellation ? '#2563EB' : '#f4f3f4'}
                  />
                </View>
                
                {!isCancellation && (
                  <>
                    {/* Price Amendment */}
                    <View className="mb-4">
                      <Text className="mb-2 font-JakartaMedium">New Price (Optional)</Text>
                      <TextInput
                        className={`p-3 rounded-lg ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                        value={newPrice}
                        onChangeText={setNewPrice}
                        placeholder="Enter new price"
                        placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                        keyboardType="numeric"
                      />
                    </View>
                    
                    {/* Start Location */}
                    <View className="mb-4">
                      <Text className="mb-2 font-JakartaMedium">New Pickup Location (Optional)</Text>
                      <TextInput
                        className={`p-3 mb-2 rounded-lg ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                        value={newStartName}
                        onChangeText={setNewStartName}
                        placeholder="Location name"
                        placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                      />
                      <View className="flex-row">
                        <TextInput
                          className={`p-3 rounded-lg flex-1 mr-2 ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                          value={newStartLat}
                          onChangeText={setNewStartLat}
                          placeholder="Latitude"
                          placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                          keyboardType="numeric"
                        />
                        <TextInput
                          className={`p-3 rounded-lg flex-1 ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                          value={newStartLong}
                          onChangeText={setNewStartLong}
                          placeholder="Longitude"
                          placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                          keyboardType="numeric"
                        />
                      </View>
                    </View>
                    
                    {/* End Location */}
                    <View className="mb-4">
                      <Text className="mb-2 font-JakartaMedium">New Destination (Optional)</Text>
                      <TextInput
                        className={`p-3 mb-2 rounded-lg ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                        value={newEndName}
                        onChangeText={setNewEndName}
                        placeholder="Location name"
                        placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                      />
                      <View className="flex-row">
                        <TextInput
                          className={`p-3 rounded-lg flex-1 mr-2 ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                          value={newEndLat}
                          onChangeText={setNewEndLat}
                          placeholder="Latitude"
                          placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                          keyboardType="numeric"
                        />
                        <TextInput
                          className={`p-3 rounded-lg flex-1 ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                          value={newEndLong}
                          onChangeText={setNewEndLong}
                          placeholder="Longitude"
                          placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                          keyboardType="numeric"
                        />
                      </View>
                    </View>
                    
                    {/* Date/Time Picker */}
                    <View className="mb-4">
                      <Text className="mb-2 font-JakartaMedium">New Departure Time (Optional)</Text>
                      <TouchableOpacity 
                        className={`p-3 rounded-lg flex-row justify-between ${isDarkMode ? 'bg-slate-700 border-slate-600' : 'bg-gray-50 border-gray-300'} border`}
                        onPress={() => setShowDatePicker(true)}
                      >
                        <Text>{newStartTime.toLocaleString()}</Text>
                        <FontAwesome5 name="calendar-alt" size={18} color={isDarkMode ? '#FFF' : '#000'} />
                      </TouchableOpacity>
                      
                      {showDatePicker && (
                        Platform.OS === 'android' ? (
                          <DateTimePicker
                            key={`picker-${Date.now()}`} // Force re-creation of component
                            value={newStartTime}
                            mode="datetime"
                            display="default"
                            onChange={(event, selectedDate) => {
                              // Close picker first to avoid the dismiss error
                              setShowDatePicker(false);
                              
                              // Then update the date if one was selected
                              if (selectedDate) {
                                setNewStartTime(selectedDate);
                              }
                            }}
                          />
                        ) : (
                          <View>
                            <DateTimePicker
                              value={newStartTime}
                              mode="datetime"
                              display="spinner"
                              onChange={(event, selectedDate) => {
                                if (selectedDate) {
                                  setNewStartTime(selectedDate);
                                }
                              }}
                            />
                            <TouchableOpacity
                              onPress={() => setShowDatePicker(false)}
                              className="mt-2 p-2 bg-blue-600 rounded-lg"
                            >
                              <Text className="text-white text-center">Done</Text>
                            </TouchableOpacity>
                          </View>
                        )
                      )}
                    </View>
                  </>
                )}
                
                {/* Submit Button */}
                <TouchableOpacity
                  className="bg-blue-600 p-4 rounded-xl mb-4"
                  onPress={handleSubmit}
                >
                  <Text className="text-white text-center font-JakartaBold">
                    {isCancellation ? 'Request Cancellation' : 'Request Amendment'}
                  </Text>
                </TouchableOpacity>
              </>
            )}
          </ScrollView>
        </View>
      </View>
    </Modal>
  );
};

export default BookingAmendmentModal;
