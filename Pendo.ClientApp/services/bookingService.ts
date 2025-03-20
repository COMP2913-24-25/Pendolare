import { apiRequest } from "./apiClient";

import { BOOKING_ENDPOINTS } from "@/constants";

export interface CreateBookingRequest {
  JourneyId: string;
  JourneyTime: string;
}

export interface BookingResponse {
  id?: string;
  success: boolean;
  message?: string;
}

export interface BookingDetails {
  Booking: {
    BookingId : string;
    UserId: string;
    FeeMargin: number;
    RideTime: Date;
  };
  BookingStatus: {
    StatusId: number;
    Status: string;
    Description: string;
  },
  Journey: {
    JourneyId: string;
    UserId: string;
    StartTime: Date;
    StartName: string;
    StartLong: number;
    StartLat: number;
    EndName: string;
    EndLong: number;
    EndLat: number;
    Price: number;
    JourneyStatusId: number;
    JourneyType: number;
  }
}

export interface GetBookingsResponse
{
  bookings: BookingDetails[];
  success: boolean;
  message?: string;
}

/*
 * Create a booking for a journey
 * Note: The UserId is automatically added by the Kong gateway
 */
export async function createBooking(
  journeyId: string | number,
  journeyTime: Date | number,
): Promise<BookingResponse> {
  try {
    // Convert journey ID to string if it's a number (for dummy data)
    const stringJourneyId = journeyId.toString();

    console.log("reached");

    // Ensure we have a proper date string
    const dateString =
      typeof journeyTime === "number"
        ? new Date(journeyTime).toISOString()
        : journeyTime.toISOString();

    const response = await apiRequest<BookingResponse>(
      BOOKING_ENDPOINTS.CREATE_BOOKING,
      {
        method: "POST",
        body: JSON.stringify({
          JourneyId: stringJourneyId,
          JourneyTime: dateString,
        }),
      },
    );

    return {
      ...response,
      success: true,
    };
  } catch (error) {
    console.error("Create booking error:", error);
    return {
      success: false,
      message:
        error instanceof Error ? error.message : "Failed to create booking",
    };
  }
}

/*
 * Fetch all bookings for the current user
 * Note: The UserId is automatically added by the Kong gateway
 */
export async function getBookings(): Promise<GetBookingsResponse> {
  try {
    const response = await apiRequest<BookingDetails[]>(
      BOOKING_ENDPOINTS.GET_BOOKINGS,
      {
        method: "POST",
      },
      true
    );

    return {
      bookings: response,
      success: true
    };
  } catch (error) {
    console.error("Get bookings error:", error);
    return {
      success: false,
      bookings: [],
      message:
        error instanceof Error ? error.message : "Failed to fetch bookings",
    };
  }
}
