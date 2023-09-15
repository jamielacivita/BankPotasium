import IO
import logging.config
logging.config.fileConfig("logging_config.ini")
log = logging.getLogger(__name__)

def main():
    log.debug("Running main function")
    print("JWTO")
    bp_lst = IO.importcsv_lst()
    for bp in bp_lst:
        print(bp)





if __name__ == "__main__":
    main()

