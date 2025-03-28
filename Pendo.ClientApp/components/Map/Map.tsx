import { FontAwesome5 } from "@expo/vector-icons";
import axios from "axios";
import * as Location from "expo-location";
import { useEffect, useState, useRef } from "react";
import { View, StyleSheet, Platform, ActivityIndicator, Text as RNText } from "react-native";
import MapView, { Marker, Polyline, PROVIDER_DEFAULT } from "react-native-maps";

import { icons } from "@/constants";
import { getRoute } from "@/services/locationService";
import { Text } from "@/components/common/ThemedText";

interface Location {
  latitude: number;
  longitude: number;
  name?: string;
}

interface MapProps {
  pickup: Location | null;
  dropoff: Location | null;
}

/*
  Map
  Component for rendering a map with pickup and dropoff locations
*/
const Map = ({ pickup, dropoff }: MapProps) => {
  const [isMapReady, setIsMapReady] = useState(false);
  const [userLocation, setUserLocation] = useState<Location.LocationObjectCoords | null>(null);
  const [mapRegion, setMapRegion] = useState({
    latitude: 53.8008, // Leeds default
    longitude: -1.5491,
    latitudeDelta: 0.0922,
    longitudeDelta: 0.0421,
  });
  const [routeCoordinates, setRouteCoordinates] = useState<{latitude: number, longitude: number}[]>([]);
  const [loading, setLoading] = useState(false);
  const [routeLoading, setRouteLoading] = useState(false);
  const [routeError, setRouteError] = useState<string | null>(null);
  const locationTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const retryTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const retryCountRef = useRef(0);
  const mapViewRef = useRef<MapView>(null);

  // Set initial map region based on pickup/dropoff locations
  useEffect(() => {
    // Validate pickup and dropoff coordinates first
    const validPickup = pickup && typeof pickup.latitude === 'number' && typeof pickup.longitude === 'number';
    const validDropoff = dropoff && typeof dropoff.latitude === 'number' && typeof dropoff.longitude === 'number';
    
    if (validPickup && validDropoff) {
      setMapRegion({
        latitude: (pickup.latitude + dropoff.latitude) / 2,
        longitude: (pickup.longitude + dropoff.longitude) / 2,
        latitudeDelta: Math.abs(pickup.latitude - dropoff.latitude) * 1.5,
        longitudeDelta: Math.abs(pickup.longitude - dropoff.longitude) * 1.5,
      });
      fetchRoute(pickup, dropoff);
    } else if (validPickup) {
      setMapRegion({
        latitude: pickup.latitude,
        longitude: pickup.longitude,
        latitudeDelta: 0.0122,
        longitudeDelta: 0.0121,
      });
    } else if (validDropoff) {
      setMapRegion({
        latitude: dropoff.latitude, 
        longitude: dropoff.longitude,
        latitudeDelta: 0.0122,
        longitudeDelta: 0.0121,
      });
    }

    // Clear any existing retry timeouts when props change
    if (retryTimeoutRef.current) {
      clearTimeout(retryTimeoutRef.current);
      retryTimeoutRef.current = null;
    }
    retryCountRef.current = 0;
  }, [pickup, dropoff]);

  // Fetch route with improved error handling and retry logic
  const fetchRoute = async (start: Location, end: Location) => {
    // Validate coordinates before attempting to fetch route
    if (!start || !end || 
        start.latitude === undefined || start.longitude === undefined || 
        end.latitude === undefined || end.longitude === undefined) {
      console.log("Invalid coordinates, cannot fetch route", { start, end });
      setRouteError("Invalid location coordinates");
      return;
    }
    
    try {
      setRouteLoading(true);
      setRouteError(null);
      
      console.log(`Fetching route from ${start.latitude},${start.longitude} to ${end.latitude},${end.longitude}`);
      
      const result = await getRoute(start, end, (coords) => {
        if (coords && coords.length > 0) {
          setRouteCoordinates(coords);
          setRouteLoading(false);
          
          // Fit map to the route with some padding
          if (mapViewRef.current && coords.length > 0) {
            mapViewRef.current.fitToCoordinates(coords, {
              edgePadding: { top: 50, right: 50, bottom: 50, left: 50 },
              animated: true
            });
          }
        }
      });
      
      if (!result || result.length === 0) {
        throw new Error("Failed to fetch route data");
      }
      
    } catch (error) {
      console.error("Error fetching route:", error);
      setRouteError("Couldn't calculate route");
      setRouteLoading(false);
      
      // Create a straight line route as fallback
      const straightLineRoute = [
        { latitude: start.latitude, longitude: start.longitude },
        { latitude: end.latitude, longitude: end.longitude }
      ];
      setRouteCoordinates(straightLineRoute);
      
      // Only retry if it wasn't an invalid coordinate issue
      if (retryCountRef.current < 2) {
        retryCountRef.current += 1;
        console.log(`Retrying route calculation (${retryCountRef.current}/2)...`);
        
        retryTimeoutRef.current = setTimeout(() => {
          fetchRoute(start, end);
        }, 2000); // Retry after 2 seconds
      }
    }
  };

  /*
    Fetch User Location
    Fetch user's current location using Expo Location API in the background
    Derived from: https://docs.expo.dev/versions/latest/sdk/location/
  */
  useEffect(() => {
    const fetchLocation = async () => {
      try {
        const { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') {
          console.log('Permission to access location was denied');
          return;
        }

        // Set a timeout to stop waiting for location after 5 seconds
        locationTimeoutRef.current = setTimeout(() => {
          console.log("Location fetch timed out");
          if (locationTimeoutRef.current) {
            clearTimeout(locationTimeoutRef.current);
          }
        }, 5000);

        const currentLocation = await Location.getCurrentPositionAsync({
          accuracy: Location.Accuracy.Balanced,
        });
        
        if (locationTimeoutRef.current) {
          clearTimeout(locationTimeoutRef.current);
        }
        
        console.log("Current location fetched:", currentLocation.coords);
        setUserLocation(currentLocation.coords);
        
        // Only update map region if no pickup/dropoff points are set
        if (!pickup && !dropoff) {
          setMapRegion({
            latitude: currentLocation.coords.latitude,
            longitude: currentLocation.coords.longitude,
            latitudeDelta: 0.0922,
            longitudeDelta: 0.0421,
          });
        }
      } catch (error) {
        console.error("Error getting location:", error);
        if (locationTimeoutRef.current) {
          clearTimeout(locationTimeoutRef.current);
        }
      }
    };

    fetchLocation();

    // Cleanup timeouts on unmount
    return () => {
      if (locationTimeoutRef.current) {
        clearTimeout(locationTimeoutRef.current);
      }
      if (retryTimeoutRef.current) {
        clearTimeout(retryTimeoutRef.current);
      }
    };
  }, [pickup, dropoff]);

  return (
    <View style={styles.container}>
      <MapView
        ref={mapViewRef}
        provider={PROVIDER_DEFAULT}
        style={styles.map}
        initialRegion={mapRegion}
        region={mapRegion}
        onMapReady={() => setIsMapReady(true)}
        showsUserLocation={true}
        showsMyLocationButton={true}
      >
        {/* Only show user location marker if available */}
        {isMapReady && userLocation && (
          <Marker
            coordinate={{
              latitude: userLocation.latitude,
              longitude: userLocation.longitude,
            }}
            title="You are here"
          >
            <View style={styles.userMarker}>
              <FontAwesome5 name={icons.marker} size={16} color="#2563EB" />
            </View>
          </Marker>
        )}
        
        {isMapReady && pickup && (
          <Marker
            coordinate={{
              latitude: pickup.latitude,
              longitude: pickup.longitude,
            }}
            title="Pickup"
          >
            <View style={styles.pickupMarker}>
              <FontAwesome5 name={icons.marker} size={24} color="#22C55E" />
            </View>
          </Marker>
        )}
        
        {isMapReady && dropoff && (
          <Marker
            coordinate={{
              latitude: dropoff.latitude,
              longitude: dropoff.longitude,
            }}
            title="Dropoff"
          >
            <View style={styles.dropoffMarker}>
              <FontAwesome5 name={icons.target} size={24} color="#EF4444" />
            </View>
          </Marker>
        )}
        
        {isMapReady && routeCoordinates.length > 0 && (
          <Polyline
            coordinates={routeCoordinates}
            strokeColor="#2563EB"
            strokeWidth={2.5} // Reduced from 4 to 2.5 for a thinner line
            lineDashPattern={[0]}
            lineCap="round"
            lineJoin="round"
          />
        )}
      </MapView>
      
      {/* Main loading overlay */}
      {loading && (
        <View style={styles.loadingOverlay}>
          <ActivityIndicator size="large" color="#0000ff" />
        </View>
      )}
      
      {/* Route calculation indicator */}
      {routeLoading && pickup && dropoff && (
        <View style={styles.routeLoadingContainer}>
          <View style={styles.routeLoadingBox}>
            <ActivityIndicator size="small" color="#2563EB" />
            <RNText style={styles.routeLoadingText}>Calculating route...</RNText>
          </View>
        </View>
      )}
      
      {/* Route error indicator */}
      {routeError && (
        <View style={styles.routeErrorContainer}>
          <View style={styles.routeErrorBox}>
            <FontAwesome5 name="exclamation-triangle" size={16} color="#EF4444" />
            <RNText style={styles.routeErrorText}>{routeError}</RNText>
          </View>
        </View>
      )}
    </View>
  );
};

