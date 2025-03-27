import { View, TouchableOpacity, ScrollView, TextInput } from "react-native";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import { SafeAreaView } from "react-native-safe-area-context";
import { useState, useEffect } from "react";
import { FontAwesome5 } from "@expo/vector-icons";
import { router } from "expo-router";
import { icons } from "@/constants";
import ThemedButton from "@/components/common/ThemedButton";

/*
  Checkout
  Page to allow a user to select the amount they wish to top up on their account
*/
const Checkout = () => {
  const { isDarkMode } = useTheme();


  const [selectedAmount, setSelectedAmount] = useState<number | null>(null);
  const [customAmount, setCustomAmount] = useState('');

  const predefinedOptions = [10, 20, 50, 100];

  const handleTopUp = () => {
    const amountToTopUp = customAmount || selectedAmount;
    if (amountToTopUp) {
      alert(`You are topping up £${amountToTopUp}`);
    } else {
      alert('Please select or enter an amount to top up.');
    }
  };

  return (
    <SafeAreaView
      className={`flex-1 pt-2 ${isDarkMode ? "bg-slate-900" : "bg-general-500"}`}
    >
      <View className="flex-1 px-4">
        <View className="flex-row items-center my-5">
          <TouchableOpacity onPress={() => router.back()} className="mr-4">
              <FontAwesome5
                name={icons.backArrow}
                size={24}
                color={isDarkMode ? "#FFF" : "#000"}
              />
            </TouchableOpacity>
            <Text
            className={`text-2xl font-JakartaExtraBold ${
              isDarkMode ? "text-white" : "text-black"
            }`}
          >
            Top Up Balance
          </Text>
        </View>
                
        {/* Tabs */}
        <View
          className={`flex-row rounded-xl p-1 mb-4`}
        >
          {predefinedOptions.map((amount) => (
          <TouchableOpacity
          key={amount}
          className={`flex-1 py-2 rounded-lg`}
          style = {{borderColor: "#000", 
                    borderWidth: 2, 
                    minHeight: 100,
                    margin: 5, 
                    justifyContent: "center", 
                    alignItems: "center", 
                    backgroundColor: selectedAmount === amount ? "#385975" : isDarkMode ? "#fff" : "#fff" }}
          onPress={() => {
            setCustomAmount('');
            setSelectedAmount(amount);
          }}
        >
          <Text
            className={`text-center text-xl font-JakartaSemiBold`}
            style = {{
              color: selectedAmount === amount? "#fff" : "#000"
            }}
          >
            {"£" + amount}
          </Text>
        </TouchableOpacity>
        ))}
        </View>

        <View className="bg-white rounded-lg p-4 shadow-md" style = {{marginVertical: 20}}>
                <Text className="font-JakartaSemiBold text-lg">Or enter a custom amount:</Text>
                <TextInput
                    keyboardType="numeric"
                    value={customAmount ? `£${customAmount}` : ""}
                    onChangeText={(value) => {
                      // remove the £ symbol
                      const numericValue = value.replace(/^£/, "");
                
                      if (numericValue === "") {
                        setCustomAmount("");
                        setSelectedAmount(null);
                      } else {
                        // validate with regex to ensure two dp
                        const validValue = numericValue.match(/^\d*\.?\d{0,2}$/) ? numericValue : customAmount;
                
                        // ensure the value is within range 2.00 to 100.00
                        const valueInRange =
                          parseFloat(validValue) >= 1.00 && parseFloat(validValue) <= 100.00
                            ? validValue
                            : customAmount;
    
                        setCustomAmount(valueInRange);
                        setSelectedAmount(null);
                      }
                    }}
                    placeholder="Enter amount"
                    className="text-gray-500 text-lg"
                  />
        </View>

      <ThemedButton title="Top Up" onPress={handleTopUp} style={{marginVertical: 20}}/>

      </View>
    </SafeAreaView>
  );
};

export default Checkout;