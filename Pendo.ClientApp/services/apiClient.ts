import { getJWTToken } from "./authService";
import { API_BASE_URL } from "@/constants";

/*
  Make an API request to the gateway
  Returns the response data
*/
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const jwt = await getJWTToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(jwt ? { Authorization: `Bearer ${jwt}` } : {}),
    ...(options.headers || {}),
  };

  try {

    console.log(headers)
    console.log(options.body)
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    console.log(response);

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || `API request failed: ${response}`);
    }

    return data;
  } catch (error) {
    console.error(`API request failed for ${endpoint}:`, error);
    throw error;
  }
}
