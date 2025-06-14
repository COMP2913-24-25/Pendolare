import cronParser from "cron-parser";

/**
 * Converts a CRON expression to a human‐readable string.
 * 
 * @param cron the CRON expression to parse.
 * @returns a human‐readable string representing the CRON expression.
 */
export function toHumanReadable(cron: string) {
  const dayMap: { [key: string]: string } = {
    "0": "Sunday",
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday",
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
  };

  try {
    const parts = cron.split(" ");
    if (parts[0].includes("/")) {
      const minutes = parts[0].split("/")[1];
      return `Every ${minutes} minutes`;
    }

    const interval = cronParser.parse(cron, {});
    const nextDate = interval.next().toDate();
    const time = nextDate.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    const days = parts[4] !== "*" ? parts[4].split(",").map((d) => dayMap[d.trim()] || "").join(", ") : "";

    let frequency = "Weekly";
    if (parts[2] !== "*") frequency = "Monthly";
    else if (parts[4] !== "*" && parts[4].includes(",")) frequency = "Weekly";
    else if (parts[4] !== "*" && parts[4].match(/(0|1|2|3|4|5|6)/)) frequency = "Fortnightly";

    return `${frequency}, ${days ? `on ${days}` : "every day"} at ${time}`;
  } catch (error) {
    return "Invalid schedule";
  }
}

/**
 * Converts a frequency and optional weekdays to a CRON expression.
 * 
 * @param frequency - The frequency of execution ("Weekly", "Fortnightly", or "Monthly")
 * @param days - Array of weekdays (0-6, where 0 is Sunday) to run the task on
 * @param time - Date object containing the time (hours and minutes) to run the task
 * @returns A valid CRON expression string for the specified schedule
 */
export function toCronString(
    frequency: "weekly" | "fortnightly" | "monthly",
    days: string[] = [],
    time: Date
  ): string {

    const minutes = time.getMinutes();
    const hours = time.getHours();
    
    const daysList = days.length > 0 ? days : [time.getDay().toString()];
    let cronDays = daysList.join(",");
  
    if (frequency === "monthly") {
      return `${minutes} ${hours} ${time.getDate()} * *`;
    } 
    
    if (frequency === "fortnightly") {
      return `${minutes} ${hours} */14 * *`;
    }
  
    return `${minutes} ${hours} * * ${cronDays}`;
}

/**
 * Gets the next occurrence dates for a cron expression with limiting parameters.
 * 
 * @param cronExpression - The cron expression to parse
 * @param startDate - The date to start calculating from (defaults to current date)
 * @param maxDate - The maximum date cutoff (won't return dates after this)
 * @param maxDates - The maximum number of dates to return
 * @returns An array of dates representing the next occurrences
 */
export function getNextCronDates(
    cronExpression: string,
    startDate: Date = new Date(),
    maxDate?: Date,
    maxDates: number = 10
  ): Date[] {
    try{
      const results: Date[] = [];
      const interval = cronParser.parse(cronExpression, { currentDate: startDate, endDate: maxDate });
      
      if (!interval.hasNext()) {
        console.log("No next dates available for the given CRON expression.");
        return results;
      }

      let nextDate = interval.next().toDate();
      let counter = 0;
      
      while (counter < maxDates) {
        results.push(new Date(nextDate));
        counter++;
        
        if (!interval.hasNext()) {
          break;
        }

        nextDate = interval.next().toDate();
      }
      return results;
    }
    catch(error){
      console.log("Error parsing CRON expression: ", error);
      throw error;
    }
}

/**
 * Parse a cron expression into its component parts
 */
export const parseCronExpression = (cronExpression: string) => {
  const parts = cronExpression.split(' ');
  
  // Parse minutes and hours for time
  const minutes = parseInt(parts[0]);
  const hours = parseInt(parts[1]);
  const startTime = new Date();
  startTime.setHours(hours, minutes, 0, 0);
  
  // Determine frequency
  let frequency: 'weekly' | 'fortnightly' | 'monthly' = 'weekly';
  if (parts[2].includes('*/14')) {
    frequency = 'fortnightly';
  } else if (parts[2] !== '*') {
    frequency = 'monthly';
  }
  
  // Parse days of week
  let days: string[] = [];
  if (parts[4] !== '*') {
    days = parts[4].split(',');
  }
  
  return {
    startTime,
    frequency,
    days
  };
};

/**
 * Generates a CRON expression from frequency, days and time.
 * 
 * @param frequency - The frequency ("weekly", "fortnightly", or "monthly")
 * @param days - Array of weekdays (as strings) on which to run the task.
 * @param time - The time at which the task should run.
 * @returns A valid CRON expression.
 */
export const generateCronExpression = (
  frequency: 'weekly' | 'fortnightly' | 'monthly',
  days: string[],
  time: Date
) => {
  const minutes = time.getMinutes();
  const hours = time.getHours();
  
  let dayOfMonth = '*';
  let dayOfWeek = '*';
  
  // Set day of month or week based on frequency
  if (frequency === 'monthly') {
    dayOfMonth = (new Date().getDate()).toString();
  } else {
    // For weekly/fortnightly, use days of the week
    if (days.length > 0) {
      dayOfWeek = days.join(',');
    }
  }
  
  // Adjust month field for fortnightly
  const monthField = frequency === 'fortnightly' ? '*/14' : '*';
  
  return `${minutes} ${hours} ${dayOfMonth} * ${dayOfWeek}`;
};