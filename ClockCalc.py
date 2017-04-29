import re

pattern = r'(\d+):(\d+):(\d+)'


class Hour:
    """
    A hour representation
    """
    def __init__(self, h, m, s, is_negative=False, hour_type=24, hour_12_turn='AM'):
        """
        Declare a Hour type
        :param h: int Hours value
        :param m: int Minutes value
        :param s: int Seconds value
        :param is_negative: bool True for negative times and False for positive (defualt)
        :param hour_type: int 12 to 12's clock and 24 for 24's clock (default) 
        :param hour_12_turn: string 'AM'(defualt) and 'PM' in case of 12's clock 
        """
        self.hour = h
        self.minute = m
        self.second = s
        self.is_negative = is_negative
        self.type = hour_type
        self.hour_12_turn = hour_12_turn

    def diference(self, hour2):
        """
        Subtract this object time for the hour2 inserted 
        as parameter and return another Hour object
        :param hour2: ClockCalc.Hour 
        :return: ClockCalc.Hour 
        """
        hour = self.clone()

        if hour.type != 24:
            hour = hour.convert_to_24()

        hour.second -= hour2.second
        hour.minute -= hour2.minute
        hour.hour -= hour2.hour

        while hour.second < 0:
            if hour.minute > 0:
                hour.second += 60
                hour.minute -= 1
            else:
                if hour.hour > 0:
                    hour.second += 60
                    hour.minute -= 1
                    hour.minute += 60
                    hour.hour -= 1
                else:
                    hour.second *= -1
                    hour.is_negative = True
                    break

        while hour.minute < 0:
            if hour.hour > 0:
                hour.minute += 60
                hour.hour -= 1
            else:
                hour.minute *= -1
                hour.is_negative = True
                break

        if hour.hour < 0:
            hour.hour *= -1
            hour.is_negative = True

        if hour.type != 24:
            hour = hour.convert_to_12()

        return hour

    def inverse(self):
        """
        when the hour is negative => convert to positive hour
            Ex.1: -00:01:30 => 11:58:30 PM
            Ex.2: -00:01:30 => 23:58:30
        :return: ClockCalc.Hour 
        """
        hour = Hour(24, 0, 0)

        clone = self.clone()
        if self.type != 24:
            clone.convert_to_24()

        hour = hour.diference(clone)

        if self.type != 24:
            hour = hour.convert_to_12()

        hour.is_negative = not self.is_negative

        return hour

    def convert_to_24(self):
        """
        Convert this hour object in another one, changing
        the time type to 24
        :return: ClockCalc.Hour 
        """
        if self.type == 24:
            return self.clone()

        hour = self.clone()
        hour.type = 24
        if hour.hour_12_turn == 'PM':
            if hour.hour < 12:
                hour.hour += 12

        return hour

    def convert_to_12(self):
        """
        Convert this hour object in another one, changing
        the time type to 12
        :return: ClockCalc.Hour 
        """
        if self.type == 12:
            return self.clone()

        hour = self.clone()

        hour.type = 12
        if hour.hour > 12:
            hour.hour_12_turn = 'PM'
            hour.hour -= 12
        elif hour.hour == 12:
            hour.hour_12_turn = 'PM'
        else:
            hour.hour_12_turn = 'AM'

        return hour

    def __str__(self):
        """
        Formated string 
            Ex.1: '11:58:30 PM'
            Ex.2: '18:15:47'
        OBS.: negative numbers don't have the turn indication on 12's clock, but still
        obeying the policy of 12's clock and will show again in case it becames positive
        again
        :return: string
        """
        string = '{0:02}:{1:02}:{2:02}'.format(self.hour, self.minute, self.second)
        if self.is_negative:
            string = '-' + string
        elif self.type == 12:
            string = string + ' ' + self.hour_12_turn

        return string

    def clone(self):
        """
        Clone this object in a new one with the same values
        for the self.properties
        :return: ClockCalc.Hour 
        """
        return Hour(self.hour, self.minute, self.second,
                    self.is_negative, self.type, self.hour_12_turn)


def diference(hour1, hour2):
    """
    Receive two hours patterns and return the diference
    obs.: For this work will be necessary to obey the 
    24's clock rules
    :param hour1: Ex.: '18:15:47'
    :param hour2: '17:14:46'
    :return: string
    """
    first = re.match(pattern, hour1)
    second = re.match(pattern, hour2)

    hora1 = Hour(int(first.group(1)), int(first.group(2)), int(first.group(3)))
    hora2 = Hour(int(second.group(1)), int(second.group(2)), int(second.group(3)))

    return str(hora1.diference(hora2))
