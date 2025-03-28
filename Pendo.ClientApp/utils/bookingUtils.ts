import { BookingDetails, User } from "@/services/bookingService";

/**
 * Interface for a simplified representation of a ride
 */
export interface Ride {
  BookingId: string;
  JourneyId: string;
  RideTime: Date;
  Status: string;
  DriverName?: string;
  PassengerName?: string;
  PassengerId?: string;
  DriverId?: string;
  Price: number;
  Pickup?: {
    latitude: number;
    longitude: number;
    name: string;
  };
  Dropoff?: {
    latitude: number;
    longitude: number;
    name: string;
  };
}

/**
 * Converts a Ride object to a BookingDetails object
 * This is useful for adapting existing Ride data to the BookingDetails interface
 */
export function convertRideToBookingDetails(ride: Ride): BookingDetails {
  return {
    Booking: {
      BookingId: ride.BookingId,
      RideTime: ride.RideTime,
      FeeMargin: 0.2, // Default
      User: {
        UserId: ride.PassengerId || '',
        Name: ride.PassengerName || 'Passenger'
      }
    },
    BookingStatus: {
      Status: ride.Status,
      StatusId: getStatusId(ride.Status), // Convert status string to ID
      Description: getStatusDescription(ride.Status)
    },
    Journey: {
      JourneyId: ride.JourneyId,
      StartTime: ride.RideTime,
      StartName: ride.Pickup?.name || '',
      StartLat: ride.Pickup?.latitude || 0,
      StartLong: ride.Pickup?.longitude || 0,
      EndName: ride.Dropoff?.name || '',
      EndLat: ride.Dropoff?.latitude || 0,
      EndLong: ride.Dropoff?.longitude || 0,
      Price: ride.Price,
      JourneyStatusId: 1, // Default
      JourneyType: 1, // Default
      User: {
        UserId: ride.DriverId || '',
        Name: ride.DriverName || 'Driver'
      }
    }
  };
}

/**
 * Converts a BookingDetails object to a Ride object
 * This is the reverse of convertRideToBookingDetails
 */
export function convertBookingDetailsToRide(booking: BookingDetails): Ride {
  // Extract needed data with fallbacks
  const journey = booking.Journey || {};
  const bookingDetails = booking.Booking || {};
  const status = booking.BookingStatus?.Status || "Unknown";
  
  // Get driver and passenger info
  let driverName = "Driver";
  let driverId = "";
  let passengerName = "Passenger";
  let passengerId = "";
  
  if (journey.User) {
    if (typeof journey.User === "object") {
      driverId = journey.User.UserId || "";
      driverName = journey.User.Name || journey.User.FullName || journey.User.FirstName || "Driver";
    }
  }
  
  if (bookingDetails.User) {
    if (typeof bookingDetails.User === "object") {
      passengerId = bookingDetails.User.UserId || "";
      passengerName = bookingDetails.User.Name || bookingDetails.User.FullName || bookingDetails.User.FirstName || "Passenger";
    }
  }
  
  return {
    BookingId: bookingDetails.BookingId || "",
    JourneyId: journey.JourneyId || "",
    RideTime: bookingDetails.RideTime instanceof Date ? 
      bookingDetails.RideTime : 
      typeof bookingDetails.RideTime === "string" ? 
        new Date(bookingDetails.RideTime) : 
        new Date(),
    Status: status,
    DriverName: driverName,
    PassengerName: passengerName,
    PassengerId: passengerId,
    DriverId: driverId,
    Price: journey.Price || 0,
    Pickup: journey.StartName ? {
      latitude: journey.StartLat || 0,
      longitude: journey.StartLong || 0,
      name: journey.StartName
    } : undefined,
    Dropoff: journey.EndName ? {
      latitude: journey.EndLat || 0,
      longitude: journey.EndLong || 0,
      name: journey.EndName
    } : undefined
  };
}

/**
 * Helper function to convert status string to status ID
 */
function getStatusId(status: string): number {
  switch (status) {
    case "Pending": return 1;
    case "Confirmed": return 2;
    case "Cancelled": return 3;
    case "PendingCompletion": return 4;
    case "Completed": return 5;
    case "Advertised": return 6;
    default: return 1;
  }
}

/**
 * Helper function to get status description
 */
function getStatusDescription(status: string): string {
  switch (status) {
    case "Pending": return "The booking has been created but not finalised.";
    case "Confirmed": return "The booking is confirmed.";
    case "Cancelled": return "The booking has been cancelled.";
    case "PendingCompletion": return "The ride has been completed and is awaiting confirmation.";
    case "Completed": return "The ride has been completed.";
    case "Advertised": return "The journey is advertised and available for booking.";
    default: return "";
  }
}
