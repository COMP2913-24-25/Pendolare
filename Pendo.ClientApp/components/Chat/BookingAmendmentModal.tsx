import React, { useState, useEffect } from 'react';
import { Modal, View, TouchableOpacity, TextInput, ScrollView, Switch, Platform } from 'react-native';
import { Text } from '@/components/common/ThemedText';
import { FontAwesome5 } from '@expo/vector-icons';
import { useTheme } from '@/context/ThemeContext';
import { AddBookingAmendmentRequest } from '@/services/bookingService';
import DateTimePicker from '@react-native-community/datetimepicker';
import { getBookings } from '@/services/bookingService';
import { Picker } from '@react-native-picker/picker';
import { searchLocations } from '@/services/locationService';

interface Location {
  name: string;
  latitude: number;
  longitude: number;
}

interface BookingAmendmentModalProps {
  visible: boolean;
  onClose: () => void;
  onSubmit: (amendment: AddBookingAmendmentRequest) => void;
  isDriver?: boolean;
}

const BookingAmendmentModal: React.FC<BookingAmendmentModalProps> = ({
  visible,
  onClose,
  onSubmit,
  isDriver = false // Default to passenger view
}) => {
  const { isDarkMode } = useTheme();
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [isTimeModified, setIsTimeModified] = useState(false);
  const [searchResults, setSearchResults] = useState<Location[]>([]);
  const [searching, setSearching] = useState<string | null>(null);
  
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
      resetForm();
    }
  }, [visible]);
  
  const fetchUserBookings = async () => {
    setLoading(true);
    try {
      // Pass the driverView parameter based on user role
      const result = await getBookings(isDriver);
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
  
  const handleLocationSearch = (text: string, type: 'pickup' | 'dropoff') => {
    if (text.length < 3) {
      setSearchResults([]);
      setSearching(null);
      return;
    }
    
    searchLocations(
      text,
      type,
      (searchType: string) => setSearching(searchType),
      (results: Location[]) => {
        setSearchResults(results);
      }
    );
  };
  
  const handleLocationSelect = (location: Location) => {
    if (searching === 'pickup') {
      setNewStartName(location.name);
      setNewStartLat(location.latitude.toString());
      setNewStartLong(location.longitude.toString());
    } else if (searching === 'dropoff') {
      setNewEndName(location.name);
      setNewEndLat(location.latitude.toString());
      setNewEndLong(location.longitude.toString());
    }
    setSearchResults([]);
    setSearching(null);
  };
  
  const handleSubmit = () => {
    if (!selectedBookingId) {
      return;
    }
    
    // Only include StartTime if user has modified it
    let formattedStartTime = null;
    if (isTimeModified) {
      formattedStartTime = newStartTime.toISOString().split('.')[0];
    }
    
    const amendment: AddBookingAmendmentRequest = {
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
      // Set approval flags based on who is creating the amendment
      DriverApproval: isDriver,
      PassengerApproval: !isDriver
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
    setIsTimeModified(false);
    setSearchResults([]);
    setSearching(null);
  };
  
  const renderSearchResults = () => {
    if (!searching || searchResults.length === 0) return null;

    return (
      <View 
        className={`absolute left-0 right-0 z-50 ${
          isDarkMode ? 'bg-slate-800' : 'bg-white'
        } rounded-lg shadow-lg ${
          searching === 'pickup' ? 'top-[160px]' : 'top-[300px]'
        }`}
        style={{ maxHeight: 200 }}
      >
        <ScrollView keyboardShouldPersistTaps="handled">
          {searchResults.map((location, index) => (
            <TouchableOpacity
              key={`${location.name}-${index}`}
              className={`p-3 border-b ${isDarkMode ? 'border-slate-700' : 'border-slate-100'}`}
              onPress={() => handleLocationSelect(location)}
            >
              <Text>{location.name}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
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
              {isDriver ? 'Driver Request Booking Amendment' : 'Request Booking Amendment'}
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
                    <View className="mb-4 relative">
                      <Text className="mb-2 font-JakartaMedium">New Pickup Location (Optional)</Text>
                      <TextInput
                        className={`p-3 mb-2 rounded-lg ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                        value={newStartName}
                        onChangeText={(text) => {
                          setNewStartName(text);
                          handleLocationSearch(text, 'pickup');
                        }}
                        placeholder="Search for location"
                        placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                      />
                      {newStartName && (
                        <View className="flex-row">
                          <TextInput
                            className={`p-3 rounded-lg flex-1 mr-2 ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                            value={newStartLat}
                            onChangeText={setNewStartLat}
                            placeholder="Latitude"
                            placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                            keyboardType="numeric"
                            editable={false}
                          />
                          <TextInput
                            className={`p-3 rounded-lg flex-1 ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                            value={newStartLong}
                            onChangeText={setNewStartLong}
                            placeholder="Longitude"
                            placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                            keyboardType="numeric"
                            editable={false}
                          />
                        </View>
                      )}
                    </View>
                    
                    {/* End Location */}
                    <View className="mb-4 relative">
                      <Text className="mb-2 font-JakartaMedium">New Destination (Optional)</Text>
                      <TextInput
                        className={`p-3 mb-2 rounded-lg ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                        value={newEndName}
                        onChangeText={(text) => {
                          setNewEndName(text);
                          handleLocationSearch(text, 'dropoff');
                        }}
                        placeholder="Search for location"
                        placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                      />
                      {newEndName && (
                        <View className="flex-row">
                          <TextInput
                            className={`p-3 rounded-lg flex-1 mr-2 ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                            value={newEndLat}
                            onChangeText={setNewEndLat}
                            placeholder="Latitude"
                            placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                            keyboardType="numeric"
                            editable={false}
                          />
                          <TextInput
                            className={`p-3 rounded-lg flex-1 ${isDarkMode ? 'bg-slate-700 text-white border-slate-600' : 'bg-gray-50 text-black border-gray-300'} border`}
                            value={newEndLong}
                            onChangeText={setNewEndLong}
                            placeholder="Longitude"
                            placeholderTextColor={isDarkMode ? '#9CA3AF' : '#6B7280'}
                            keyboardType="numeric"
                            editable={false}
                          />
                        </View>
                      )}
                    </View>
                    
                    {/* Date/Time Picker */}
                    <View className="mb-4">
                      <Text className="mb-2 font-JakartaMedium">New Departure Time (Optional)</Text>
                      <TouchableOpacity 
                        className={`p-3 rounded-lg flex-row justify-between ${isDarkMode ? 'bg-slate-700 border-slate-600' : 'bg-gray-50 border-gray-300'} border`}
                        onPress={() => {
                          setShowDatePicker(true);
                          setIsTimeModified(true);
                        }}
                      >
                        <Text>{isTimeModified ? newStartTime.toLocaleString() : "Not changing (keep as scheduled)"}</Text>
                        <FontAwesome5 name="calendar-alt" size={18} color={isDarkMode ? '#FFF' : '#000'} />
                      </TouchableOpacity>
                      
                      {showDatePicker && (
                        Platform.OS === 'android' ? (
                          <DateTimePicker
                            key={`picker-${Date.now()}`}
                            value={newStartTime}
                            mode="datetime"
                            display="default"
                            onChange={(event, selectedDate) => {
                              setShowDatePicker(false);
                              if (selectedDate) {
                                setNewStartTime(selectedDate);
                                setIsTimeModified(true);
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
                                  setIsTimeModified(true);
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
            
            {/* Search Results */}
            {renderSearchResults()}
          </ScrollView>
        </View>
      </View>
    </Modal>
  );
};

export default BookingAmendmentModal;
