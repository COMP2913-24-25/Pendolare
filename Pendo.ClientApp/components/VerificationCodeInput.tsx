import React, { useRef, useState } from "react";
import { View, TextInput, StyleSheet } from "react-native";

import { useTheme } from "@/context/ThemeContext";

interface VerificationCodeInputProps {
  code: string;
  onCodeChange: (code: string) => void;
}

/*
  VerificationCodeInput
  Renders 6 input fields for entering a verification code
  Calls onCodeChange callback with the full code string
  Based on: https://medium.com/@medranomiler/simplifying-otp-input-in-react-native-fc601d73d346
*/
const VerificationCodeInput = ({
  code,
  onCodeChange,
}: VerificationCodeInputProps): JSX.Element => {
  const { isDarkMode } = useTheme();
  const inputRefs = useRef<TextInput[]>([]);
  const [focusedIndex, setFocusedIndex] = useState<number>(0);

  // Handle code change and focus next input
  const handleCodeChange = (text: string, index: number) => {
    const newCode = code.split("");
    newCode[index] = text;
    const newCodeString = newCode.join("");
    onCodeChange(newCodeString);

    if (text.length === 1 && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  // Handle backspace key press and focus previous input
  const handleKeyPress = (event: any, index: number) => {
    if (event.nativeEvent.key === "Backspace" && index > 0 && !code[index]) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  // Render 6 input fields for verification code
  return (
    <View className="flex-row justify-between w-full">
      {[0, 1, 2, 3, 4, 5].map((index) => (
        <TextInput
          key={index}
          ref={(ref) => ref && (inputRefs.current[index] = ref)}
          className={`w-12 h-14 text-center text-xl font-JakartaBold rounded-lg ${
            isDarkMode
              ? "bg-slate-700 text-white border-slate-600"
              : "bg-neutral-100 text-black border-neutral-200"
          } ${focusedIndex === index ? "border-2 border-blue-500" : "border"}`}
          maxLength={1}
          keyboardType="numeric"
          value={code[index] || ""}
          onChangeText={(text) => handleCodeChange(text, index)}
          onKeyPress={(event) => handleKeyPress(event, index)}
          onFocus={() => setFocusedIndex(index)}
          onBlur={() => setFocusedIndex(-1)}
        />
      ))}
    </View>
  );
};

export default VerificationCodeInput;
