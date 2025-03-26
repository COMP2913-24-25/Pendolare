import { apiRequest } from "./apiClient";

import { PAYMENT_ENDPOINTS } from "@/constants";

export interface BalanceSheet {
  Status: string;
  Pending: number | 0.00;
  NonPending: number | 0.00;
}

export interface PaymentSheetResponse {
    Status: string,
    PaymentIntent: string,
    EphemeralKey: string,
    CustomerId: string,
    PublishableKey: string
}
/*
 * Get PaymentSheet
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

    return response;

  } catch (error) {
    console.error("View Balance error:", error);
    return {
        Status: "fail",
        Pending: -99,
        NonPending: -99
    };
  }
}

export const fetchPaymentSheetParams = async () => {
        const response = await apiRequest<PaymentSheetResponse>(
            PAYMENT_ENDPOINTS.PAYMENT_SHEET,
            {
                method: "POST",
                body: JSON.stringify({Amount: 11.50}),
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