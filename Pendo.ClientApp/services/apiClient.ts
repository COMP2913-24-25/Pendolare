import { getJWTToken, logout } from "./authService";
import { API_BASE_URL } from "@/constants";

import { router } from "expo-router";

/*
  Make an API request to the gateway
  Returns the response data
*/
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  forceJsonParse: boolean = false,
  silentFail: boolean = true, // Flag to suppress specific errors
): Promise<T> {
  const jwt = await getJWTToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(jwt ? { Authorization: `Bearer ${jwt}` } : {}),
    ...(options.headers || {}),
  };

  let response: Response | null = null;

  try {

    response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    let data: any = null;

    const responseText = await response.text(); 

    if (!response.ok) {
        if (response.status === 401) {
            console.log("Received 401 Unauthorized. Logging out.");
            await logout();
            router.replace("/auth/signin");
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                data = { message: responseText || response.statusText || "Unauthorized" };
            }
        } else if (!silentFail) {
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                data = { message: responseText || `API request failed: ${response.statusText}` };
            }
        }
        // Throw error for non-ok responses, but respect silentFail for logging later
        throw new Error(data?.message || `API request failed with status ${response.status}`);
    }

    if (forceJsonParse) {
      console.log("Forcing JSON parse");
      try {
        data = JSON.parse(responseText);
        console.debug(`${endpoint} response:`, data);
      } catch (e) {
        console.error(`Failed to force JSON parse for ${endpoint}:`, e);
        throw new Error(`Invalid JSON received from ${endpoint}`);
      }
    } else {
        try {
            data = JSON.parse(responseText);
            console.debug(`${endpoint} response:`, data);
        } catch (e) {
             console.warn(`Response from ${endpoint} was not valid JSON, returning raw text.`);
             data = responseText;
        }
    }

    return data as T;
  } catch (error) {
    // Only log the error if silentFail is false
    if (!silentFail) {
      console.error(`API request failed for ${endpoint}:`, error); 
    }
    // Always re-throw the error to be handled by the caller service
    throw error; 
  }
}
