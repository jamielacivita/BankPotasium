from typing import List, Set, Tuple
from collections import namedtuple
from prettytable import PrettyTable
import math

Measurement = namedtuple('Measurement', ['date', 'sys', 'dia'])

class BPLog:
    def __init__(self):
        # self.measurements is the full list of measurements taken.
        self.measurements: List[Measurement] = []
        # self.measurements_daily_avg is a average of any set of measurements taken for a paticular day.
        self.measurements_daily_avg = []
        # self.measurements_sevenday_avg is the seven day rolling average measurement set.
        self.measurements_sevenday_avg = []

    def add_measurement(self, m: Measurement):
        if m.date != "Date":
            self.measurements.append(m)

    def print_number_measurements(self):
        print(len(self.measurements))

    def print_daily_average(self):
        mytable = PrettyTable(["Date", "SYS", "DIA"])
        for row in self.measurements_daily_avg:
            mytable.add_row(row)
        print(mytable)

    def set_measurements_daily_avg(self):
        self.measurements_daily_avg = []
        unique_dates = self._get_unique_dates()

        # iterate over the dates and for each date get the list of measurements
        for date in unique_dates:
            daily_measurements = self._get_daily_measurements(date)

            avg_sys, avg_dia = self._calc_averages(daily_measurements)

            # append to measurements_daily_avg
            self.measurements_daily_avg.append([date, avg_sys, avg_dia])

    def set_measurements_sevenday_avg(self):
        # interate over the daily average
        first_index = 0
        last_index = len(self.measurements_daily_avg)
        # print(f"first index : {first_index}")
        # print(f"last index : {last_index}")

        for start in range(first_index, last_index-6):
            # print(f"start : {start}")
            # print(f"emd : {start + 7}")

            res = []
            res.extend(self.measurements_daily_avg[start:start+7])
            # print(res)

            sum_sys = 0
            sum_dia = 0
            for m in res:
                sum_sys = sum_sys + m[1]
                sum_dia = sum_dia + m[2]

            avg_sys = math.trunc(sum_sys / 7)
            avg_dia = math.trunc(sum_dia / 7)
            date = res[-1][0]

            self.measurements_sevenday_avg.append([date, avg_sys, avg_dia])

    def print_measurements_sevenday_avg(self):
        mytable = PrettyTable(["Date", "SYS", "DIA"])
        for row in self.measurements_sevenday_avg:
            mytable.add_row(row)
        print("Seven Day Rolling Average")
        print(mytable)

    def _get_unique_dates(self) -> List[str]:
        """ get the unique list of dates
        """
        dates = []
        for m in self.measurements:
            if m.date not in dates:
                dates.append(m.date)
        return dates

    def _get_daily_measurements(self, date):
        daily_measurements = []
        for m in self.measurements:
            if m.date == date:
                daily_measurements.append(m)
        return daily_measurements

    def _calc_averages(self, daily_measurements: List[Measurement]) -> Tuple[int, int]:
        """
        calculate the average sys and dia from the list of measurements
        """
        sum_sys = 0
        sum_dia = 0
        for m in daily_measurements:
            sum_sys += int(m.sys)
            sum_dia += int(m.dia)
        avg_sys = sum_sys // len(daily_measurements)
        avg_dia = sum_dia // len(daily_measurements)
        return avg_sys, avg_dia