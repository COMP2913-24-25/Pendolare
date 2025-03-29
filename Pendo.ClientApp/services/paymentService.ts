import { apiRequest } from "./apiClient";

import { PAYMENT_ENDPOINTS, ADMIN_ENDPOINTS } from "@/constants";

export interface WeeklyRevenue {
  week: number;
  total_income: number;
}

export interface BalanceSheet {
  Status: string;
  Pending: number;
  NonPending: number;
  Weekly: WeeklyRevenue[];
}

export interface StatusResponse {
  Status: string;
  Error: string;
}

export interface SingularPaymentMethod {
  Brand: string;
  Funding: string;
  Last4: string;
  Exp_month: number;
  Exp_year: number;
  PaymentType: string;
}
export interface Discount {
  // Update property names to match API response format
  DiscountId: string;
  WeeklyJourneys: number;
  DiscountPercentage: number;
  CreateDate: string;
}
export interface PaymentMethodResponse {
  Status: string;
  Methods: Array<SingularPaymentMethod>
}

export interface PaymentSheetResponse {
  Status: string,
  PaymentIntent: string,
  EphemeralKey: string,
  CustomerId: string,
  PublishableKey: string
}

/*
 * Get PaymentMethods
 * Note: The UserId is automatically added by the Kong gateway
 */
export async function PaymentMethods(): Promise<PaymentMethodResponse> {
  try {
    const response = await apiRequest<PaymentMethodResponse>(
      PAYMENT_ENDPOINTS.PAYMENT_METHODS,
      {
        method: "POST",
        body: JSON.stringify({}),
      },
      true
    );

    return response;

  } catch (error) {
    console.error("View Balance error:", error);
    return {
      Status: "fail",
      Methods: []
    };
  }
}

/*
 * Post PayoutRequest
 * Note: The UserId is automatically added by the Kong gateway
 */
export async function PayoutRequest(): Promise<StatusResponse> {
  try {
    const response = await apiRequest<StatusResponse>(
      PAYMENT_ENDPOINTS.CREATE_PAYOUT,
      {
        method: "POST",
        body: JSON.stringify({}),
      },
      true
    );

    return response;

  } catch (error) {
    console.error("Payout error:", error);
    return {
      Status: "fail",
      Error: String(error)
    };
  }
}

/*
 * Post ViewBalance
 * Note: The UserId is automatically added by the Kong gateway
 */
export const ViewBalance = async (): Promise<BalanceSheet> => {
  try {
    const response = await apiRequest<BalanceSheet>(
      PAYMENT_ENDPOINTS.VIEW_BALANCE,
      {
        method: "POST",
        body: JSON.stringify({}),
      },
      true
    );
    console.log("FETCHING BALANCE SHEET")
    console.log(response)

    return response;

  } catch (error) {
    console.error("Payout error:", error);
    return {
      Status: "fail",
      Pending: 0.00,
      NonPending: 0.00,
      Weekly: [],
    };
  }
};

/*
 * Fetch PaymentSheet Parameters
 * Returns neccecary attributes for presentation of payment sheet
*/
export const fetchPaymentSheetParams = async (amount: number) => {
  const response = await apiRequest<PaymentSheetResponse>(
    PAYMENT_ENDPOINTS.PAYMENT_SHEET,
    {
      method: "POST",
      body: JSON.stringify({ Amount: amount }),
    },
    true
  );

  const { PaymentIntent, EphemeralKey, CustomerId } = await response

  return {
      PaymentIntent, 
      EphemeralKey,
      CustomerId
  }
}

/**
 * Fetches available discounts from the Admin API
 * @returns Array of discount options
 */
export const getDiscounts = async (): Promise<Discount[]> => {
  try {
    const response = await apiRequest<Discount[]>(
      ADMIN_ENDPOINTS.GET_DISCOUNTS,
      {
        method: "GET"
      },
      true
    );
    return response;
  } catch (error) {
    console.error("Error fetching discounts:", error);
    return [];
  }
};

/**
 * Finds the appropriate discount based on number of journeys per week
 * @param journeysPerWeek Number of journeys per week
 * @returns The matching discount or null if none found
 */
export const findDiscountForJourneys = async (journeysPerWeek: number): Promise<Discount | null> => {
  try {
    const discounts = await getDiscounts();
    
    // Sort descending by weekly journeys to find the highest applicable discount
    const sortedDiscounts = discounts.sort((a, b) => b.WeeklyJourneys - a.WeeklyJourneys);
    
    // Find the first discount where weekly journeys is less than or equal to requested amount
    return sortedDiscounts.find(d => journeysPerWeek >= d.WeeklyJourneys) || null;
  } catch (error) {
    console.error("Error finding discount:", error);
    return null;
  }
};