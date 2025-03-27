import axios from "axios";

const baseUrl = "https://api.openrouteservice.org";

/**
 * Get the route between two locations using the OpenRouteService API.
 * 
 * @param pickup The pickup location
 * @param dropoff The dropoff location
 * @param setRouteCoordinates Callback function to set the route coordinates
 * 
 * @returns list of coordinates for the route between the two locations.
 */
export async function getRoute(pickup : any, dropoff : any, setRouteCoordinates : any = null)
{
    const response = await axios.get(
        `${baseUrl}/v2/directions/driving-car?api_key=${process.env.EXPO_PUBLIC_OSR_KEY}&start=${pickup.longitude},${pickup.latitude}&end=${dropoff.longitude},${dropoff.latitude}`,
      );
    const coordinates = response.data.features[0].geometry.coordinates;

    const points = coordinates.map(
        ([longitude, latitude]: [number, number]) => ({
          latitude,
          longitude,
        }),
      );

    if (setRouteCoordinates != null) {
        setRouteCoordinates(points);
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
        `${baseUrl}/geocode/search`,
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