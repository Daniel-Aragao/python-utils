import re

pattern = r'(\d+):(\d+):(\d+)'


class Hour:
    def __init__(self, h, m, s, is_negative=False, hour_type=24, hour_12_turn='AM'):
        self.hour = h
        self.minute = m
        self.second = s
        self.is_negative = is_negative
        self.type = hour_type
        self.hour_12_turn = hour_12_turn

    def diference(self, hour2):
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
        hour = Hour(24, 0, 0)

        clone = self.clone()
        if self.type != 24:
            clone.convert_to_24()

        hour = hour.diference(clone)

        if self.type != 24:
            hour = hour.convert_to_12()

        hour.is_negative = not hour.is_negative

        return hour

    def convert_to_24(self):
        if self.type == 24:
            return self.clone()

        hour = self.clone()
        hour.type = 24
        if hour.hour_12_turn == 'PM':
            if hour.hour < 12:
                hour.hour += 12

        return hour

    def convert_to_12(self):
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
        string = '{0:02}:{1:02}:{2:02}'.format(self.hour, self.minute, self.second)
        if self.is_negative:
            string = '-' + string
        elif self.type == 12:
            string = string + ' ' + self.hour_12_turn

        return string

    def clone(self):
        return Hour(self.hour, self.minute, self.second,
                    self.is_negative, self.type, self.hour_12_turn)


def diference(hour1, hour2):
    first = re.match(pattern, hour1)
    second = re.match(pattern, hour2)

    hora1 = Hour(int(first.group(1)), int(first.group(2)), int(first.group(3)))
    hora2 = Hour(int(second.group(1)), int(second.group(2)), int(second.group(3)))

    return str(hora1.diference(hora2))
