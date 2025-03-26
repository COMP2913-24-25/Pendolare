import * as SecureStore from "expo-secure-store";

import { apiRequest } from "./apiClient";

import { PAYMENT_ENDPOINTS } from "@/constants";

export interface BalanceSheet {
  UserId: string;
  Pending: number | 0.00;
  NonPending: number | 0.00;
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
        UserId: "NONE",
        Pending: -99,
        NonPending: -99
    };
  }
}