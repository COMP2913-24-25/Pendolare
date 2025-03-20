import { apiRequest } from "./apiClient";
import { JOURNEY_ENDPOINTS } from "@/constants";

interface JourneyDetails {
    BootHeight: number;
    BootWidth: number;
    StartDate: Date;
    JourneyType: number;
    MaxPrice: number;
    NumPassengers: number;
    DistanceRadius: number;
    StartLat: number;
    StartLong: number;
    EndLat: number;
    EndLong: number;
    SortByPrice: "string"
}

interface GetJourneyResponse {
    success: boolean;
    journeys: JourneyDetails[];
    message?: string;
}

export interface CreateJourneyRequest {
    AdvertisedPrice?: number;
    StartName?: string;
    StartLong?: number;
    StartLat?: number;
    EndName?: string;
    EndLong?: number;
    EndLat?: number;
    StartDate?: string;
    RepeatUntil?: string;
    StartTime?: string;
    MaxPassengers?: number;
    RegPlate?: string;
    CurrencyCode?: string;
    JourneyType?: number;
    Recurrance?: string;
    JourneyStatusId: number;
    BootWidth: number;
    BootHeight: number;
    LockedUntil?: string;
}

// New: interface for filtering journeys
export interface GetJourneysRequest {
    BootHeight?: number;
    BootWidth?: number;
    StartDate?: string;
    JourneyType?: number;
    MaxPrice?: number;
    NumPassengers?: number;
    DistanceRadius?: number;
    StartLat?: number;
    StartLong?: number;
    EndLat?: number;
    EndLong?: number;
    SortByPrice?: string;
}

export async function getJourneys(filters?: GetJourneysRequest): Promise<GetJourneyResponse> {
    try {
        console.log("Getting journeys with filters:", filters);
        const response = await apiRequest<any>(
            JOURNEY_ENDPOINTS.GET_JOURNEYS,
            {
                method: "POST",
                body: JSON.stringify(filters || {})
            }
        );
        // If response does not have "journeys", assume response is the array of journeys.
        if (!("journeys" in response)) {
            return {
                success: true,
                journeys: Array.isArray(response) ? response : [],
            };
        }
        // Ensure that response has a success property.
        if (typeof response.success === "undefined") {
            response.success = true;
        }
        return { ...response };
    } catch (error) {
        console.error("Get journeys error:", error);
        return {
            success: false,
            journeys: [],
            message:
                error instanceof Error ? error.message : "Failed to get journeys.",
        };
    }
}

export async function createJourney(payload: CreateJourneyRequest): Promise<any> {
    try {
        payload.BootHeight = 0;
        payload.BootWidth = 0;
        payload.CurrencyCode = "GBP";
        payload.LockedUntil = new Date().toISOString();
        const response = await apiRequest<any>(
            JOURNEY_ENDPOINTS.CREATE_JOURNEY,
            {
                method: "POST",
                body: JSON.stringify(payload),
            },
            true
        );
        return response;
    } catch (error) {
        console.error("Create journey error:", error);
        throw error;
    }
}
