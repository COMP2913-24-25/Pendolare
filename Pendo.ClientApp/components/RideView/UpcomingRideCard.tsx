import { View, TouchableOpacity, ActivityIndicator } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import { BookingDetails } from "@/services/bookingService";
import StatusBadge from "./StatusBadge";
import CronVisualizer from "./CronVisualiser";
import { getNextCronDates } from "@/utils/cronTools";
import OneClickRebook from "./OneClickRebook";
import CheckoutModal, { SubRide } from "./Modals/CheckoutModal";
import { useState } from "react";
import { ViewBalance } from "@/services/paymentService";
import { createBooking } from "@/services/bookingService";
import { create } from "react-test-renderer";

interface UpcomingRideCardProps {
  booking?: BookingDetails;
  onPress: () => void;
}

/*
    UpcomingRideCard
    Card for upcoming ride in ride view
*/
const UpcomingRideCard = ({ booking, onPress }: UpcomingRideCardProps) => {
  const { isDarkMode } = useTheme();
  const [visible, setVisible] = useState(false);
  const [userBalance, setUserBalance] = useState(0);
  const [subrides, setSubrides] = useState<SubRide[]>([]);
  const [endDate, setEnddate] = useState<Date>(new Date(Date.now() + (1000 * 60 * 60 * 24 * 14)));
  const [startDate, setStart] = useState<Date>(new Date());

  const handleRebookCommuter = async () => {
    createBooking(booking?.Journey.JourneyId as any,
      startDate,
      endDate
    ).then((res) => {
        console.log("Rebooked successfully:", res);
        setVisible(false);
      });
  }

  async function getSubrides() {
    // Fetch subrides here
    let start = booking?.Booking.BookedWindowEnd ? new Date(booking.Booking.BookedWindowEnd) : new Date();

    if (start < new Date()) {
      start = new Date(Date.now() + (1000 * 60 * 15));
    }

    setStart(start);

    const twoWeeksFromNow = new Date(Date.now() + (1000 * 60 * 60 * 24 * 14));
    let end = new Date(booking?.Journey?.RepeatUntil ?? twoWeeksFromNow.getTime()) > twoWeeksFromNow 
    ? twoWeeksFromNow : new Date(booking?.Journey.RepeatUntil ?? twoWeeksFromNow.getTime());

    if (end === undefined) {
      // don't ask
      end = twoWeeksFromNow;
    }

    setEnddate(end);

    const times = getNextCronDates(booking?.Journey.Recurrance as string, start, end, 40);

    times.forEach((time) => {
      console.log("Time:", time);
    });

    setSubrides(times.map((time) => {
      return {
        journeyId: booking?.Journey.JourneyId as string,
        journeyDate: time as Date,
        price: booking?.Journey.Price as number,
        parent: booking?.Journey,
      };
    }));
  }
  
  // Log the booking data to see its structure
  console.log("UpcomingRideCard received booking:", booking);
  
  // Check if booking is valid and has the required properties
  const isValidBooking = !!booking && 
                       typeof booking === 'object' &&
                       (!!booking.Journey || !!booking.Booking);
  
  if (!isValidBooking) {
    console.log("Invalid booking data for card:", booking);
    return (
      <TouchableOpacity
        className={`p-4 rounded-lg shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"} items-center`}
        onPress={onPress}
        disabled={true}
      >
        <ActivityIndicator size="small" color="#2563EB" className="mb-2" />
        <Text className="text-gray-500">Loading ride details...</Text>
      </TouchableOpacity>
    );
  }
  
  // Safely extract data with fallbacks for everything
  const journey = booking.Journey || {};
  const rideDetails = booking.Booking || {};
  const status = booking.BookingStatus || { Status: "Unknown" };
  
  // Handle missing properties with fallbacks
  const endName = journey.EndName || 'Destination';
  const price = journey.Price || 0;
  
  // Safely get driver name
  let driverName = 'Driver';
  if (journey.User) {
    const user = journey.User;
    if (typeof user === 'object') {
      if (user.Name) driverName = user.Name;
      else if (user.FullName) driverName = user.FullName;
      else if (user.FirstName) driverName = user.FirstName;
    }
  }

  if (booking.Journey.Recurrance) {
    // get next date from cron
    
    const startDate = rideDetails.RideTime < new Date() ? new Date() : rideDetails.RideTime;

    const endDate = new Date(Date.now() + (1000 * 60 * 60 * 24 * 30));

    const cron = booking.Journey.Recurrance;
    const nextDate = getNextCronDates(cron, startDate, endDate, 1)[0];
    if (nextDate) {
      rideDetails.RideTime = nextDate;
    }
  }
  
  // Safe date conversion
  let rideTime = new Date();
  try {
    if (rideDetails.RideTime) {
      if (typeof rideDetails.RideTime === 'string') {
        rideTime = new Date(rideDetails.RideTime);
      } else if (rideDetails.RideTime instanceof Date) {
        rideTime = rideDetails.RideTime;
      }
    }
  } catch (e) {
    console.error("Error parsing ride time:", e);
  }

  return (
    <TouchableOpacity
      className={`p-4 rounded-lg shadow-sm ${isDarkMode ? "bg-slate-800" : "bg-white"}`}
      onPress={onPress}
    >
      <View className="flex-row justify-between items-center mb-2">
        <Text
          className="text-lg font-JakartaBold flex-1"
          numberOfLines={3}
          adjustsFontSizeToFit
          minimumFontScale={1}
        >
          {endName}
        </Text>
        <Text className="text-blue-600 font-JakartaBold ml-2">
          £{price.toFixed(2)}
        </Text>
      </View>
      <View className="flex-row justify-between items-center mb-2">
        <Text className="text-gray-500">{rideTime.toUTCString()}</Text>
        <Text className="text-gray-800 font-JakartaSemiBold">With {driverName}</Text>
      </View>
      <StatusBadge statusText={status.Status} />
      {(booking.Journey.Recurrance &&     
      <View className="mt-2">
        <CronVisualizer
          cron={booking.Journey.Recurrance}
          endDate={booking.Journey.RepeatUntil ?? rideTime}
          isDarkMode={isDarkMode}
          />
          <View>
            <OneClickRebook onPress={() => {
              getSubrides();
              ViewBalance().then((balance) => {
                setUserBalance(balance.NonPending);
              });
              setVisible(true);
            }}/>
            <CheckoutModal
              visible={visible}
              onClose={() => setVisible(false)}
              onConfirm={handleRebookCommuter}
              isDarkMode={isDarkMode}
              userBalance={userBalance}
              subrides={subrides}
              />
          </View>
      </View>)}
    </TouchableOpacity>
  );
};

export default UpcomingRideCard;
