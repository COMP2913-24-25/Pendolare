import { apiRequest } from "./apiClient";

import { BOOKING_ENDPOINTS } from "@/constants";

export interface AddBookingAmmendmentRequest {
  CancellationRequest: any;
  BookingId: string;
  ProposedPrice: number | null;
  StartName: string | null;
  StartLong: number | null;
  StartLat: number | null;
  EndName: string | null;
  EndLong: number | null;
  EndLat: number | null;
  StartTime: string | null;
  DriverApproval: boolean;
  PassengerApproval: boolean;
  // Add commuter schedule amendment fields
  ScheduleAmendment?: boolean;
  RecurrenceCron?: string;
  RepeatUntil?: string;
}

// Update the interface to match what the server expects
export interface ApproveBookingAmmendmentRequest {
  DriverApproval: boolean;
  PassengerApproval: boolean;
  CancellationRequest: boolean;
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
  BookingAmmendmentId?: string; // Add this to support the server response format
  Status?: string; // Add this to support the server response format
  Message?: string; // Add this to support the server response format
  success?: boolean;
  message?: string;
}

// Add new User interface
export interface User {
  UserId: string;
  Name?: string;
  FullName?: string;
  FirstName?: string;
  LastName?: string;
  Email?: string;
  // Add other user properties as needed
}

export interface BookingDetails {
  Booking: {
    BookingId: string;
    User: User; // Update to use the User interface
    FeeMargin: number;
    RideTime: Date;
    BookedWindowEnd?: Date;
  };
  BookingStatus: {
    StatusId: number;
    Status: string;
    Description: string;
  },
  Journey: {
    JourneyId: string;
    User: User; // Update to use the User interface
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
    Recurrance?: string;
    RepeatUntil?: Date;
  }
}

