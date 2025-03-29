import { View, Text, ScrollView } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { useTheme } from '@/context/ThemeContext';
import { useRevenueChart } from '@/hooks/useRevenueChart';

interface WeeklyRevenue {
  week: number;
  total_income: number;
}

interface RevenueChartProps {
  weeklyData: WeeklyRevenue[];
  title?: string;
}
/*
    RevenueChart
    A component that displays a line chart of weekly revenue data
*/
const RevenueChart = ({ weeklyData, title = "Weekly Revenue" }: RevenueChartProps) => {
  const { isDarkMode } = useTheme();
  const { 
    hasData, 
    labels, 
    data, 
    totalRevenue, 
    averageRevenue, 
    chartWidth 
  } = useRevenueChart(weeklyData);
  
  // If no data, show placeholder
  if (!hasData) {
    return (
      <View className={`p-4 rounded-lg ${isDarkMode ? 'bg-slate-800' : 'bg-white'} shadow mb-5`}>
        <Text className={`font-JakartaBold text-lg mb-2 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
          {title}
        </Text>
        <Text className={`${isDarkMode ? 'text-gray-400' : 'text-gray-500'} text-center py-6`}>
          No revenue data available yet
        </Text>
      </View>
    );
  }

  const chartConfig = {
    backgroundGradientFrom: isDarkMode ? '#1e293b' : '#ffffff',
    backgroundGradientTo: isDarkMode ? '#1e293b' : '#ffffff',
    decimalPlaces: 2,
    color: () => isDarkMode ? '#3b82f6' : '#2563eb',
    labelColor: () => isDarkMode ? '#cbd5e1' : '#64748b',
    style: {
      borderRadius: 16,
    },
    propsForDots: {
      r: '6',
      strokeWidth: '2',
      stroke: isDarkMode ? '#2563eb' : '#3b82f6',
    },
    propsForBackgroundLines: {
      stroke: isDarkMode ? '#334155' : '#e2e8f0',
    },
  };

  return (
    <View className={`p-4 rounded-lg ${isDarkMode ? 'bg-slate-800' : 'bg-white'} shadow mb-5`}>
      <Text className={`font-JakartaBold text-lg mb-2 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
        {title}
      </Text>
      
      {/* Revenue Summary */}
      <View className="flex-row justify-between mb-4">
        <View className="items-center flex-1">
          <Text className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            Total Revenue
          </Text>
          <Text className={`text-lg font-JakartaBold ${isDarkMode ? 'text-green-400' : 'text-green-600'}`}>
            £{totalRevenue}
          </Text>
        </View>
        <View className="items-center flex-1">
          <Text className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            Average Weekly
          </Text>
          <Text className={`text-lg font-JakartaBold ${isDarkMode ? 'text-blue-400' : 'text-blue-600'}`}>
            £{averageRevenue}
          </Text>
        </View>
      </View>
      
      {/* Chart in ScrollView for wider datasets */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        <LineChart
          data={{
            labels,
            datasets: [
              {
                data,
                color: () => isDarkMode ? '#3b82f6' : '#2563eb',
                strokeWidth: 2,
              }
            ],
          }}
          width={chartWidth}
          height={220}
          chartConfig={chartConfig}
          bezier
          style={{
            marginVertical: 8,
            borderRadius: 16,
          }}
          formatYLabel={(value) => `£${value}`}
        />
      </ScrollView>
    </View>
  );
};

export default RevenueChart;
