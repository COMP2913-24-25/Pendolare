import React from "react";
import { View } from "react-native";
import MapView from "react-native-maps";

const Map = () => {
  const randomLatitude = 37.78825;
  const randomLongitude = -122.4324;

  const region = {
    latitude: randomLatitude,
    longitude: randomLongitude,
    latitudeDelta: 0.0922,
    longitudeDelta: 0.0421,
  };

  return (
    <View style={{ flex: 1 }}>
      <MapView style={{ flex: 1 }} initialRegion={region} />
    </View>
  );
};

export default Map;
