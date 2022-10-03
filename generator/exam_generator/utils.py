import time


def int_to_roman(num: int):
    """
    Solution from https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-1.php
    :param num: integer number to be converted
    :return: converter number in Roman system
    """
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ""
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num


def random_date(start, end, prop):
    """
    Solution from https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    """
    def str_time_prop(_start, _end, time_format, _prop):
        """Get a time at a proportion of a range of two formatted times.

        start and end should be strings specifying times formatted in the
        given format (strftime-style), giving an interval [start, end].
        prop specifies how a proportion of the interval to be taken after
        start.  The returned time will be in the specified format.
        """

        stime = time.mktime(time.strptime(_start, time_format))
        etime = time.mktime(time.strptime(_end, time_format))
        ptime = stime + _prop * (etime - stime)
        return time.strftime(time_format, time.localtime(ptime))

    return str_time_prop(start, end, '%d.%m.%Y', prop)
