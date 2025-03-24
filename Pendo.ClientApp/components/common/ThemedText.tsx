import * as React from "react";
import { Text as RNText, TextProps } from "react-native";
import { useTheme } from "@/context/ThemeContext";

// The Text component applies theme-based color automatically.
export function Text({ style, ...props }: TextProps) {
	const { isDarkMode } = useTheme();
	return (
		<RNText
			style={[{ color: isDarkMode ? "#FFFFFF" : "#000000" }, style]}
			{...props}
		/>
	);
}
