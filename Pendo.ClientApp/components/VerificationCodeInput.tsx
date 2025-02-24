import React, { useRef, useState } from "react";
import { View, TextInput, StyleSheet } from "react-native";

import { useTheme } from "@/context/ThemeContext";

interface VerificationCodeInputProps {
  code: string;
  onCodeChange: (code: string) => void;
}

const VerificationCodeInput: React.FC<VerificationCodeInputProps> = ({
  code,
  onCodeChange,
}) => {
  const { isDarkMode } = useTheme();
  const inputRefs = useRef<TextInput[]>([]);
  const [focusedIndex, setFocusedIndex] = useState<number>(0);

  const handleCodeChange = (text: string, index: number) => {
    const newCode = code.split("");
    newCode[index] = text;
    const newCodeString = newCode.join("");
    onCodeChange(newCodeString);

    if (text.length === 1 && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyPress = (event: any, index: number) => {
    if (event.nativeEvent.key === "Backspace" && index > 0 && !code[index]) {
      inputRefs.current[index - 1]?.focus();
    }
  };

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
