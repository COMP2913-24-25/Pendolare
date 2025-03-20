import { apiRequest } from "./apiClient";

import { BOOKING_ENDPOINTS } from "@/constants";

export interface AddBookingAmmendmentRequest {
  BookingId: string;
  ProposedPrice: number | null;
  StartName: string | null;
  StartLong: number | null;
  StartLat: number | null;
  EndName: string | null;
  EndLong: number | null;
  EndLat: number | null;
  StartTime: Date | null;
  DriverApproval: boolean;
  PassengerApproval: boolean;
}

export interface CompleteBookingRequest {
  Completed: boolean;
}

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
    if (typeof journeyId === "undefined")
      throw new Error("Journey ID is required to create a booking");

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

export async function addBookingAmmendment(bookingAmmendment : AddBookingAmmendmentRequest) : Promise<BookingResponse> {
  try{
    console.log(`Adding booking ammendment for booking ${bookingAmmendment.BookingId}`);

    const response = await apiRequest<BookingResponse>(
      BOOKING_ENDPOINTS.ADD_BOOKING_AMMENDMENT,
      {
        method: "POST",
        body: JSON.stringify(bookingAmmendment)
      }
    );

    return {
      ...response
    };

  } catch (error) {
    console.error("Add booking ammendment error:", error);
    return {
      success: false,
      message:
        error instanceof Error ? error.message : "Failed to add booking ammendment.",
    };
  }
}

export async function approveBookingAmmendment(bookingAmmendmentId : string) : Promise<BookingResponse> {
  try {
    console.log(`Approving booking ammendment ${bookingAmmendmentId}`);

    const response = await apiRequest<BookingResponse>(
      `${BOOKING_ENDPOINTS.ADD_BOOKING_AMMENDMENT}/${bookingAmmendmentId}`,
      {
        method: "PUT",
        body: JSON.stringify({})
      },
    );

    return {
      ...response
    };
  } catch (error) {
    console.error("Approve booking ammendment error:", error);
    return {
      success: false,
      message:
        error instanceof Error ? error.message : "Failed to approve booking ammendment.",
    };
  }
}

export async function approveBooking(bookingId: string) : Promise<BookingResponse> {
  try {
    console.log(`Approving booking ${bookingId}`);

    const response = await apiRequest<BookingResponse>(
      `${BOOKING_ENDPOINTS.APPROVE_BOOKING}/${bookingId}`,
      {
        method: "PUT",
        body: JSON.stringify({})
      },
    );

    return {
      ...response
    };
  } catch (error) {
    console.error("Approve booking error:", error);
    return {
      success: false,
      message:
        error instanceof Error ? error.message : "Failed to approve booking",
    };
  }
}

export async function cancelBooking(bookingId: string, reason: string): Promise<BookingResponse> {
  try {
    console.log(`Cancelling booking ${bookingId} with reason: ${reason}`);
    // Replace with actual API call
    await Promise.resolve();

    return {
      success: true,
    };
  } catch (error) {
    console.error("Cancel booking error:", error);
    return {
      success: false,
      message:
        error instanceof Error ? error.message : "Failed to cancel booking",
    };
  }
}

export async function confirmAtPickup(bookingId: string) : Promise<BookingResponse> {
  try {
    console.log("Confirming at pickup");

    const response = await apiRequest<BookingResponse>(
      `${BOOKING_ENDPOINTS.CONFIRM_AT_PICKUP}/${bookingId}`,
      {
        method: "POST",
        body: JSON.stringify({})
      });

    return {
      ...response
    };

  } catch (error) {
    console.error("Confirm at pickup error:", error);
    return {
      success: false,
      message:
        error instanceof Error ? error.message : "Failed to confirm at pickup",
    };
  }
}

export async function completeBooking(completed: boolean) : Promise<BookingResponse> {
  try {
    console.log("Completing booking");

    const response = await apiRequest<BookingResponse>(
      BOOKING_ENDPOINTS.COMPLETE_BOOKING,
      {
        method: "POST",
        body: JSON.stringify({ Completed: completed }),
      });

    return {
      ...response
    };
  } catch (error) {
    console.error("Complete booking error:", error);
    return {
      success: false,
      message:
        error instanceof Error ? error.message : "Failed to complete booking",
    };
  }
}