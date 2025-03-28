import { useState, useEffect } from 'react';
import { generateCronExpression, parseCronExpression } from '@/utils/cronTools';

export type FrequencyType = 'weekly' | 'fortnightly' | 'monthly';

export interface UseCommuterScheduleProps {
  initialCronExpression?: string;
  initialEndDate?: Date | string;
}

export const useCommuterSchedule = ({ 
  initialCronExpression, 
  initialEndDate 
}: UseCommuterScheduleProps = {}) => {
  // Default end date is 30 days from now
  const defaultEndDate = new Date();
  defaultEndDate.setDate(defaultEndDate.getDate() + 30);
  
  // Start time defaults to 9:00 AM today
  const defaultStartTime = new Date();
  defaultStartTime.setHours(9, 0, 0, 0);
  
  const [frequency, setFrequency] = useState<FrequencyType>('weekly');
  const [startTime, setStartTime] = useState<Date>(defaultStartTime);
  const [endDate, setEndDate] = useState<Date>(
    initialEndDate instanceof Date ? initialEndDate :
    typeof initialEndDate === 'string' ? new Date(initialEndDate) :
    defaultEndDate
  );
  
  const [selectedDays, setSelectedDays] = useState<{[key: string]: boolean}>({
    '0': false, // Sunday
    '1': false, // Monday
    '2': false, // Tuesday
    '3': false, // Wednesday
    '4': false, // Thursday
    '5': false, // Friday
    '6': false  // Saturday
  });
  
  // Parse initial cron expression if provided
  useEffect(() => {
    if (initialCronExpression) {
      try {
        const result = parseCronExpression(initialCronExpression);
        
        // Update state based on parsed cron
        setStartTime(result.startTime);
        setFrequency(result.frequency);
        
        // Update selected days
        const newSelectedDays = { ...selectedDays };
        result.days.forEach(day => {
          newSelectedDays[day] = true;
        });
        setSelectedDays(newSelectedDays);
      } catch (error) {
        console.error("Error parsing cron expression:", error);
      }
    }
  }, [initialCronExpression]);
  
  // Toggle a weekday selection
  const toggleDay = (day: string) => {
    const newSelectedDays = { ...selectedDays };
    newSelectedDays[day] = !newSelectedDays[day];
    setSelectedDays(newSelectedDays);
  };
  
  // Get selected days as array
  const getSelectedDaysArray = () => {
    return Object.keys(selectedDays).filter(key => selectedDays[key]);
  };
  
  // Generate cron expression from current settings
  const getCronExpression = () => {
    const daysList = getSelectedDaysArray();
    
    // Ensure at least one day is selected for weekly frequency
    if (frequency === 'weekly' && daysList.length === 0) {
      // Default to the current day if none selected
      const currentDay = new Date().getDay().toString();
      daysList.push(currentDay);
    }
    
    return generateCronExpression(frequency, daysList, startTime);
  };
  
  return {
    frequency,
    setFrequency,
    startTime,
    setStartTime,
    endDate,
    setEndDate,
    selectedDays,
    toggleDay,
    getSelectedDaysArray,
    getCronExpression
  };
};
