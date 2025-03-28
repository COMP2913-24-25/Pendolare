from cronex import CronExpression
from croniter import croniter
from datetime import datetime

def checkTimeValid(cron, time):
    """
    checkTimeValid method checks if the specified time is valid for the specified cron expression.
    :param cron: Cron expression.
    :param time: Time to be checked.
    :return: True if the time is valid, False otherwise.
    """
    try:
        cron = CronExpression(cron)
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        time_tuple = (time.year, time.month, time.day, time.hour, time.minute)
        return cron.check_trigger(time_tuple)
    except Exception as e:
        return str(e)

def toHumanReadable(cron: str) -> str:
    """
    toHumanReadable method converts a cron expression to a human-readable schedule.
    :param cron: Cron expression.
    :returns Human-readable schedule.
    """

    day_map = {
        "0": "Sunday",
        "1": "Monday",
        "2": "Tuesday",
        "3": "Wednesday",
        "4": "Thursday",
        "5": "Friday",
        "6": "Saturday",
    }
    
    try:
        parts = cron.split(" ")
        if "/" in parts[0]:
            minutes = parts[0].split("/")[1]
            return f"Every {minutes} minutes"

        base = datetime.now()
        itr = croniter(cron, base)
        next_date = itr.get_next(datetime)
        time_str = next_date.strftime("%I:%M %p").lstrip("0")
        
        days = ""
        if parts[4] != "*":
            day_list = [day_map.get(d.strip(), "") for d in parts[4].split(",")]
            days = ", ".join(filter(None, day_list))
        
        frequency = "Weekly"
        if parts[2] != "*":
            frequency = "Monthly"
        elif parts[4] != "*":
            if "," in parts[4]:
                frequency = "Weekly"
            else:
                frequency = "Fortnightly"
        
        day_part = f"on {days}" if days else "every day"
        return f"{frequency}, {day_part} at {time_str}"
    
    except Exception:
        return "Invalid schedule"
    
def getNextTimes(cron : str, startTime : datetime, endTime : datetime, max : datetime) -> list[datetime]:
    """
    getNextTimes method returns the next max times that satisfy the cron expression between the specified start and end times.
    :param cron: Cron expression.
    :param startTime: Start time.
    :param endTime: End time.
    :param max: Maximum number of times to return.
    :return: List of times.
    """
    try:
        startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        endTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")

        iter = croniter(cron, startTime)
        numTimes = 0
        times = []
        nextTime = iter.get_next(datetime)

        while nextTime <= endTime and numTimes < max:
            times.append(nextTime)
            numTimes += 1
            nextTime = iter.get_next(datetime)

        return times
    except Exception as e:
        return str(e)
