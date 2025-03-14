import { FontAwesome5 } from "@expo/vector-icons";
import axios from "axios";
import * as Location from "expo-location";
import { useEffect, useState } from "react";
import { View, Platform, Text } from "react-native";
import MapView, { Marker, Polyline, PROVIDER_DEFAULT } from "react-native-maps";
import ThemedView from "@/components/common/ThemedView";

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
  const [userLocation, setUserLocation] =
    useState<Location.LocationObjectCoords | null>(null);
  const [mapRegion, setMapRegion] = useState({
    latitude: 53.8008, // Leeds default
    longitude: -1.5491,
    latitudeDelta: 0.0922,
    longitudeDelta: 0.0421,
  });
  const [routeCoordinates, setRouteCoordinates] = useState([]);

  useEffect(() => {
    const requestLocationPermission = async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        console.log("Permission to access location was denied");
        return;
      }

      let location = await Location.getCurrentPositionAsync({});
      setUserLocation(location.coords);
      setMapRegion({
        latitude: location.coords.latitude,
        longitude: location.coords.longitude,
        latitudeDelta: 0.0922,
        longitudeDelta: 0.0421,
      });
    };

    requestLocationPermission();
  }, []);

  useEffect(() => {
    if (pickup && dropoff) {
      setMapRegion({
        latitude: (pickup.latitude + dropoff.latitude) / 2,
        longitude: (pickup.longitude + dropoff.longitude) / 2,
        latitudeDelta: Math.abs(pickup.latitude - dropoff.latitude) * 1.5,
        longitudeDelta: Math.abs(pickup.longitude - dropoff.longitude) * 1.5,
      });

      // Fetch route from OpenRouteService API
      const fetchRoute = async () => {
        const response = await axios.get(
          `https://api.openrouteservice.org/v2/directions/driving-car?api_key=${process.env.EXPO_PUBLIC_OSR_KEY}&start=${pickup.longitude},${pickup.latitude}&end=${dropoff.longitude},${dropoff.latitude}`,
        );
        const coordinates = response.data.features[0].geometry.coordinates;
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

  const onMapReady = () => {
    setIsMapReady(true);
  };

  // Map view with markers for pickup and dropoff locations
  // Utilising: https://github.com/react-native-maps/react-native-maps

  return (
    <ThemedView
      className="flex-1 items-center justify-center"
      lightStyle="bg-gray-200"
      darkStyle="bg-slate-700"
    >
      <Text>Map Placeholder</Text>
      <View style={{ flex: 1 }}>
        <MapView
          style={{ flex: 1 }}
          initialRegion={mapRegion}
          region={mapRegion}
          provider={Platform.select({
            ios: PROVIDER_DEFAULT,
            android: PROVIDER_DEFAULT,
          })}
          onMapReady={onMapReady}
          loadingEnabled={true}
          showsUserLocation={true}
          followsUserLocation={true}
        >
          {isMapReady && pickup && (
            <Marker
              coordinate={pickup}
              title="Pickup Location"
              description={pickup.name}
            >
              <View className="bg-blue-600 p-2 rounded-full">
                <FontAwesome5 name={icons.car} size={24} color="#FFF" />
              </View>
            </Marker>
          )}

          {isMapReady && dropoff && (
            <Marker
              coordinate={dropoff}
              title="Destination"
              description={dropoff.name}
            >
              <View className="bg-red-600 p-2 rounded-full">
                <FontAwesome5 name={icons.flag} size={24} color="#FFF" />
              </View>
            </Marker>
          )}

          {isMapReady && routeCoordinates.length > 0 && (
            <Polyline
              coordinates={routeCoordinates}
              strokeColor="#2563EB"
              strokeWidth={3}
            />
          )}
        </MapView>
      </View>
    </ThemedView>
  );
};

export default Map;
