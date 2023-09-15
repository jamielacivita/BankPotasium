import logging.config
logging.config.fileConfig("logging_config.ini")
log = logging.getLogger(__name__)

def main():
    log.debug("Running main function")
    print("JWTO")


if __name__ == "__main__":
    main()

