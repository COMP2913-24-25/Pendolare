import React, { useState, useEffect } from 'react';
import { Modal, View, Text, TouchableOpacity, ScrollView, ActivityIndicator } from 'react-native';
import { FontAwesome5 } from '@expo/vector-icons';
import { icons } from '@/constants';

export interface SubRide {
  journeyId: string;
  journeyDate: Date;
  price: number;
  parent: any;
}

export interface Discount {
  name: string;
  amount: number;
}

interface CheckoutModalProps {
  visible: boolean;
  onClose: () => void;
  subrides: SubRide[];
  discount?: Discount;
  userBalance: number;
  isDarkMode: boolean;
  onConfirm: () => void;
}

const CheckoutModal = ({ 
  visible, 
  onClose, 
  subrides, 
  discount, 
  userBalance,
  isDarkMode,
  onConfirm 
}: CheckoutModalProps) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [subtotal, setSubtotal] = useState(0);
  const [total, setTotal] = useState(0);
  const [discountAmount, setDiscountAmount] = useState(0);

  // Calculate totals when rides or discount changes
  useEffect(() => {
    // Calculate subtotal from all rides
    const calcSubtotal = subrides.reduce((acc, ride) => acc + parseFloat(ride.price.toString()), 0);
    setSubtotal(calcSubtotal);
    
    // Apply discount if provided
    if (discount) {
      const discountValue = calcSubtotal * discount.amount;
      setDiscountAmount(discountValue);
      setTotal(calcSubtotal - discountValue);
    } else {
      setDiscountAmount(0);
      setTotal(calcSubtotal);
    }
  }, [subrides, discount]);

  const handleConfirm = async () => {
    setIsProcessing(true);
    try {
      await onConfirm();
      setTimeout(() => {
        setIsProcessing(false);
        onClose();
      }, 1000);
    } catch (error) {
      console.error("Error in checkout:", error);
      setIsProcessing(false);
    }
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString(undefined, { 
      weekday: 'short', 
      day: 'numeric', 
      month: 'short', 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const formatCurrency = (amount: number) => {
    return `£${amount.toFixed(2)}`;
  };

  // Check if user has enough balance for this booking
  const hasEnoughBalance = userBalance >= total;

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={onClose}
    >
      <View className="flex-1 justify-end">
        <View 
          className={`${isDarkMode ? 'bg-slate-900' : 'bg-white'} 
                     rounded-t-3xl shadow-xl max-h-[80%] min-h-[50%]`}
        >
          {/* Header */}
          <View className="p-5 border-b border-gray-200 flex-row justify-between items-center">
            <Text className={`text-xl font-JakartaBold ${isDarkMode ? 'text-white' : 'text-black'}`}>
              Checkout
            </Text>
            <TouchableOpacity onPress={onClose}>
              <FontAwesome5 
                name={icons.close} 
                size={20} 
                color={isDarkMode ? '#FFF' : '#000'} 
              />
            </TouchableOpacity>
          </View>

          {/* Content */}
          <ScrollView className="p-5">
            {/* Journey summary */}
            <View className="mb-6">
              <Text className={`text-lg font-JakartaBold mb-2 ${isDarkMode ? 'text-white' : 'text-black'}`}>
                Commuter Journey Summary
              </Text>
              <Text className={`mb-4 ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                You're booking a recurring journey with {subrides.length} trips in the next period.
              </Text>
              
              {/* Rides list */}
              <View className={`p-4 rounded-xl mb-4 ${isDarkMode ? 'bg-slate-800' : 'bg-gray-100'}`}>
                {subrides.slice(0, 3).map((ride, index) => (
                  <View key={index} className="flex-row justify-between mb-2">
                    <Text className={isDarkMode ? 'text-gray-300' : 'text-gray-700'}>
                      {formatDate(ride.journeyDate)}
                    </Text>
                    <Text className={isDarkMode ? 'text-white' : 'text-black'}>
                      {formatCurrency(parseFloat(ride.price.toString()))}
                    </Text>
                  </View>
                ))}
                
                {subrides.length > 3 && (
                  <View className="border-t border-gray-300 pt-2 mt-2">
                    <Text className={`text-center ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                      + {subrides.length - 3} more journeys
                    </Text>
                  </View>
                )}
              </View>
            </View>

            {/* Price breakdown */}
            <View className="mb-6">
              <Text className={`text-lg font-JakartaBold mb-2 ${isDarkMode ? 'text-white' : 'text-black'}`}>
                Price Breakdown
              </Text>
              
              <View className={`p-4 rounded-xl ${isDarkMode ? 'bg-slate-800' : 'bg-gray-100'}`}>
                <View className="flex-row justify-between mb-2">
                  <Text className={isDarkMode ? 'text-gray-300' : 'text-gray-700'}>
                    Subtotal ({subrides.length} journeys)
                  </Text>
                  <Text className={isDarkMode ? 'text-white' : 'text-black'}>
                    {formatCurrency(subtotal)}
                  </Text>
                </View>
                
                {discount && (
                  <View className="flex-row justify-between mb-2">
                    <Text className="text-green-600">
                      {discount.name} ({discount.amount * 100}% off)
                    </Text>
                    <Text className="text-green-600">
                      -{formatCurrency(discountAmount)}
                    </Text>
                  </View>
                )}
                
                <View className="border-t border-gray-300 pt-2 mt-2 flex-row justify-between">
                  <Text className={`font-JakartaBold ${isDarkMode ? 'text-white' : 'text-black'}`}>
                    Total
                  </Text>
                  <Text className={`font-JakartaBold ${isDarkMode ? 'text-white' : 'text-black'}`}>
                    {formatCurrency(total)}
                  </Text>
                </View>
              </View>
            </View>

            {/* Balance status */}
            <View className={`p-4 rounded-xl mb-6 ${
              hasEnoughBalance 
                ? isDarkMode ? 'bg-green-900' : 'bg-green-100' 
                : isDarkMode ? 'bg-red-900' : 'bg-red-100'
            }`}>
              <View className="flex-row items-center">
                <FontAwesome5 
                  name={hasEnoughBalance ? 'check-circle' : 'exclamation-circle'} 
                  size={20}
                  color={
                    hasEnoughBalance 
                      ? isDarkMode ? '#4ADE80' : '#16A34A'
                      : isDarkMode ? '#F87171' : '#DC2626'
                  }
                  style={{ marginRight: 8 }}
                />
                <Text className={
                  hasEnoughBalance 
                    ? isDarkMode ? 'text-green-300' : 'text-green-800'
                    : isDarkMode ? 'text-red-300' : 'text-red-800'
                }>
                  {hasEnoughBalance 
                    ? `Your balance of ${formatCurrency(userBalance)} is sufficient for this booking.`
                    : `Your balance of ${formatCurrency(userBalance)} is insufficient. You need ${formatCurrency(total - userBalance)} more.`
                  }
                </Text>
              </View>
            </View>
          </ScrollView>

          {/* Footer with confirm button */}
          <View className="p-5 border-t border-gray-200">
            <TouchableOpacity
              className={`py-4 rounded-xl items-center justify-center ${
                hasEnoughBalance && !isProcessing
                  ? 'bg-blue-600'
                  : 'bg-gray-400'
              }`}
              onPress={handleConfirm}
              disabled={!hasEnoughBalance || isProcessing}
            >
              {isProcessing ? (
                <ActivityIndicator color="#FFFFFF" />
              ) : (
                <Text className="text-white text-center font-JakartaBold text-lg">
                  {hasEnoughBalance 
                    ? 'Confirm Booking' 
                    : 'Insufficient Balance'}
                </Text>
              )}
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

export default CheckoutModal;
