from typing import List, Tuple
from collections import namedtuple
from pathlib import Path
from prettytable import PrettyTable
import csv
import logging

log = logging.getLogger(__name__)

Datapoint = namedtuple('Datapoint', ['date', 'sys', 'dia'])


class BPLog:
    def __init__(self):

        # the full list of measurements taken
        self.measurements: List[Datapoint] = []

        # an average of any set of measurements taken on a particular day
        self.daily_avg: List[Datapoint] = []

        # the seven day rolling average measurement set
        self.seven_day_avg: List[Datapoint] = []

    def add_measurement(self, m: Datapoint):
        if m.date != "Date":
            self.measurements.append(m)

    def calc_daily_avg(self):
        self.daily_avg = []
        unique_dates = self._get_unique_dates()

        # iterate over the dates and for each date get the list of measurements
        for date in unique_dates:
            daily_measurements = self._get_daily_measurements(date)

            avg_sys, avg_dia = self._calc_averages(daily_measurements)

            # append to daily_avg
            self.daily_avg.append(Datapoint(date, avg_sys, avg_dia))

    def calc_seven_day_avg(self):
        self.seven_day_avg = []

        # iterate over the daily average
        first_index = 0
        last_index = len(self.daily_avg)
        # print(f"first index : {first_index}")
        # print(f"last index : {last_index}")

        for start in range(first_index, last_index - 6):

            measurements = self.daily_avg[start:start + 7]
            # print(measurements)

            sum_sys = 0
            sum_dia = 0
            for m in measurements:
                sum_sys += m.sys
                sum_dia += m.dia

            avg_sys = sum_sys // 7
            avg_dia = sum_dia // 7
            date = measurements[-1].date

            self.seven_day_avg.append(Datapoint(date=date, sys=avg_sys, dia=avg_dia))

    def print_number_measurements(self):
        print(len(self.measurements))

    def print_daily_average(self):
        table = PrettyTable(["Date", "SYS", "DIA"])
        for m in self.daily_avg:
            row = m.date, m.sys, m.dia
            table.add_row(row)
        print(table)

    def print_seven_day_avg(self):
        table = PrettyTable(["Date", "SYS", "DIA"])
        for m in self.seven_day_avg:
            row = m.date, m.sys, m.dia
            table.add_row(row)
        print("Seven Day Rolling Average")
        print(table)

    def _get_unique_dates(self) -> List[str]:
        """ get the unique list of dates
        """
        dates = []
        for m in self.measurements:
            if m.date not in dates:
                dates.append(m.date)
        return dates

    def _get_daily_measurements(self, date):
        """ get the list of measurements for a date
        """
        daily_measurements = []
        for m in self.measurements:
            if m.date == date:
                daily_measurements.append(m)
        return daily_measurements

    @staticmethod
    def _calc_averages(daily_measurements: List[Datapoint]) -> Tuple[int, int]:
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

    def import_from_csv(self, file: Path | str):
        if isinstance(file, str):
            file = Path(file)
        if not file.exists():
            raise FileNotFoundError(f'File {file} not found.')
        self.measurements = []
        log.debug("In import CSV")
        with open(file, 'r') as f:
            bp_csv_reader_obj = csv.reader(f)
            for line in bp_csv_reader_obj:
                self.add_measurement(Datapoint(date=line[0], sys=line[1], dia=line[2]))
