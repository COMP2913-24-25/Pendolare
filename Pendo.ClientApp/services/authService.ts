import * as SecureStore from "expo-secure-store";

import { apiRequest } from "./apiClient";

import { AUTH_ENDPOINTS } from "@/constants";

const JWT_KEY = "pendolare";
const USER_EMAIL_KEY = "pendolare_email";
const IS_NEW_USER_KEY = "pendolare_is_new_user";

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

/* 
  Request an OTP for the given email address
  Returns a success flag and an optional error message
*/
export async function requestOTP(emailAddress: string): Promise<OTPResponse> {
  try {
    console.log(JSON.stringify({ emailAddress: emailAddress }));
    const response = await apiRequest<OTPResponse>(AUTH_ENDPOINTS.REQUEST_OTP, {
      method: "POST",
      body: JSON.stringify({ emailAddress: emailAddress }),
    });

    await SecureStore.setItemAsync(USER_EMAIL_KEY, emailAddress);

    return {
      ...response,
      success: true,
    };
  } catch (error) {
    console.error("Request OTP error:", error);
    return {
      success: false,
      message:
        error instanceof Error
          ? error.message
          : "Network error. Please try again.",
    };
  }
}

/*
  Verify the OTP for the given email address
  Returns a JWT token if successful, or an error message if verification fails
*/
export async function verifyOTP(otp: string): Promise<VerifyOTPResponse> {
  try {
    const emailAddress = await SecureStore.getItemAsync(USER_EMAIL_KEY);
    
    if (!emailAddress) {
      return {
        jwt: "",
        isNewUser: false,
        authenticated: false,
        error: "No email address found. Please request an OTP first.",
      };
    }


    console.log(JSON.stringify({ emailAddress, otp }));
    
    const response = await apiRequest<VerifyOTPResponse>(AUTH_ENDPOINTS.VERIFY_OTP, {
      method: "POST",
      body: JSON.stringify({ emailAddress, otp }),
    });

    if (response.jwt) {
      // Store JWT token in secure storage
      await SecureStore.setItemAsync(JWT_KEY, response.jwt);
      // Store user status
      await SecureStore.setItemAsync(IS_NEW_USER_KEY, response.isNewUser.toString());
      
      return {
        ...response,
        authenticated: true,
      };
    }

    return {
      jwt: "",
      isNewUser: false,
      authenticated: false,
      error: response.error || "Failed to verify OTP.",
    };
  } catch (error) {
    console.error("Verify OTP error:", error);
    return {
      jwt: "",
      isNewUser: false,
      authenticated: false,
      error: error instanceof Error ? error.message : "Network error. Please try again.",
    };
  }
}

/*
  Check if the user is authenticated by verifying the JWT token exists
*/
export async function isAuthenticated(): Promise<boolean> {
  const jwt = await SecureStore.getItemAsync(JWT_KEY);
  return !!jwt;
}

/*
  Get the JWT token from secure storage
*/
export async function getJWTToken(): Promise<string | null> {
  return SecureStore.getItemAsync(JWT_KEY);
}

/*
  Check if the user is a new user
*/
export async function isNewUser(): Promise<boolean> {
  const isNewUser = await SecureStore.getItemAsync(IS_NEW_USER_KEY);
  return isNewUser === "true";
}

/*
  Log out by clearing the secure storage
*/
export async function logout(): Promise<void> {
  await SecureStore.deleteItemAsync(JWT_KEY);
  await SecureStore.deleteItemAsync(USER_EMAIL_KEY);
  await SecureStore.deleteItemAsync(IS_NEW_USER_KEY);
}
