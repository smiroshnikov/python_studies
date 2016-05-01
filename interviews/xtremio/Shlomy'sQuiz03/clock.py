def test():
    pass


"""
For this week python quiz:


Analog clocks display time with an analog clock face, which consists of a round dial with the numbers 1 through 12, the hours in the day, around the outside.
The hours are indicated with an hour hand, which makes two revolutions in a day, while the minutes are indicated by a minute hand, which makes one revolution per hour.
In this quiz we will use a clock without second hand. The hour hand moves smoothly and the minute hand moves step by step.
You are given a time in 24-hour format and you should calculate a lesser angle between the hour and minute hands in degrees.
Don't forget that clock has numbers from 1 to 12, so 23 == 11.
The time is given as a string with the follow format "HH:MM", where HH is hours and MM is minutes.
Hours and minutes are given in two digits format, so "1" will be written as "01". The result should be given in degrees with precision ±0.1.



Input: A time as a string.

Output: The lesser angle as an integer or a float.

Example:
clock_angle("02:30") == 105
clock_angle("13:42") == 159
clock_angle("01:43") == 153.5,
clock_angle("00:00") == 0,
clock_angle("12:01") == 5.5,
clock_angle("18:00") == 180
"""