/*
  Custom styles for Map component
  Derived from: https://github.com/react-native-maps/react-native-maps/blob/master/example/src/examples/CustomMarkers.tsx
*/
const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: '100%',
    height: 300,
    overflow: 'hidden',
  },
  map: {
    width: '100%',
    height: '100%',
  },
  userMarker: {
    padding: 3,
    backgroundColor: 'white',
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#2563EB',
  },
  pickupMarker: {
    padding: 2,
    borderRadius: 10,
  },
  dropoffMarker: {
    padding: 2,
    borderRadius: 10,
  },
  loadingOverlay: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.5)',
  },
  routeLoadingContainer: {
    position: 'absolute',
    top: 10,
    left: 0,
    right: 0,
    alignItems: 'center',
    zIndex: 1000,
  },
  routeLoadingBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  routeLoadingText: {
    marginLeft: 8,
    fontSize: 14,
    color: '#2563EB',
    fontWeight: '500',
  },
  routeErrorContainer: {
    position: 'absolute',
    top: 10,
    left: 0,
    right: 0,
    alignItems: 'center',
    zIndex: 1000,
  },
  routeErrorBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  routeErrorText: {
    marginLeft: 8,
    fontSize: 14,
    color: '#EF4444',
    fontWeight: '500',
  }
});

export default Map;
