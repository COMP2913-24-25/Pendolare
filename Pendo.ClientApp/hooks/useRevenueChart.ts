import { useMemo } from 'react';
import { Dimensions } from 'react-native';

interface WeeklyRevenue {
  week: number;
  total_income: number;
}

/**
 * Custom hook to handle chart data processing for revenue charts
 */
export const useRevenueChart = (weeklyData: WeeklyRevenue[]) => {
  return useMemo(() => {
    // Get screen width and account for margins
    const screenWidth = Dimensions.get('window').width - 40;
    
    // If no data, return empty state
    if (!weeklyData || weeklyData.length === 0) {
      return {
        hasData: false,
        screenWidth,
        labels: [],
        data: [],
        totalRevenue: "0.00",
        averageRevenue: "0.00"
      };
    }

    // Process data for chart
    const labels = weeklyData.map(item => `Week ${item.week}`);
    const data = weeklyData.map(item => parseFloat(item.total_income.toFixed(2)));
    
    // Calculate average revenue
    const averageRevenue = data.length > 0 
      ? (data.reduce((sum, val) => sum + val, 0) / data.length).toFixed(2)
      : "0.00";
    
    // Calculate total revenue
    const totalRevenue = data.reduce((sum, val) => sum + val, 0).toFixed(2);
    
    return {
      hasData: true,
      screenWidth,
      labels,
      data,
      totalRevenue,
      averageRevenue,
      chartWidth: Math.max(screenWidth, labels.length * 70)
    };
  }, [weeklyData]);
};
