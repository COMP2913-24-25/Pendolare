import * as SecureStore from "expo-secure-store";

import { apiRequest } from "./apiClient";

import { PAYMENT_ENDPOINTS } from "@/constants";


export const USER_PENDING_BALANCE = "userPendingBalance";
export const USER_NON_PENDING_BALANCE = "userNonPendingBalance";

export interface BalanceSheet {
  Status: string;
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

    if (response.Status) {
        await SecureStore.setItemAsync(USER_PENDING_BALANCE, response.Pending.toString());
        await SecureStore.setItemAsync(USER_NON_PENDING_BALANCE, response.NonPending.toString());
    }
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