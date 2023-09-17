import logging.config
import BPLog as BP

logging.config.fileConfig("logging_config.ini")
log = logging.getLogger(__name__)


def main():
    log.debug("Running main function")
    print("JWTO")
    my_log = BP.BPLog()
    my_log.import_from_csv('../tests_data/230915_BP.csv')

    # my_log.print_number_measurements()
    my_log.set_measurements_daily_avg()
    # my_log.print_daily_average()
    my_log.set_measurements_sevenday_avg()
    my_log.print_measurements_sevenday_avg()
    print("JWTO")


if __name__ == "__main__":
    main()
