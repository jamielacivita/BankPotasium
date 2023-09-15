import csv
import logging
log = logging.getLogger(__name__)

def importcsv_lst():
    out_lst = []
    log.debug("In import CSV")
    with open("230915_BP.csv") as f:
        bp_csv_reader_obj = csv.reader(f)
        for line in bp_csv_reader_obj:
            date = line[0]
            sys = line[1]
            dia = line[2]
            trim_lst = [ date, sys, dia]
            out_lst.append(trim_lst)
    f.close()

    return out_lst


