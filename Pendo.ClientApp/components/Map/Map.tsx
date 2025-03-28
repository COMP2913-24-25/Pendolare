import { FontAwesome5 } from "@expo/vector-icons";
import axios from "axios";
import * as Location from "expo-location";
import { useEffect, useState, useRef } from "react";
import { View, StyleSheet, Platform, ActivityIndicator, Alert } from "react-native";
import MapView, { Marker, Polyline, PROVIDER_DEFAULT } from "react-native-maps";

import { icons } from "@/constants";
import { getRoute } from "@/services/locationService";

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
  const locationTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Set initial map region based on pickup/dropoff locations
  useEffect(() => {
    if (pickup && dropoff) {
      setMapRegion({
        latitude: (pickup.latitude + dropoff.latitude) / 2,
        longitude: (pickup.longitude + dropoff.longitude) / 2,
        latitudeDelta: Math.abs(pickup.latitude - dropoff.latitude) * 1.5,
        longitudeDelta: Math.abs(pickup.longitude - dropoff.longitude) * 1.5,
      });
      getRoute(pickup, dropoff, setRouteCoordinates);
    } else if (pickup) {
      setMapRegion({
        latitude: pickup.latitude,
        longitude: pickup.longitude,
        latitudeDelta: 0.0122,
        longitudeDelta: 0.0121,
      });
    } else if (dropoff) {
      setMapRegion({
        latitude: dropoff.latitude, 
        longitude: dropoff.longitude,
        latitudeDelta: 0.0122,
        longitudeDelta: 0.0121,
      });
    }
  }, [pickup, dropoff]);

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

    // Cleanup timeout on unmount
    return () => {
      if (locationTimeoutRef.current) {
        clearTimeout(locationTimeoutRef.current);
      }
    };
  }, [pickup, dropoff]);

  return (
    <View style={styles.container}>
      <MapView
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
            strokeWidth={4}
          />
        )}
      </MapView>
      {loading && (
        <View style={styles.loadingOverlay}>
          <ActivityIndicator size="large" color="#0000ff" />
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
  }
});

export default Map;
