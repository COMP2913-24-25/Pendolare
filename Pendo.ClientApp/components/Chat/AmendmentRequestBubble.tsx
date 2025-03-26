import React from 'react';
import { View, TouchableOpacity } from 'react-native';
import { Text } from '@/components/common/ThemedText';
import { useTheme } from '@/context/ThemeContext';
import { formatTimestamp } from '@/utils/formatTime';
import { AddBookingAmmendmentRequest } from '@/services/bookingService';
import { FontAwesome5 } from '@expo/vector-icons';

interface AmendmentRequestBubbleProps {
  amendment: AddBookingAmmendmentRequest;
  amendmentId: string;
  isFromCurrentUser: boolean;
  timestamp: string;
  onApprove: (amendmentId: string) => void;
  requesterApproved?: boolean; // Add this to track if the requester already approved
}

const AmendmentRequestBubble: React.FC<AmendmentRequestBubbleProps> = ({
  amendment,
  amendmentId,
  isFromCurrentUser,
  timestamp,
  onApprove,
  requesterApproved = false
}) => {
  const { isDarkMode } = useTheme();
  
  // Format the amendment details for display
  const formatAmendmentDetails = () => {
    const details = [];
    
    if (amendment.CancellationRequest) {
      details.push('Booking cancellation requested');
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
        <View className="mb-2">
          <Text className={`font-JakartaBold ${isDarkMode ? 'text-white' : 'text-indigo-800'}`}>
            {amendment.CancellationRequest ? 'Booking Cancellation Request' : 'Booking Amendment Request'}
          </Text>
          <Text className={`text-xs ${isDarkMode ? 'text-indigo-200' : 'text-indigo-500'}`}>
            Booking ID: {amendment.BookingId}
          </Text>
        </View>
        
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
          
          {/* Show approval buttons or approval status */}
          {!isFromCurrentUser && !amendment.DriverApproval && (
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
          
          {/* Show different status based on approval state */}
          {(amendment.DriverApproval || isFromCurrentUser) && (
            <View className="flex-row items-center">
              <FontAwesome5 name="check-circle" size={14} color="green" />
              <Text className="text-green-600 text-xs ml-1">
                {isFromCurrentUser 
                  ? (amendment.DriverApproval ? "Fully Approved" : "Awaiting Approval")
                  : "Approved"}
              </Text>
            </View>
          )}
        </View>
      </View>
    </View>
  );
};

export default AmendmentRequestBubble;
