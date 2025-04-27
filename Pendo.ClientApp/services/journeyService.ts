import { apiRequest } from "./apiClient";
import { JOURNEY_ENDPOINTS } from "@/constants";

export interface JourneyDetails {
    JourneyId: string;
    UserId: string;
    User_: any;
    BootHeight: number;
    BootWidth: number;
    StartDate: Date;
    JourneyType: number;
    AdvertisedPrice: number;
    MaxPassengers: number;
    DistanceRadius: number;
    StartName: string;
    EndName: string;
    StartLat: number;
    StartLong: number;
    EndLat: number;
    EndLong: number;
    SortByPrice: "string";
    Recurrance: string;
    RepeatUntil: Date
    JourneyStatusId: number;
}

export interface GetJourneyResponse {
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
    EndDate?: string;
    JourneyType?: number;
    MaxPrice?: number;
    NumPassengers?: number;
    DistanceRadius?: number;
    StartLat?: number;
    StartLong?: number;
    EndLat?: number;
    EndLong?: number;
    SortByPrice?: string;
    DriverView: boolean;
}

export async function getJourneys(filters?: GetJourneysRequest): Promise<GetJourneyResponse> {
    try {
        console.log("Getting journeys with filters:", filters);
        const response = await apiRequest<JourneyDetails[]>(
            JOURNEY_ENDPOINTS.GET_JOURNEYS,
            {
                method: "POST",
                body: JSON.stringify(filters || {})
            },
            true
        );
        
        return {
            success: true,
            journeys: response
        }
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
