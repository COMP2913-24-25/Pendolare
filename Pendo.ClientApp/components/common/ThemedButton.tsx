import React from "react";
import { TouchableOpacity, Text } from "react-native";

import { ButtonProps } from "@/types/type";

/*
  getBgVariantStyle
  Returns the background color based on the variant
*/
const getBgVariantStyle = (variant: ButtonProps["bgVariant"]) => {
  switch (variant) {
    case "secondary":
      return "bg-gray-500";
    case "danger":
      return "bg-red-500";
    case "success":
      return "bg-green-500";
    case "outline":
      return "bg-transparent border-neutral-300 border-[0.5px]";
    default:
      return "bg-[#0286FF]";
  }
};

/*
  getTextVariantStyle
  Returns the text color based on the variant
*/
const getTextVariantStyle = (variant: ButtonProps["textVariant"]) => {
  switch (variant) {
    case "primary":
      return "text-black";
    case "secondary":
      return "text-gray-100";
    case "danger":
      return "text-red-100";
    case "success":
      return "text-green-100";
    default:
      return "text-white";
  }
};

/* 
  CustomButton
  Custom button component with support for different variants and icons
*/
const Button = ({
  onPress,
  title,
  bgVariant = "primary",
  textVariant = "default",
  IconLeft,
  IconRight,
  className,
  disabled = false,
  ...props
}: ButtonProps) => {
  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled}
      className={`w-full rounded-full p-3 flex flex-row justify-center items-center shadow-md shadow-neutral-400/70 ${getBgVariantStyle(bgVariant)} ${className} ${
        disabled ? "opacity-60" : ""
      }`}
      {...props}
    >
      {IconLeft && <IconLeft />}
      
      {/* Conditionally render text if title isn't empty */}
      {title && (
        <Text className={`text-lg font-bold ${getTextVariantStyle(textVariant)}`}>
          {title}
        </Text>
      )}
      
      {IconRight && <IconRight />}
    </TouchableOpacity>
  );
};

export default Button;