export interface GetBookingsResponse {
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
  journeyTime: Date,
  bookedWindowEnd: Date | null = null
): Promise<BookingResponse> {
  try {
    // Convert journey ID to string if it's a number (for dummy data)
    if (typeof journeyId === "undefined")
      throw new Error("Journey ID is required to create a booking");

    const stringJourneyId = journeyId.toString();

    const response = await apiRequest<BookingResponse>(
      BOOKING_ENDPOINTS.CREATE_BOOKING,
      {
        method: "POST",
        body: JSON.stringify({
          JourneyId: stringJourneyId,
          JourneyTime: journeyTime.toISOString().split("Z")[0],
          EndCommuterWindow: bookedWindowEnd?.toISOString().split("Z")[0],
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
export async function getBookings(driverView: boolean = false): Promise<GetBookingsResponse> {
  try {
    const response = await apiRequest<BookingDetails[]>(
      BOOKING_ENDPOINTS.GET_BOOKINGS,
      {
        method: "POST",
        body: JSON.stringify({ DriverView: driverView }),
      },
      true
    );

    // Add additional preprocessing to ensure structure integrity
    const processedBookings = response.map((booking: any) => {
      // Ensure Journey object exists and has all required properties
      if (!booking.Journey) {
        booking.Journey = {};
      }
      
      // Ensure Booking object exists
      if (!booking.Booking) {
        booking.Booking = {};
      }
      
      // Ensure BookingStatus object exists
      if (!booking.BookingStatus) {
        booking.BookingStatus = { Status: 'Unknown' };
      }
      
      return booking;
    });

    return {
      bookings: processedBookings,
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

export async function addBookingAmmendment(bookingAmmendment: AddBookingAmmendmentRequest): Promise<BookingResponse> {
  try {
    console.log(`Adding booking ammendment for booking ${bookingAmmendment.BookingId}`);

    const response = await apiRequest<BookingResponse>(
      BOOKING_ENDPOINTS.ADD_BOOKING_AMMENDMENT,
      {
        method: "POST",
        body: JSON.stringify(bookingAmmendment)
      }
    );

    // Normalise the response to ensure it has success property
    return {
      ...response,
      success: response.success || response.Status === "Success"
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

export async function approveBookingAmmendment(
  bookingAmmendmentId: string, 
  isCancellation: boolean = false,
  isDriverApproving: boolean = true
): Promise<BookingResponse> {
  try {
    console.log(`Approving booking ammendment ${bookingAmmendmentId} (Cancellation: ${isCancellation}, Driver: ${isDriverApproving})`);

    const approvalRequest = {
      DriverApproval: isDriverApproving,
      PassengerApproval: !isDriverApproving,
      CancellationRequest: isCancellation
    };

    console.log("Sending approval request payload:", JSON.stringify(approvalRequest));

    const response = await apiRequest<BookingResponse>(
      `${BOOKING_ENDPOINTS.APPROVE_BOOKING_AMMENDMENT}/${bookingAmmendmentId}`,
      {
        method: "PUT",
        body: JSON.stringify(approvalRequest)
      },
    );

    return {
      ...response,
      success: response.success || response.Status === "Success"
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

export async function approveBooking(bookingId: string): Promise<BookingResponse> {
  try {
    console.log(`Approving booking ${bookingId}`);

    const response = await apiRequest<BookingResponse>(
      `${BOOKING_ENDPOINTS.APPROVE_BOOKING}/${bookingId}`,
      {
        method: "PUT",
        body: JSON.stringify({})
      },
      false,
      true //Silently fail. 403 is expected if there are booking ammendments.
    );

    return {
      ...response
    };
  } catch (error) {
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
    await Promise.resolve(); // use the bookingAmmendment endpoint!

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

export async function confirmAtPickup(bookingId: string): Promise<BookingResponse> {
  try {
    console.log("Confirming at pickup");

    const response = await apiRequest<BookingResponse>(
      `${BOOKING_ENDPOINTS.CONFIRM_AT_PICKUP}/${bookingId}`,
      {
        method: "PUT",
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

export async function completeBooking(bookingId: string, completed: boolean): Promise<BookingResponse> {
  try {
    console.log("Completing booking");

    const response = await apiRequest<BookingResponse>(
      `${BOOKING_ENDPOINTS.COMPLETE_BOOKING}/${bookingId}`,
      {
        method: "PUT",
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

/**
 * Rebooks an expired commuter journey
 * Preserves the original booking duration instead of using a fixed 30-day period
 * 
 * @param journeyId The ID of the journey to rebook
 * @param options Optional parameters to customize rebooking
 * @returns Success status and message
 */
export const rebookCommuterJourney = async (
  journeyId: string,
  options?: {
    startDate?: Date;
    customDuration?: number;
  }
): Promise<{success: boolean; message?: string}> => {
  try {
    // Default start date is today
    const startDate = options?.startDate || new Date();
    
    // First try to get the original journey details to determine duration
    let originalDuration = options?.customDuration;
    
    if (!originalDuration) {
      try {
        const journeyResponse = await getJourneys({
          DriverView: true
        });
        
        if (journeyResponse.success) {
          // Find the specific journey
          const originalJourney = journeyResponse.journeys.find(j => 
            j.JourneyId === journeyId && j.JourneyType === 2 // Make sure it's a commuter journey
          );
          
          if (originalJourney && originalJourney.RepeatUntil) {
            // Calculate the original duration in milliseconds
            const originalStartDate = new Date(originalJourney.StartDate);
            const originalEndDate = new Date(originalJourney.RepeatUntil);
            const originalDurationMs = originalEndDate.getTime() - originalStartDate.getTime();
            
            // Convert to days, minimum 7 days, maximum 90 days
            originalDuration = Math.max(7, Math.min(90, Math.ceil(originalDurationMs / (1000 * 60 * 60 * 24))));
            console.log(`Using original booking duration of ${originalDuration} days`);
          }
        }
      } catch (error) {
        console.warn("Could not determine original journey duration:", error);
      }
      
      // Default to 30 days if original duration is not found
      originalDuration = originalDuration || 30;
    }
    
    // Calculate end date based on duration
    const endDate = new Date(startDate);
    endDate.setDate(endDate.getDate() + originalDuration);
    
    // Use the existing createBooking function
    const result = await createBooking(journeyId, startDate, endDate);
    
    return {
      success: result.success || result.Status === "Success",
      message: result.message || result.Message
    };
  } catch (error) {
    console.error("Error rebooking commuter journey:", error);
    return {
      success: false,
      message: "An unexpected error occurred while rebooking"
    };
  }
};