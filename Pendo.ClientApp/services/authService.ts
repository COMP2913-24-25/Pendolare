import AsyncStorage from "@react-native-async-storage/async-storage";
import * as SecureStore from "expo-secure-store";

import { apiRequest } from "./apiClient";

import { AUTH_ENDPOINTS } from "@/constants";

const JWT_KEY = "pendolare";
const USER_EMAIL_KEY = "pendolare_email";
const IS_NEW_USER_KEY = "pendolare_is_new_user";

export const USER_FIRST_NAME_KEY = "userFirstName";
export const USER_LAST_NAME_KEY = "userLastName";
export const USER_RATING_KEY = "userRating";

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

interface UpdateUserResponse {
  success: boolean;
  message: string;
}

interface GetUserResponse {
  success: boolean;
  message: string;
  firstName: string;
  lastName: string;
  userRating: number;
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

/**
 * 
 * @param firstName the first name to update the user with.
 * @param lastName the last name to update the user with.
 * 
 * @returns a boolean indicating whether the user was successfully updated.
 */
export async function updateUser(firstName: string, lastName: string): Promise<boolean> {
  try {
    const jwt = await SecureStore.getItemAsync(JWT_KEY);
    if (!jwt) {
      return false;
    }

    const response = await apiRequest<UpdateUserResponse>(AUTH_ENDPOINTS.UPDATE_USER, {
      method: "PATCH",
      body: JSON.stringify({ firstName, lastName }),
      headers: {
        Authorization: `Bearer ${jwt}`,
      },
    });

    return response.success;
  } catch (error) {
    console.error("Update user error:", error);
    return false;
  }
}

/**
 * Get the user's first name, last name, and rating and store them in the secure store.
 * 
 * @returns the user's first name, last name, and rating, or an error message if the user is not authenticated / does not exist.
 */
export async function getUser(): Promise<GetUserResponse> {
  try {
    const jwt = await SecureStore.getItemAsync(JWT_KEY);
    if (!jwt) {
      return {
        success: false,
        message: "User not authenticated",
        firstName: "",
        lastName: "",
        userRating: -1,
      };
    }

    const response = await apiRequest<GetUserResponse>(AUTH_ENDPOINTS.GET_USER, {
      method: "POST",
      body: JSON.stringify({}),
      headers: {
        Authorization: `Bearer ${jwt}`,
      }
    });

    if (response.success) {
      // Store the user's details securely
      await AsyncStorage.setItem(USER_FIRST_NAME_KEY, response.firstName);
      await AsyncStorage.setItem(USER_LAST_NAME_KEY, response.lastName);
      await AsyncStorage.setItem(USER_RATING_KEY, response.userRating == -1 ? "N/A" : response.userRating.toString());
    }

    return response;
  } catch (error) {
    console.error("Get user error:", error);
    return {
      success: false,
      message: "Failed to get user",
      firstName: "",
      lastName: "",
      userRating: -1,
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
  Get the user's name
*/
export async function getUserObject(): Promise<{firstName: string | null, lastName: string | null, rating: string | null}> {
  const firstName = await AsyncStorage.getItem(USER_FIRST_NAME_KEY);
  const lastName = await AsyncStorage.getItem(USER_LAST_NAME_KEY);
  const rating = await AsyncStorage.getItem(USER_RATING_KEY);
  
  return { firstName, lastName, rating };
}

/*
  Set user data in AsyncStorage
*/
export async function setUserData(firstName?: string, lastName?: string, rating?: string): Promise<void> {
  if (firstName) await AsyncStorage.setItem(USER_FIRST_NAME_KEY, firstName);
  if (lastName) await AsyncStorage.setItem(USER_LAST_NAME_KEY, lastName);
  if (rating) await AsyncStorage.setItem(USER_RATING_KEY, rating);
}

/*
  Check if the user is a new user
*/
export async function isNewUser(): Promise<boolean> {
  const isNewUser = await SecureStore.getItemAsync(IS_NEW_USER_KEY);
  return isNewUser === "true";
}

/*
  Get the current user ID from JWT token
*/
export async function getCurrentUserId(): Promise<string | null> {
  try {
    const token = await getJWTToken();
    if (!token) {
      return null;
    }

    // JWT structure: header.payload.signature
    const parts = token.split('.');
    if (parts.length === 3) {
      const payload = JSON.parse(atob(parts[1]));
      // Extract user ID from the name identifier claim
      const userId = payload["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"];
      if (userId) {
        return userId;
      }
    }
    return null;
  } catch (error) {
    console.error("Failed to extract user ID from JWT:", error);
    return null;
  }
}

/*
  Log out by clearing the secure storage and async storage
*/
export async function logout(): Promise<void> {
  await SecureStore.deleteItemAsync(JWT_KEY);
  await SecureStore.deleteItemAsync(USER_EMAIL_KEY);
  await SecureStore.deleteItemAsync(IS_NEW_USER_KEY);

  await AsyncStorage.removeItem(USER_FIRST_NAME_KEY);
  await AsyncStorage.removeItem(USER_LAST_NAME_KEY);
  await AsyncStorage.removeItem(USER_RATING_KEY);
  console.log("Cleared auth tokens and user data.");
}
