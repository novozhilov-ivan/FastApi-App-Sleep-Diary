# from .views import *
#
#
# # Todo переименовать параметр
# def str_to_time(s):
#     return datetime.time(datetime.strptime(s, '%H:%M'))
#
#
# # Todo переименовать параметр
# def str_to_ymd(s):
#     return datetime.date(datetime.strptime(s, '%Y-%m-%d'))
#
#
# # Todo переименовать параметр
# def timedelta_to_minutes(s):
#     return s.seconds / 60
#
#
# # Todo переименовать функцию
# def eff(spal, vkrovati):
#     if spal == 0:
#         return 0
#     return round((spal / vkrovati * 100), 2)
#
#
# # todo rename
# def h_m(vremya: int or datetime):
#     if type(vremya) == int:
#         if vremya % 60 < 10:
#             # todo rename var
#             hm = str(vremya // 60) + ':0' + str(vremya % 60)
#         else:
#             hm = str(vremya // 60) + ':' + str(vremya % 60)
#     elif type(vremya) == datetime:
#         hm = vremya.strftime('%H:%M')
#     else:
#         # raise
#         hm = 'TypeError'
#     return hm
#
# # # todo rename
# # def h_m(vremya: int or datetime):
# #     if isinstance(vremya, int):
# #         if vremya % 60 < 10:
# #             # todo rename var
# #             hm = str(vremya // 60) + ':0' + str(vremya % 60)
# #         else:
# #             hm = str(vremya // 60) + ':' + str(vremya % 60)
# #     elif isinstance(vremya, datetime):
# #         hm = vremya.strftime('%H:%M')
# #     else:
# #         raise TypeError
# #
# #     return hm
#
#
# def get_timedelta(date1, date2, vremya1, vremya2):
#     return datetime.combine(date1, vremya1) - datetime.combine(date2, vremya2)
#
#
# # todo переименовать.
# def date_dmy_to_ymd(s):
#     return s[0][6:] + '-' + s[0][3:5] + '-' + s[0][0:2]
#
#
# # todo raname "eff"
# # todo добавить докстрингу
# # todo переименовать пераметр
# # todo Поправить логику связанную с тем, что используется id. Если 1 день не созхдать notation,
# #  то все соотношения сдвинутся
#
#
# def eff_sleep_of_week(nedelya):
#     """Вычисляет среднюю эффективность сна за неделю"""
#     sum_eff, elem_of_week = 0, 0
#     # todo строка ниже является совсем не очевидной
#     for day in range(1 + 7 * (nedelya - 1), 8 * nedelya - (nedelya - 1)):
#         # todo мб вместо elem иользовать еременную notation
#         for elem in notation:
#             # todo почему elem.id, а не elem.data???
#             if elem.id != day:
#                 continue
#             elem_of_week += 1
#             if elem.spal != 0:
#                 sum_eff += elem.spal / elem.vkrovati
#
#     if elem_of_week == 0:
#         return 0
#     else:
#         return round(((sum_eff / elem_of_week) * 100), 2)
#
#
# def avg_duration_sleep_of_week(nedelya):
#     sum_min, elem_of_week = 0, 0
#
#     for day in range(1 + 7 * (nedelya - 1), 8 * nedelya - (nedelya - 1)):
#         for elem in notations:
#             if elem.id == day:
#                 elem_of_week += 1
#                 sum_min += elem.spal
#     if elem_of_week == 0:
#         return 0
#     else:
#         return int(sum_min / elem_of_week)
#
#
# def check_notations(nedelya):
#     amount = 0
#     for day in range(1 + 7 * (nedelya - 1), 8 * nedelya - (nedelya - 1)):
#         for elem in notations:
#             if elem.id == day:
#                 amount += 1
#     if amount == 0:
#         return 0
#     else:
#         return amount
#
# # def last_day(day_number):
# #     day = 0
# #     for elem in notations:
# #         day += 1
# #     if day_number == day:
# #         return True
# #     else:
# #         return False
#
#
# def last_day(day_number: int):
#     if day_number == db_elem_counter:
#         return True
#     return False
#
#
# # todo функиця наверное не нужна
# def dmy_today():
#     return datetime.date(datetime.today())
