from datetime import datetime, date, time, timedelta

# todo проверять чтобы время сна было меньше времени проведенного в кровати


def sleep_duration_less_time_in_bed():
    pass



def sleep_time_check(sleep_date, bedtime, asleep):
    """Проверка корректности времени отхода ко сну и времени засыпания относительно друг друга.
    Возвращает время в кровати засыпания, если время засыпания больше времени отхода ко сну, а также
    если время засыпания меньше времени отхода ко сну, но не более чем на 12 часов,
    иначе возбуждает ошибку значения.
    Если две точки времени находятся в рамках одного часа и количество минут во времени засыпания больше
    количества минут во времени отхода ко сну, то возбуждается ошибка значения.
    """
    if bedtime > asleep:
        datetime_bedtime = datetime.combine(sleep_date, bedtime)
        datetime_asleep = datetime.combine(date(sleep_date.year, sleep_date.month, sleep_date.day + 1), asleep)
        if bedtime.hour == asleep.hour and bedtime.minute > asleep.minute:
            """Вызывает ошибку если уснул раньше чем лег в рамках часа"""
            raise ValueError("Не можешь в рамках часа уснуть раньше чем лег!")
        elif datetime_asleep - datetime_bedtime > timedelta(hours=12):
            """Вызывает ошибку если разница между отходом ко сну и засыпанием больше 12 часов"""
            raise ValueError("Время отхода ко сну не может быть позже времени засыпания!\n"
                             "Или разница между временем засыпания и временем отхода ко сну не может быть "
                             "более 12 часов!")
        return datetime_asleep - datetime_bedtime
    else:
        return datetime.combine(sleep_date, asleep) - datetime.combine(sleep_date, bedtime)


def wake_up_time_check(sleep_date, awake, rise):
    """Проверка корректности времени пробуждения и времени подъема с кровати относительно друг друга.
    Возвращает время в кровати после сна, если время пробуждения меньше времени подъема, а также
    если время пробуждения больше чем время подъема, но не больше чем на 12 часов,
    иначе возбуждает ошибку значения.
    Если две точки времени находятся в рамках одного часа и количество минут во времени пробуждения больше
    количества минут во времени подъема, то возбуждается ошибка значения.
    """
    if awake > rise:
        datetime_awake = datetime.combine(sleep_date, awake)
        datetime_rise = datetime.combine(date(sleep_date.year, sleep_date.month, sleep_date.day + 1), rise)
        if awake.hour == rise.hour and awake.minute > rise.minute:
            """"""
            raise ValueError("Не можешь в рамках часа уснуть раньше чем лег!")
        elif datetime_rise - datetime_awake > timedelta(hours=12):
            """"""
            raise ValueError("Время отхода ко сну не может быть позже времени засыпания!\n"
                             "Или разница между временем засыпания и временем отхода ко сну не может быть "
                             "более 12 часов!")
        return datetime_rise - datetime_awake
    else:
        return datetime.combine(sleep_date, rise) - datetime.combine(sleep_date, awake)


sleeeeep = date(2022, 1, 5)
print('1 бывает')
awake = time(hour=23, minute=55)
rise = time(hour=0, minute=5)
print(wake_up_time_check(sleeeeep, awake, rise))

try:
    print('\n2 ошибка должна быть')
    awake = time(hour=3, minute=50)
    rise = time(hour=4, minute=30)
    print(wake_up_time_check(sleeeeep, awake, rise), '\n')
except ValueError as err:
    print(err.args[0], '\n')

print('3 бывает')
awake = time(hour=5, minute=50)
rise = time(hour=6, minute=5)
print(wake_up_time_check(sleeeeep, awake, rise))
