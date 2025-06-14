import React from 'react';
import { View, TouchableOpacity } from 'react-native';
import { Text } from '@/components/common/ThemedText';
import { useTheme } from '@/context/ThemeContext';
import { formatTimestamp } from '@/utils/formatTime';
import { AddBookingAmendmentRequest } from '@/services/bookingService';
import { FontAwesome5 } from '@expo/vector-icons';
import { toHumanReadable } from '@/utils/cronTools';

interface AmendmentRequestBubbleProps {
  amendment: AddBookingAmendmentRequest;
  amendmentId: string;
  isFromCurrentUser: boolean;
  timestamp: string;
  onApprove: (amendmentId: string) => void;
  requesterApproved?: boolean;
  isDriverView?: boolean; // Add prop to indicate if the current user is a driver
}

const AmendmentRequestBubble: React.FC<AmendmentRequestBubbleProps> = ({
  amendment,
  amendmentId,
  isFromCurrentUser,
  timestamp,
  onApprove,
  requesterApproved = false,
  isDriverView = false
}) => {
  const { isDarkMode } = useTheme();
  
  // Correctly identify who needs to approve this amendment
  const needsDriverApproval = !amendment.DriverApproval;
  const needsPassengerApproval = !amendment.PassengerApproval;
  
  // Check if the current user can approve based on their role
  const canApprove = isDriverView ? needsDriverApproval : needsPassengerApproval;

  // Determine the status of the amendment
  const isFullyApproved = amendment.DriverApproval && amendment.PassengerApproval;
  const isPartiallyApproved = (amendment.DriverApproval || amendment.PassengerApproval) && !isFullyApproved;
  
  // Determine who originally requested this amendment (based on who already approved it)
  const requestedByDriver = amendment.DriverApproval && !amendment.PassengerApproval;
  const requestedBy = requestedByDriver ? 'Driver' : 'Passenger';

  // Format the amendment details for display
  const formatAmendmentDetails = () => {
    const details = [];
    
    if (amendment.CancellationRequest) {
      details.push('Booking cancellation requested');
    } else if (amendment.ScheduleAmendment) {
      // Handle schedule amendments
      if (amendment.RecurrenceCron) {
        details.push(`New schedule: ${toHumanReadable(amendment.RecurrenceCron)}`);
      }
      
      if (amendment.RepeatUntil) {
        const date = new Date(amendment.RepeatUntil);
        details.push(`Repeat until: ${date.toLocaleDateString()}`);
      }
    } else {
      if (amendment.ProposedPrice) {
        details.push(`New price: £${amendment.ProposedPrice.toFixed(2)}`);
      }
      
      if (amendment.StartName) {
        details.push(`New pickup: ${amendment.StartName}`);
      }
      
      if (amendment.EndName) {
        details.push(`New destination: ${amendment.EndName}`);
      }
      
      if (amendment.StartTime) {
        const date = new Date(amendment.StartTime);
        details.push(`New time: ${date.toLocaleString()}`);
      }
    }
    
    return details.length > 0 ? details : ['No changes specified'];
  };
  
  return (
    <View className={`mb-4 ${isFromCurrentUser ? 'items-end' : 'items-start'}`}>
      <View
        className={`rounded-2xl p-4 max-w-[85%] ${
          isDarkMode ? 'bg-indigo-800' : 'bg-indigo-100'
        }`}
      >
        <View className="mb-2 flex-row justify-between items-center">
          <Text className={`font-JakartaBold ${isDarkMode ? 'text-white' : 'text-indigo-800'}`}>
            {amendment.CancellationRequest 
              ? 'Booking Cancellation Request' 
              : amendment.ScheduleAmendment
                ? 'Schedule Amendment Request'
                : 'Booking Amendment Request'}
          </Text>
          <View className={`px-2 py-1 rounded-full ${
            requestedByDriver ? 'bg-blue-600' : 'bg-green-600'
          }`}>
            <Text className="text-white text-xs">{requestedBy}</Text>
          </View>
        </View>
        
        <Text className={`text-xs ${isDarkMode ? 'text-indigo-200' : 'text-indigo-500'}`}>
            Booking ID: {amendment.BookingId}
        </Text>
        
        <View className="border-t border-b my-2 py-2 border-opacity-20 border-indigo-300">
          {formatAmendmentDetails().map((detail, index) => (
            <Text 
              key={index} 
              className={`${isDarkMode ? 'text-white' : 'text-indigo-800'} py-1`}
            >
              • {detail}
            </Text>
          ))}
        </View>
        
        <View className="flex-row justify-between items-center mt-2">
          <Text
            className={`text-xs ${
              isDarkMode ? 'text-indigo-200' : 'text-indigo-500'
            }`}
          >
            {formatTimestamp(new Date(timestamp).getTime())}
          </Text>
          
          {/* Show approval buttons if current user can approve */}
          {canApprove && (
            <View className="flex-row">
              <TouchableOpacity
                className="bg-green-600 px-3 py-1 rounded-full mr-2"
                onPress={() => onApprove(amendmentId)}
              >
                <Text className="text-white text-xs">Approve</Text>
              </TouchableOpacity>
              <TouchableOpacity
                className="bg-red-600 px-3 py-1 rounded-full"
              >
                <Text className="text-white text-xs">Decline</Text>
              </TouchableOpacity>
            </View>
          )}
          
          {/* Show approval status when not showing approval buttons */}
          {(!canApprove || isFullyApproved) && (
            <View className="flex-row items-center">
              {isFullyApproved ? (
                <>
                  <FontAwesome5 name="check-circle" size={14} color="green" />
                  <Text className="text-green-600 text-xs ml-1">Fully Approved</Text>
                </>
              ) : isPartiallyApproved ? (
                <>
                  <FontAwesome5 name="check" size={14} color="orange" />
                  <Text className="text-orange-500 text-xs ml-1">Partially Approved</Text>
                </>
              ) : (
                <>
                  <FontAwesome5 name="clock" size={14} color="orange" />
                  <Text className="text-orange-500 text-xs ml-1">Awaiting Approval</Text>
                </>
              )}
            </View>
          )}
        </View>
      </View>
    </View>
  );
};

export default AmendmentRequestBubble;
