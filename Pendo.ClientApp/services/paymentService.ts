import { apiRequest } from "./apiClient";

import { PAYMENT_ENDPOINTS } from "@/constants";

export interface BalanceSheet {
  Status: string;
  Pending: number | 0.00;
  NonPending: number | 0.00;
  Weekly: any[];
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
export async function ViewBalance(): Promise<BalanceSheet> {
  try {
    const response = await apiRequest<BalanceSheet>(
      PAYMENT_ENDPOINTS.VIEW_BALANCE,
      {
        method: "POST",
        body: JSON.stringify({}),
      },
      true
    );

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
}

export const fetchPaymentSheetParams = async (amount: number) => {
        const response = await apiRequest<PaymentSheetResponse>(
            PAYMENT_ENDPOINTS.PAYMENT_SHEET,
            {
                method: "POST",
                body: JSON.stringify({Amount: amount}),
            },
            true
        );

        const {PaymentIntent, EphemeralKey, CustomerId} = await response

        return {
            PaymentIntent, 
            EphemeralKey,
            CustomerId
        }
} 

