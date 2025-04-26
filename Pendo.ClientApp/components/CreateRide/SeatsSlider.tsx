import React from 'react';
import { View, Text } from 'react-native';
import Slider from '@react-native-community/slider';
import { FontAwesome5 } from '@expo/vector-icons';

interface Props {
  seats: string;
  setSeats: (val: string) => void;
  minSeats: number;
  maxSeats: number;
  isDarkMode: boolean;
}

export function SeatSlider({
  seats,
  setSeats,
  minSeats,
  maxSeats,
  isDarkMode,
}: Props) {
  const current = Number(seats) || minSeats;

  const StepMarker = (props: any) => {
    return (
      <View
        style={{
          width: props.size,
          height: props.size,
          borderRadius: 100,
          backgroundColor: isDarkMode ? '#fff' : '#000',
          alignSelf: 'center',
          marginTop: props.marginTop,
          zIndex: -1,
        }}
      />
    );
  };

  return (
    <View className="mb-4">
      <Text className={`text-lg font-JakartaBold mb-2 ${isDarkMode ? 'text-white' : 'text-black'}`}>
        Available Seats: {current}
      </Text>

      {/* Seat icons */}
      <View className="flex-row mb-1 items-center justify-center">
        {Array.from({ length: maxSeats }, (_, i) => (
          <FontAwesome5
            key={i}
            name="chair"
            solid={i < current}
            size={30}
            color={
              i < current
                ? isDarkMode
                  ? '#fff'
                  : '#000'
                : isDarkMode
                ? '#888'
                : '#ccc'
            }
            style={{ marginRight: 6 }}
          />
        ))}
      </View>

      {/* Slider */}
      <View className="relative">
        <Slider
          style={{ width: '100%', height: 40 }}
          minimumValue={minSeats}
          maximumValue={maxSeats}
          step={1}
          tapToSeek={true}
          value={current}
          minimumTrackTintColor={isDarkMode ? '#fff' : '#000'}
          maximumTrackTintColor={isDarkMode ? '#555' : '#ccc'}
          thumbTintColor={isDarkMode ? '#fff' : '#000'}
          onValueChange={(val) => {
            setSeats(val.toString());
          }}
          StepMarker={() => {return (
          <StepMarker 
            size={12} 
            marginTop={4}
          />);}}
        />
      </View>

    </View>
  );
}