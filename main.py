import IO
import logging.config
from prettytable import PrettyTable
import math

logging.config.fileConfig("logging_config.ini")
log = logging.getLogger(__name__)


class BPLog:
    def __init__(self):
      #self.measurements is the full list of measurements taken.
      self.measurements = []
      #self.measurements_daily_avg is a average of any set of measurements taken for a paticular day.
      self.measurements_daily_avg = []
      # self.measurements_sevenday_avg is the seven day rolling average measurement set.
      self.measurements_sevenday_avg = []


    def add_measurement(self, measurement):
        if measurement[0] != "Date":
            self.measurements.append(measurement)
        return None

    def print_number_measurements(self):
        print(len(self.measurements))
        return None

    def print_daily_average(self):
        mytable = PrettyTable(["Date","SYS","DIA"])
        for row in self.measurements_daily_avg:
            mytable.add_row(row)
        print(mytable)

    def set_measurements_daily_avg(self):
        # get the unique list of dates
        unique_dates_lst = []
        for m in self.measurements:
            date = m[0]
            if date not in unique_dates_lst:
                unique_dates_lst.append(date)
            else:
                pass
        # iterate over the dates and for each date get the list of measurements

        for date in unique_dates_lst:
            daily_measurements_lst = []
            for measurement in self.measurements:
                if measurement[0] == date:
                    daily_measurements_lst.append(measurement)
                else:
                    pass

        # calculate the average sys and dia from that list
            sum_sys = 0
            sum_dia = 0
            for measurement in daily_measurements_lst:
                sum_sys = sum_sys + int(measurement[1])
                sum_dia = sum_dia + int(measurement[2])
            avg_sys = sum_sys / len(daily_measurements_lst)
            avg_dia = sum_dia / len(daily_measurements_lst)
            avg_sys = math.trunc(avg_sys)
            avg_dia = math.trunc(avg_dia)

        # append to measurements_daily_avg
            self.measurements_daily_avg.append([date, avg_sys, avg_dia ] )

    def set_measurements_sevenday_avg(self):
        # interate over the daily average
        first_index = 0
        last_index = len(self.measurements_daily_avg)
        #print(f"first index : {first_index}")
        #print(f"last index : {last_index}")

        for start in range(first_index,last_index-6):
            #print(f"start : {start}")
            #print(f"emd : {start + 7}")

            res = []
            res.extend(self.measurements_daily_avg[start:start+7])
            #print(res)

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
        mytable = PrettyTable(["Date","SYS","DIA"])
        for row in self.measurements_sevenday_avg:
            mytable.add_row(row)
        print("Seven Day Rolling Average")
        print(mytable)



def main():
    log.debug("Running main function")
    print("JWTO")
    my_log = BPLog()
    bp_lst = IO.importcsv_lst()
    for bp in bp_lst:
        my_log.add_measurement(bp)

    #my_log.print_number_measurements()
    my_log.set_measurements_daily_avg()
    #my_log.print_daily_average()
    my_log.set_measurements_sevenday_avg()
    my_log.print_measurements_sevenday_avg()
    print("JWTO")


if __name__ == "__main__":
    main()

