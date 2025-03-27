import React from "react";
import { Modal, Text, View, ScrollView, TouchableOpacity } from "react-native";
import { FontAwesome5 } from "@expo/vector-icons";
import { icons } from "@/constants";

export interface SubRide {
    journeyId: string;
    journeyDate: Date;
    price: number;
    parent: any;
}

export interface Discount {
    name: string;
    amount: number;
}

interface CheckoutModalProps {
    subrides: SubRide[];
    discount?: Discount;
    userBalance: number;
    visible: boolean;
    onClose: () => void;
    isDarkMode: boolean;
    onConfirm: () => void;
}

const CheckoutModal = ({
    subrides,
    discount,
    userBalance,
    visible,
    onClose,
    isDarkMode,
    onConfirm,
}: CheckoutModalProps) => {
    const subTotalPrice: number = subrides.reduce((sum, ride) => sum + ride.price, 0) ?? 0;
    const totalPrice: number = subTotalPrice * (1 - (discount?.amount ?? 0));

    return (
        <Modal visible={visible} onRequestClose={onClose} animationType="slide">
            <View className={`flex-1 ${isDarkMode ? "bg-slate-900" : "bg-white"} p-6 pt-12`}>
                {/* Header */}
                <View className="flex-row items-center justify-between mb-6">
                    <TouchableOpacity
                        onPress={onClose}
                        className={`p-2 rounded-full ${isDarkMode ? "bg-slate-800" : "bg-gray-200"}`}
                    >
                        <FontAwesome5 name={icons.backArrow} size={24} color={isDarkMode ? "#FFF" : "#000"} />
                    </TouchableOpacity>
                    <Text className={`text-xl font-bold ${isDarkMode ? "text-white" : "text-black"}`}>
                        Checkout
                    </Text>
                    <View className="w-10" />
                </View>

                {/* Price Breakdown */}
                <ScrollView className="flex-1 mb-4">
                    <Text className="text-xl font-bold mb-3">Price Breakdown</Text>
                    <View className="p-3 rounded-lg border border-gray-200 shadow-2xl">
                        <Text className="text-lg font-bold pt-2 border-t">Rides</Text>
                        {subrides.map((subride, index) => (
                            <View key={index} className="flex-row justify-between py-2">
                                <Text className={`text-md ${isDarkMode ? "text-gray-200" : "text-gray-800"}`}>
                                    &nbsp;Ride on {subride.journeyDate.toLocaleString()}
                                </Text>
                                <Text className={`text-md font-bold ${isDarkMode ? "text-gray-200" : "text-gray-800"}`}>
                                    £{subride.price.toFixed(2)}
                                </Text>
                            </View>
                        ))}

                        {/* Discounts Applied - needs to be implemented properly */}
                        {discount && (
                            <View className="py-3 border-y border-gray-400">
                                <Text className={`text-lg font-bold ${isDarkMode ? "text-gray-300" : "text-gray-700"}`}>
                                    Discounts Applied
                                </Text>
                                <View className="flex-row justify-between">
                                    <Text className={`text-md ${isDarkMode ? "text-gray-300" : "text-gray-700"}`}>
                                        {discount.name} ({(discount.amount * 100).toFixed(2)}%)
                                    </Text>
                                    <Text className={`text-md ${isDarkMode ? "text-gray-300" : "text-gray-700"}`}>
                                        - £{(subTotalPrice * discount.amount).toFixed(2)}
                                    </Text>
                                </View>
                            </View>
                        )}

                        {/* User balance section */}
                        <View className="py-3 border-b border-gray-400">
                            <Text className={`text-lg font-bold ${isDarkMode ? "text-gray-300" : "text-gray-700"}`}>
                                User Balance
                            </Text>
                            <View className="flex-row justify-between">
                                <Text className={`text-md ${isDarkMode ? "text-gray-300" : "text-gray-700"}`}>
                                    User Balance
                                </Text>
                                <Text className={`text-md ${isDarkMode ? "text-gray-300" : "text-gray-700"}`}>
                                    - £{totalPrice.toFixed(2)}
                                </Text>
                            </View>
                            <View className="flex-row justify-between py-1">
                                <Text className={`text-md ${isDarkMode ? "text-gray-300" : "text-gray-700"}`}>
                                    Remaining Balance
                                </Text>
                                <Text className={`text-md font-bold ${isDarkMode ? "text-gray-300" : "text-gray-700"}`}>
                                    £{(userBalance - totalPrice).toFixed(2)}
                                </Text>
                            </View>
                        </View>
                    </View>

                </ScrollView>

                {/* Total Price */}
                <View className="border-t border-gray-400 py-4">
                    <View className="flex-row justify-between border-b border-gray-400 pb-2">
                        <Text className={`text-lg ${isDarkMode ? "text-white" : "text-black"}`}>
                            Subtotal
                        </Text>
                        <Text className={`text-lg ${isDarkMode ? "text-white" : "text-black"}`}>
                            £{subTotalPrice.toFixed(2)}
                        </Text>
                    </View>
                    <View className="flex-row justify-between py-2">
                        <Text className={`text-xl font-bold ${isDarkMode ? "text-white" : "text-black"}`}>
                            Total
                        </Text>
                        <Text className={`text-xl font-bold ${isDarkMode ? "text-white" : "text-black"}`}>
                            £{totalPrice.toFixed(2)}
                        </Text>
                    </View>
                </View>

                {/* Confirm Button */}
                <TouchableOpacity
                    onPress={onConfirm}
                    className={`w-full py-4 rounded-lg items-center ${isDarkMode ? "bg-blue-500" : "bg-blue-600"}`}
                >
                    <Text className="text-white text-md font-bold">Confirm</Text>
                </TouchableOpacity>
            </View>
        </Modal>
    );
};

export default CheckoutModal;
