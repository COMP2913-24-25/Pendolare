import axios from "axios";
import React, { useEffect, useState } from "react";
import { View, Image, Platform } from "react-native";
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

const Map = ({ pickup, dropoff }: MapProps) => {
  const [isMapReady, setIsMapReady] = useState(false);
  const [mapRegion, setMapRegion] = useState({
    latitude: pickup?.latitude || 37.78825,
    longitude: pickup?.longitude || -122.4324,
    latitudeDelta: 0.0922,
    longitudeDelta: 0.0421,
  });
  const [routeCoordinates, setRouteCoordinates] = useState([]);

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

  return (
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
      >
        {isMapReady && pickup && (
          <Marker
            coordinate={pickup}
            title="Pickup Location"
            description={pickup.name}
          >
            <Image
              source={icons.marker}
              style={{ width: 40, height: 40, tintColor: "#2563EB" }}
            />
          </Marker>
        )}

        {isMapReady && dropoff && (
          <Marker
            coordinate={dropoff}
            title="Destination"
            description={dropoff.name}
          >
            <Image
              source={icons.marker}
              style={{ width: 40, height: 40, tintColor: "#DC2626" }}
            />
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
  );
};

export default Map;
