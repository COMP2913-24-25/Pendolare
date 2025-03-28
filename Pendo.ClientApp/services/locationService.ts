import axios from "axios";

/**
 * Get a route between two points
 * @param pickup The pickup location
 * @param dropoff The dropoff location
 * @param onProgress Optional callback to receive coordinates as they're processed
 * @returns Array of coordinates representing the route
 */
export const getRoute = async (
  pickup: { latitude: number; longitude: number },
  dropoff: { latitude: number; longitude: number },
  onProgress?: (coordinates: { latitude: number; longitude: number }[]) => void
): Promise<{ latitude: number; longitude: number }[]> => {
  // Validate coordinates to prevent API errors
  if (!pickup || !dropoff || 
      typeof pickup.latitude !== 'number' || typeof pickup.longitude !== 'number' ||
      typeof dropoff.latitude !== 'number' || typeof dropoff.longitude !== 'number' ||
      isNaN(pickup.latitude) || isNaN(pickup.longitude) ||
      isNaN(dropoff.latitude) || isNaN(dropoff.longitude)) {
    console.error("Invalid coordinates provided to getRoute:", { pickup, dropoff });
    return [];
  }
  
  try {
    // Log the request for debugging
    console.log(`Calculating route from ${pickup.latitude},${pickup.longitude} to ${dropoff.latitude},${dropoff.longitude}`);
    
    // Use a more detailed route request with alternatives and steps
    const response = await axios.get(
      `https://router.project-osrm.org/route/v1/driving/${pickup.longitude},${pickup.latitude};${dropoff.longitude},${dropoff.latitude}?overview=full&alternatives=false&steps=true&geometries=geojson`,
      { timeout: 5000 } // Add timeout to avoid long-hanging requests
    );

    if (
      response.data &&
      response.data.routes &&
      response.data.routes.length > 0 &&
      response.data.routes[0].geometry &&
      response.data.routes[0].geometry.coordinates
    ) {
      // Extract coordinates from the response
      const coordinates = response.data.routes[0].geometry.coordinates.map(
        (coord: [number, number]) => ({
          latitude: coord[1],
          longitude: coord[0],
        })
      );
      
      // Early return if no coordinates are found
      // This is a safeguard, as the above checks should ensure coordinates exist
      if (!coordinates || coordinates.length === 0) {
        console.warn("No valid coordinates returned from routing service");
        return [];
      }
      
      // Simplify the route if it has too many points to improve performance
      let simplifiedCoords = coordinates;
      if (coordinates.length > 100) {
        // Take every nth point to reduce the number of points
        simplifiedCoords = coordinates.filter((_: any, index: number) => index % Math.ceil(coordinates.length / 100) === 0);
        // Always include start and end points
        if (simplifiedCoords.length >= 2) {
          simplifiedCoords[0] = coordinates[0];
          simplifiedCoords[simplifiedCoords.length - 1] = coordinates[coordinates.length - 1];
        }
      }
      
      // Call progress callback if provided
      if (onProgress) {
        onProgress(simplifiedCoords);
      }

      return simplifiedCoords;
    } else {
      console.warn("Invalid route response structure:", response.data);
      return [];
    }
  } catch (error) {
    console.error("Error fetching route:", error);
    
    // Try a fallback to straight line if the routing service fails
    if (pickup && dropoff) {
      const straightLineRoute = [
        { latitude: pickup.latitude, longitude: pickup.longitude },
        { latitude: dropoff.latitude, longitude: dropoff.longitude },
      ];
      
      console.log("Using straight line route as fallback");
      
      // Call progress callback if provided
      if (onProgress) {
        onProgress(straightLineRoute);
      }
      
      return straightLineRoute;
    }
    
    return [];
  }
}

/**
 * Search for locations using the OpenRouteService API.
 * 
 * @param query The search query
 * @param type The type of location being searched for (pickup or dropoff)
 * @param onSearching Callback function to be called when the search is in progress
 * @param onSearchComplete Callback function to be called when the search is complete
 * 
 * @returns list of locations matching the search query.
 */
export async function searchLocations(query: string, type: "pickup" | "dropoff", onSearching: any | null, onSearchComplete: any | null) {
    if (query.length < 3) return;

    console.log(`Searching for location: [${query}]`);

    if (onSearching) {
        onSearching(type);
    }

    try {
      // Make a GET request to the OpenRouteService API with boundary coordinates
      const response = await axios.get(
        `https://api.openrouteservice.org/geocode/search`,
        {
          params: {
            api_key: process.env.EXPO_PUBLIC_OSR_KEY,
            text: query,
            "boundary.rect.min_lat": "49.674",
            "boundary.rect.max_lat": "61.061",
            "boundary.rect.min_lon": "-8.178",
            "boundary.rect.max_lon": "1.987",
            // Limit search results to UK only
            sources: "openstreetmap",
          },
        },
      );

      if (response.data.features) {
        // Map the response data to a simplified location object
        if(onSearchComplete) {
            onSearchComplete(
                response.data.features.map((feature: any) => ({
                  name: feature.properties.label,
                  latitude: feature.geometry.coordinates[1],
                  longitude: feature.geometry.coordinates[0],
                })),
            );
        }
      }
    } catch (error) {
      console.error("Location search error:", error);
    }
};