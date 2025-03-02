import * as SecureStore from "expo-secure-store";

import { API_BASE_URL, AUTH_ENDPOINTS } from "@/constants";

const JWT_KEY = "pendolino_jwt";
const USER_EMAIL_KEY = "pendolino_email";
const IS_NEW_USER_KEY = "pendolino_is_new_user";

interface OTPResponse {
  success: boolean;
  message?: string;
}

interface VerifyOTPResponse {
  jwt: string;
  isNewUser: boolean;
  authenticated: boolean;
  error?: string;
}

export async function requestOTP(emailAddress: string): Promise<OTPResponse> {
  try {
    console.log(JSON.stringify({ emailAddress: emailAddress }));
    const response = await fetch(
      `${API_BASE_URL}${AUTH_ENDPOINTS.REQUEST_OTP}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ emailAddress: emailAddress }),
      },
    );
    console.log(response);

    if (response.status === 200) {
      // Store email for later use
      await SecureStore.setItemAsync(USER_EMAIL_KEY, emailAddress);
      return { success: true };
    }

    return {
      success: false,
      message: "Failed to send verification code",
    };
  } catch (error) {
    console.error("Request OTP error:", error);
    return {
      success: false,
      message: "Network error. Please try again.",
    };
  }
}

export async function verifyOTP(
  email: string,
  otp: string,
): Promise<VerifyOTPResponse> {
  try {
    const response = await fetch(
      `${API_BASE_URL}${AUTH_ENDPOINTS.VERIFY_OTP}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: email, otp: otp }),
      },
    );

    const data = await response.json();

    if (data.authenticated) {
      // Store JWT and user status
      await SecureStore.setItemAsync(JWT_KEY, data.jwt);
      await SecureStore.setItemAsync(IS_NEW_USER_KEY, String(data.isNewUser));
      return data;
    }

    return {
      ...data,
      error: "Invalid verification code. Please try again.",
    };
  } catch (error) {
    console.error("Verify OTP error:", error);
    return {
      jwt: "",
      isNewUser: false,
      authenticated: false,
      error: "Network error. Please try again.",
    };
  }
}

export async function getJWT(): Promise<string | null> {
  return await SecureStore.getItemAsync(JWT_KEY);
}

export async function getUserEmail(): Promise<string | null> {
  return await SecureStore.getItemAsync(USER_EMAIL_KEY);
}

export async function getIsNewUser(): Promise<boolean> {
  const value = await SecureStore.getItemAsync(IS_NEW_USER_KEY);
  return value === "true";
}

export async function logout(): Promise<void> {
  await SecureStore.deleteItemAsync(JWT_KEY);
  await SecureStore.deleteItemAsync(IS_NEW_USER_KEY);
  // We keep the email for convenience
}

export async function isAuthenticated(): Promise<boolean> {
  const jwt = await getJWT();
  return !!jwt;
}
