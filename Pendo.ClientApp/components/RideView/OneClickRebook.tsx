import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Alert, ActivityIndicator } from 'react-native';
import { FontAwesome5 } from '@expo/vector-icons';
import { useTheme } from '@/context/ThemeContext';
import { rebookCommuterJourney } from '@/services/bookingService';

interface OneClickRebookProps {
  journeyId: string;
  originalDuration?: number;
  startDate?: Date;
  onSuccess?: () => void;
  compact?: boolean;
}

/**
 * OneClickRebook component provides a single button to quickly rebook 
 * an expired commuter journey preserving the original booking's duration
 */
const OneClickRebook = ({ 
  journeyId, 
  originalDuration,
  startDate, 
  onSuccess, 
  compact = false 
}: OneClickRebookProps) => {
  const { isDarkMode } = useTheme();
  const [isRebooking, setIsRebooking] = useState(false);
  
  const handleRebook = async () => {
    try {
      setIsRebooking(true);
      
      const result = await rebookCommuterJourney(
        journeyId, 
        {
          startDate: startDate || new Date(),
          customDuration: originalDuration
        }
      );
      
      if (result.success) {
        Alert.alert(
          "Success",
          "Journey rebooked successfully! Your commuter journey has been extended.",
          [{ text: "OK" }]
        );
        if (onSuccess) onSuccess();
      } else {
        Alert.alert(
          "Booking Failed",
          result.message || "Failed to rebook journey. Please try again.",
          [{ text: "OK" }]
        );
      }
    } catch (error) {
      console.error("Error rebooking journey:", error);
      Alert.alert(
        "Error",
        "An unexpected error occurred. Please try again later.",
        [{ text: "OK" }]
      );
    } finally {
      setIsRebooking(false);
    }
  };
  
  if (compact) {
    return (
      <TouchableOpacity
        className={`py-2 px-4 rounded-full ${isDarkMode ? 'bg-blue-700' : 'bg-blue-600'}`}
        onPress={handleRebook}
        disabled={isRebooking}
      >
        {isRebooking ? (
          <ActivityIndicator size="small" color="#FFFFFF" />
        ) : (
          <Text className="text-white text-center font-JakartaBold">Rebook</Text>
        )}
      </TouchableOpacity>
    );
  }
  
  return (
    <View className="mt-3">
      <TouchableOpacity
        className={`flex-row items-center justify-center py-3 px-4 rounded-lg ${
          isRebooking 
            ? (isDarkMode ? 'bg-blue-800' : 'bg-blue-400') 
            : (isDarkMode ? 'bg-blue-700' : 'bg-blue-600')
        }`}
        onPress={handleRebook}
        disabled={isRebooking}
      >
        {isRebooking ? (
          <ActivityIndicator size="small" color="#FFFFFF" />
        ) : (
          <>
            <FontAwesome5 name="redo" size={16} color="#FFFFFF" />
            <Text className="text-white font-JakartaBold ml-2">
              One-Click Rebook
            </Text>
          </>
        )}
      </TouchableOpacity>
    </View>
  );
};

export default OneClickRebook;
