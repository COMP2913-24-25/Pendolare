import { router } from "expo-router";
import { useRef, useState, useEffect } from "react";
import { Image, Text, TouchableOpacity, View, Animated, Dimensions } from "react-native";
import Swiper from "react-native-swiper";

import Button from "@/components/common/ThemedButton";
import { onboarding } from "@/constants";
import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";

const { width, height } = Dimensions.get("window");

/*
  OnBoarding
  Screen for onboarding new users
*/
const OnBoarding = () => {
  const { isLoggedIn } = useAuth();
  const { isDarkMode } = useTheme();
  const swiperRef = useRef<Swiper>(null);
  const [activeIndex, setActiveIndex] = useState(0);
  
  // Force showing onboarding for now
  const shouldShowOnboarding = true;

  // Redirect to home if user should skip onboarding
  useEffect(() => {
    if (isLoggedIn && !shouldShowOnboarding) {
      router.replace("/home/tabs/home");
    }
  }, [isLoggedIn, shouldShowOnboarding]);

  const isLastSlide = activeIndex === onboarding.length - 1;

  /*
    Handle next button press
    Redirect to home if on last slide
  */
  const handleNext = () => {
    if (isLastSlide) {
      router.replace("/home/tabs/home");
    } else {
      swiperRef.current?.scrollBy(1);
    }
  };

  /*
    Render pagination dots
  */
  const renderPagination = () => {
    return (
      <View className="flex flex-row justify-center my-5">
        {onboarding.map((_, index) => (
          <TouchableOpacity 
            key={index}
            onPress={() => swiperRef.current?.scrollTo(index)}
            className="mx-1"
          >
            <View 
              className={`w-[32px] h-[4px] rounded-full ${
                activeIndex === index ? "bg-blue-500" : "bg-gray-200"
              }`}
            />
          </TouchableOpacity>
        ))}
      </View>
    );
  };

  return (
    <ThemedSafeAreaView className="flex-1 items-center justify-between">
      {/* Header with Skip Button */}
      <View className="w-full flex-row justify-end px-5">
        <TouchableOpacity
          onPress={() => router.replace("/home/tabs/home")}
          className={`px-4 py-2 rounded-full ${isDarkMode ? "bg-slate-700" : "bg-gray-50"}`}
        >
          <Text className={`text-base font-JakartaBold ${isDarkMode ? "text-white" : "text-gray-600"}`}>Skip</Text>
        </TouchableOpacity>
      </View>
       
      {/* Swiper with proper height constraints */}
      <View className="flex-1 w-full" style={{ maxHeight: height * 0.6 }}>
        <Swiper
          ref={swiperRef}
          loop={false}
          showsPagination={false}
          onIndexChanged={(index) => setActiveIndex(index)}
        >
          {onboarding.map((item) => (
            <View key={item.id} className="flex-1 items-center justify-center px-6">
              <Animated.View 
                style={{ 
                  width: '100%',
                  alignItems: 'center' 
                }}
              >
                <Image
                  source={item.image}
                  style={{ width: '85%', height: 280 }}
                  resizeMode="contain"
                />
                
                <View className="mt-8 items-center">
                  <Text className={`text-3xl font-JakartaBold text-center ${isDarkMode ? "text-white" : "text-black"}`}>
                    {item.title}
                  </Text>
                  <Text className={`text-base font-JakartaMedium text-center mt-3 max-w-[100%] ${isDarkMode ? "text-gray-300" : "text-gray-500"}`}>
                    {item.description}
                  </Text>
                </View>
              </Animated.View>
            </View>
          ))}
        </Swiper>
      </View>
      
      {/* Footer */}
      <View className="w-full items-center pt-6 pb-8" style={{ marginTop: 'auto' }}>
        {renderPagination()}
        
        <Button
          title={isLastSlide ? "Get Started" : "Next"}
          onPress={handleNext}
          className="text-lg font-JakartaBold"
        />
      </View>
    </ThemedSafeAreaView>
  );
};

export default OnBoarding;