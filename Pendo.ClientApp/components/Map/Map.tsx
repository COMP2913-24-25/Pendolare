import { FontAwesome5 } from "@expo/vector-icons";
import axios from "axios";
import * as Location from "expo-location";
import { useEffect, useState } from "react";
import { View, StyleSheet, Platform, ActivityIndicator, Alert } from "react-native";
import MapView, { Marker, Polyline, PROVIDER_DEFAULT } from "react-native-maps";

import { icons } from "@/constants";

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
  const [loading, setLoading] = useState(true);

  /*
    Fetch User Location
    Fetch user's current location using Expo Location API 
    Derived from: https://docs.expo.dev/versions/latest/sdk/location/
  */
  useEffect(() => {
    (async () => {
      try {
        const { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') {
          Alert.alert('Permission Denied', 'Location permission is required for this feature');
          setLoading(false);
          return;
        }

        const currentLocation = await Location.getCurrentPositionAsync({
          accuracy: Location.Accuracy.Highest,
        });
        
        console.log("Current location fetched:", currentLocation.coords);
        setUserLocation(currentLocation.coords);
        
        // Update map region based on user location
        setMapRegion({
          latitude: currentLocation.coords.latitude,
          longitude: currentLocation.coords.longitude,
          latitudeDelta: 0.0922,
          longitudeDelta: 0.0421,
        });
        
        setLoading(false);
      } catch (error) {
        console.error("Error getting location:", error);
        setLoading(false);
      }
    })();
  }, []);

  /*
    Fetch Route
    Fetch route from OpenRouteService API
  */
  useEffect(() => {
    if (pickup && dropoff) {
      setMapRegion({
        latitude: (pickup.latitude + dropoff.latitude) / 2,
        longitude: (pickup.longitude + dropoff.longitude) / 2,
        latitudeDelta: Math.abs(pickup.latitude - dropoff.latitude) * 1.5,
        longitudeDelta: Math.abs(pickup.longitude - dropoff.longitude) * 1.5,
      });

      /*
        Fetch route from OpenRouteService API
        Derived from: https://openrouteservice.org/dev/#/api-docs/directions/get
      */
      const fetchRoute = async () => {
        const response = await axios.get(
          `https://api.openrouteservice.org/v2/directions/driving-car?api_key=${process.env.EXPO_PUBLIC_OSR_KEY}&start=${pickup.longitude},${pickup.latitude}&end=${dropoff.longitude},${dropoff.latitude}`,
        );
        const coordinates = response.data.features[0].geometry.coordinates;
        /*
          Convert coordinates to points for Polyline
          Derived from: https://github.com/react-native-maps/react-native-maps/blob/master/docs/polyline.md
        */
        const points = coordinates.map(
          ([longitude, latitude]: [number, number]) => ({
            latitude,
            longitude,
          }),
        );
        setRouteCoordinates(points);
      };

      fetchRoute();
    }
  }, [pickup, dropoff]);

  return (
    <View style={styles.container}>
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        <MapView
          provider={PROVIDER_DEFAULT}
          style={styles.map}
          initialRegion={mapRegion}
          region={mapRegion}
          onMapReady={() => setIsMapReady(true)}
          showsUserLocation={true}
          showsMyLocationButton={true}
          followsUserLocation={true}
        >
          {/* Always show user location marker if available */}
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
  }
});

export default Map;
