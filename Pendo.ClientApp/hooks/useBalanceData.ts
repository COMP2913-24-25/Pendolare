import { useState, useEffect } from 'react';
import { ViewBalance, BalanceSheet } from '@/services/paymentService';

interface WeeklyRevenue {
  week: number;
  total_income: number;
}
/*
    Custom hook to fetch and manage balance data
*/
export const useBalanceData = () => {
  const [balanceData, setBalanceData] = useState<BalanceSheet | null>(null);
  const [weeklyRevenue, setWeeklyRevenue] = useState<WeeklyRevenue[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchBalanceData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const data = await ViewBalance();
      console.log("Balance data received:", data);
      
      setBalanceData(data);
      
      // Process weekly revenue data if available
      if (data && data.Weekly && Array.isArray(data.Weekly)) {
        // Sort by week number
        const sortedWeekly = [...data.Weekly].sort((a, b) => a.week - b.week);
        setWeeklyRevenue(sortedWeekly);
      } else {
        setWeeklyRevenue([]);
      }
    } catch (err) {
      console.error("Error fetching balance data:", err);
      setError("Failed to load balance data");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBalanceData();
  }, []);

  return {
    balanceData,
    weeklyRevenue,
    isLoading,
    error,
    refresh: fetchBalanceData
  };
};
