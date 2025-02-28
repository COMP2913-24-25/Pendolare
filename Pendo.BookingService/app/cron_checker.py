from cronex import CronExpression

def checkTimeValid(cron, time):
    """
    checkTimeValid method checks if the specified time is valid for the specified cron expression.
    :param cron: Cron expression.
    :param time: Time to be checked.
    :return: True if the time is valid, False otherwise.
    """
    try:
        cron = CronExpression(cron)
        return cron.check_trigger(time)
    except Exception as e:
        return str(e)