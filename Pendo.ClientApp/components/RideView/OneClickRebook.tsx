import React from 'react'
import { View, Text, TouchableOpacity } from 'react-native'

interface Props {
  onRebook: () => void
}

export default function RebookCommuterJourney({ onRebook }: Props) {
  return (
    <View className="flex-1 justify-center items-center bg-white mt-2">
      <TouchableOpacity onPress={onRebook} className="bg-blue-500 rounded-full px-6 py-3 shadow-lg">
        <Text className="text-white text-xs font-semibold">Rebook Journey for next 2 week period!</Text>
      </TouchableOpacity>
    </View>
  )
}
