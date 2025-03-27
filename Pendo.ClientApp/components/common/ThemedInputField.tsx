import * as React from "react";
import {
  TextInput,
  View,
  Image,
  KeyboardAvoidingView,
  TouchableWithoutFeedback,
  Keyboard,
  Platform,
} from "react-native";

import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import { InputFieldProps } from "@/types/type";

/*
  InputField
  Renders a text input field with a label and optional icon
  Uses the current theme for styling
*/
const InputField = ({
  label,
  icon,
  secureTextEntry = false,
  labelStyle,
  containerStyle,
  inputStyle,
  iconStyle,
  className,
  ...props
}: InputFieldProps) => {
  const { isDarkMode } = useTheme();

  return (
    // KeyboardAvoidingView and TouchableWithoutFeedback are used to dismiss the keyboard when tapping outside the input
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <View className="my-2 w-full">
          <Text className={`text-lg font-JakartaSemiBold mb-3 ${labelStyle}`}>
            {label}
          </Text>
          <View
            className={`flex flex-row justify-start items-center relative rounded-full border
              ${
                isDarkMode
                  ? "bg-slate-700 border-slate-600"
                  : "bg-neutral-100 border-neutral-100"
              } ${containerStyle}`}
          >
            {icon && (
              <Image
                source={icon}
                className={`w-6 h-6 ml-4 ${iconStyle}`}
                style={{ tintColor: isDarkMode ? "#FFF" : undefined }}
              />
            )}
            <TextInput
              className={`rounded-full p-4 font-JakartaSemiBold text-[15px] flex-1 
                ${isDarkMode ? "text-white" : "text-black"} 
                ${inputStyle}`}
              placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
              secureTextEntry={secureTextEntry}
              {...props}
            />
          </View>
        </View>
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
};

export default InputField;