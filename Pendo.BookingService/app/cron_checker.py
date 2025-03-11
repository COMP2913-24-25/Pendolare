from cronex import CronExpression
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