import { FontAwesome5 } from "@expo/vector-icons";
import { useCallback, useState } from "react";
import { View, TouchableOpacity, Modal, ScrollView, ActivityIndicator, Alert } from "react-native";
import Map from "../Map/Map";
import { Text } from "@/components/common/ThemedText"; // updated
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { createBooking } from "@/services/bookingService";
import { toHumanReadable, getNextCronDates } from "@/utils/cronTools";
import { Rating } from "react-native-ratings";
import CheckoutModal, { Discount, SubRide } from "./Modals/CheckoutModal";
import { BalanceSheet, ViewBalance } from "@/services/paymentService";
import { useFocusEffect } from "expo-router";

interface RideDetailsProps {
  ride: any;
  visible: boolean;
  onClose: () => void;
}

/*
  RideDetails
  Modal component for displaying ride details and booking
*/
const RideDetails = ({ ride, visible, onClose }: RideDetailsProps) => {
  const { isDarkMode } = useTheme();
  const [inBooking, setInBooking] = useState(false);
  const [bookingStatus, setBookingStatus] = useState<{
    success: boolean;
    message: string;
    showMessage: boolean;
  }>({
    success: false,
    message: "",
    showMessage: false,
  });
  const [showCheckout, setShowCheckout] = useState(false);
  const [subrides, setSubrides] = useState<SubRide[]>([]);
  const [discount, setDiscount] = useState<Discount>();
  const [userBalance, setUserBalance] = useState(0.00);

  // Extract discount info if available
  const hasDiscount = ride.Discount || 
                     (ride.Journey && ride.Journey.Discount);
  const discountInfo = hasDiscount ? 
                      (ride.Discount || ride.Journey.Discount) : 
                      null;
  
  // Format price with discount if applicable
  const formatPrice = () => {
    let formattedPrice = "";
    
    // Handle different price properties depending on data structure
    const price = ride.price || ride.AdvertisedPrice;
    
    if (!hasDiscount) {
      return typeof price === 'number' ? `£${price.toFixed(2)}` : price;
    }
    
    // If there's a discount, calculate and display original and discounted price
    const originalPrice = discountInfo?.OriginalPrice || price/(1-discountInfo?.DiscountPercentage);
    const discountPercentage = discountInfo?.DiscountPercentage * 100;
    
    return (
      <View>
        <View className="flex-row items-center">
          <Text className="font-JakartaBold text-2xl text-blue-600">
            {typeof price === 'number' ? `£${price.toFixed(2)}` : price}
          </Text>
          <Text className="ml-2 line-through text-gray-500">
            £{originalPrice.toFixed(2)}
          </Text>
        </View>
        <Text className="text-xs text-green-600">
          {discountPercentage}% discount applied
        </Text>
      </View>
    );
  };

  const handleBooking = async () => {
    setInBooking(true);

    try {
      // Extract departureTime from string or timestamp
      const departureTime = new Date(ride.departureTime);

      if (ride.recurrence) {
        const oneWeek = 604800000; // 1 week in milliseconds
        const journeyDates = getNextCronDates(
            ride.recurrence, 
            departureTime, 
            new Date(departureTime.getTime() + oneWeek), 
            24);

        // Apply discount from journey if available
        let rideDiscount: Discount | undefined;
        if (hasDiscount) {
          rideDiscount = {
            name: `${discountInfo.WeeklyJourneys} Journeys/Week Discount`,
            amount: discountInfo.DiscountPercentage
          };
        } else {
          rideDiscount = {
            name: "Frequent Rider Discount",
            amount: 0.1
          };
        }

        const newSubrides : SubRide[] = journeyDates.map((date) => ({
          journeyId: ride.JourneyId,
          journeyDate: date,
          price: ride.AdvertisedPrice || ride.price?.replace('£', ''),
          parent: ride,
        }));

        setSubrides(newSubrides);
        setDiscount(rideDiscount);

        setShowCheckout(true);
        return;
      }

      const result = await createBooking(ride.JourneyId, departureTime);

      if (result.success) {
        setBookingStatus({
          success: true,
          message: "Your ride has been successfully booked!",
          showMessage: true,
        });

        // Close the details modal after a short delay
        setTimeout(() => {
          onClose();
          setTimeout(
            () => setBookingStatus((prev) => ({ ...prev, showMessage: false })),
            500,
          );
        }, 2000);
      } else {
        setBookingStatus({
          success: false,
          message:
            result.message || "Failed to book your ride. Please try again.",
          showMessage: true,
        });
      }
    } catch (error) {
      setBookingStatus({
        success: false,
        message: "An error occurred while booking. Please try again later.",
        showMessage: true,
      });
    } finally {
      setInBooking(false);
    }
  };

  const handleCommuterBooking = async () => {
    const twoWeeks = 1209600000; // 2 weeks in milliseconds
    const result = await createBooking(ride.JourneyId, new Date(ride.departureTime), new Date(twoWeeks));

    console.log("Commuter booking result:", result);
    
    if (result.Status !== "Error") {
      Alert.alert("Success", "Your ride has been successfully booked!");
      return;
    }

    Alert.alert("Error", "Failed to book your ride. Please try again.");
    return;
  };

  const dismissMessage = () => {
    setBookingStatus((prev) => ({ ...prev, showMessage: false }));
  };

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onShow={() => {
        ViewBalance().then((balance : BalanceSheet) => {
          setUserBalance(balance.NonPending);
        });
      }}
      onRequestClose={onClose}
    >
      <View className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-white"}`}>
        <View className="h-1/3">
          <Map pickup={ride.pickup} dropoff={ride.dropoff} />
          <TouchableOpacity
            className={`absolute top-12 left-4 p-2 rounded-full shadow-sm ${
              isDarkMode ? "bg-slate-800" : "bg-white"
            }`}
            onPress={onClose}
          >
            <FontAwesome5
              name={icons.close}
              size={24}
              color={isDarkMode ? "#FFF" : "#000"}
            />
          </TouchableOpacity>
        </View>

        <ScrollView className="p-5">
          <View>
            <View className="flex-row items-center justify-between mb-4">
              <View className="flex-row items-center">
                <View
                  className={`w-12 h-12 rounded-full mr-3 items-center justify-center ${
                    isDarkMode ? "bg-slate-700" : "bg-gray-200"
                  }`}
                >
                  <FontAwesome5
                    name={icons.person}
                    size={24}
                    color={isDarkMode ? "#FFF" : "#666666"}
                  />
                </View>
                <View>
                  <Text className="font-JakartaBold text-lg">{ride.driverName}</Text>
                  <View className="flex-row items-center">
                    {ride.rating === -1 ? (
                      <Text className="text-xs font-Jakarta">No driver rating yet!</Text>
                    ) : (
                      <Rating startingValue={ride.rating} readonly imageSize={16} />
                    )}
                  </View>
                </View>
              </View>
              {formatPrice()}
            </View>

            <View
              className={`p-4 rounded-xl mb-4 ${
                isDarkMode ? "bg-slate-800" : "bg-gray-50"
              }`}
            >
              <View className="mb-3">
                <Text className="text-gray-500">From</Text>
                <Text className="font-JakartaMedium">{ride.pickup.name}</Text>
              </View>
              <View className="mb-3">
                <Text className="text-gray-500">To</Text>
                <Text className="font-JakartaMedium">{ride.dropoff.name}</Text>
              </View>
              <View className="mb-3">
                <Text className="text-gray-500">Departure</Text>
                <Text className="font-JakartaMedium">{ride.departureTime}</Text>
              </View>
              <View>
                <Text className="text-gray-500">Price</Text>
                <View>
                  <Text className="font-JakartaMedium">
                    {typeof ride.price === 'number' ? `£${ride.price.toFixed(2)}` : ride.price}
                  </Text>
                  {hasDiscount && (
                    <Text className="text-xs text-green-600">
                      {discountInfo?.DiscountPercentage * 100}% discount for {discountInfo?.WeeklyJourneys} journeys per week
                    </Text>
                  )}
                </View>
              </View>
            </View>

            <View
              className={`p-4 rounded-xl mb-6 ${
                isDarkMode ? "bg-slate-800" : "bg-gray-50"
              }`}
            >
              <View className="flex-row items-center">
                <FontAwesome5
                  name={icons.person}
                  size={20}
                  color={isDarkMode ? "#FFF" : "#666666"}
                  style={{ marginRight: 8 }}
                />
                <Text className="text-gray-600">
                  {ride.MaxPassengers} seats available
                </Text>
              </View>

              {ride.recurrence && (
                <View className="flex-row items-center mt-2">
                  <FontAwesome5
                    name={icons.time}
                    size={20}
                    color={isDarkMode ? "#FFF" : "#666666"}
                    style={{ marginRight: 8 }}
                  />
                  <Text className="text-gray-600">
                    {toHumanReadable(ride.recurrence)}
                  </Text>
                </View>
              )}
            </View>

            <View className="flex-row justify-between space-x-4">
              <TouchableOpacity
                className={`flex-1 ${
                  inBooking ? "bg-blue-400" : "bg-blue-600"
                } py-4 rounded-xl items-center justify-center`}
                onPress={handleBooking}
                disabled={inBooking}
              >
                {inBooking ? (
                  <ActivityIndicator color="#FFFFFF" />
                ) : (
                  <Text className="text-white text-center font-JakartaBold text-lg">
                    Book Journey
                  </Text>
                )}
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </View>

      {/* Booking Status Modal */}
      <Modal
        transparent={true}
        visible={bookingStatus.showMessage}
        animationType="fade"
        onRequestClose={dismissMessage}
      >
        <TouchableOpacity
          className="flex-1 bg-black/50 justify-center items-center"
          activeOpacity={1}
          onPress={dismissMessage}
        >
          <View
            className={`w-5/6 p-5 rounded-xl ${
              bookingStatus.success
                ? isDarkMode
                  ? "bg-green-900"
                  : "bg-green-50"
                : isDarkMode
                  ? "bg-red-900"
                  : "bg-red-50"
            }`}
          >
            <View className="flex-row items-center mb-2">
              <FontAwesome5
                name={bookingStatus.success ? icons.check : icons.alert}
                size={24}
                color={
                  bookingStatus.success
                    ? isDarkMode
                      ? "#4ADE80"
                      : "#16A34A"
                    : isDarkMode
                      ? "#F87171"
                      : "#DC2626"
                }
                style={{ marginRight: 10 }}
              />
              <Text
                className={`font-JakartaBold text-lg ${
                  bookingStatus.success
                    ? isDarkMode
                      ? "text-green-300"
                      : "text-green-800"
                    : isDarkMode
                      ? "text-red-300"
                      : "text-red-800"
                }`}
              >
                {bookingStatus.success ? "Success" : "Error"}
              </Text>
            </View>
            <Text
              className={`${
                bookingStatus.success
                  ? isDarkMode
                    ? "text-green-200"
                    : "text-green-700"
                  : isDarkMode
                    ? "text-red-200"
                    : "text-red-700"
              }`}
            >
              {bookingStatus.message}
            </Text>
          </View>
        </TouchableOpacity>
      </Modal>

      <CheckoutModal 
        visible={showCheckout} 
        onClose={() => setShowCheckout(false)} 
        subrides={subrides} 
        discount={discount}
        userBalance={userBalance}
        isDarkMode={isDarkMode} 
        onConfirm={() => handleCommuterBooking()} />
    </Modal>
  );
};

export default RideDetails;
