#!/usr/bin/env python
import pandas as pd
import sys, os

HERE = os.path.dirname(os.path.realpath(__file__))

relpath = "../data/oflc-decisions/processed/oflc-decisions.csv"
decisions = pd.read_csv(os.path.join(HERE, relpath))

emp_up = decisions["employer_name"]\
    .fillna("")\
    .str.upper()

DEST_BASE = os.path.join(HERE, "../output/certification-lists/")
def write_matching(name, criteria):
    df = decisions[criteria]
    path = "{0}{1}.csv".format(DEST_BASE, name)
    df.to_csv(path, index=False, encoding="utf-8")
    
if __name__ == "__main__":
    write_matching(
        "peri-and-sons-2015",
        (emp_up.str.contains("PERI.*SONS") &
        (decisions["last_event_date"] >= "2015-01-01"))
    )

    write_matching(
        "sierra-cascade-nursery-2015",
        (emp_up.str.contains("SIERRA CASCADE") &
        (decisions["last_event_date"] >= "2015-01-01"))
    )

    write_matching(
        "overlook-harvesting-2015",
        (emp_up.str.contains("OVERLOOK HARV") &
        (decisions["last_event_date"] >= "2015-01-01"))
    )

    write_matching(
        "randy-clanton-farms-2015",
        (emp_up.str.contains("CLANTON FARM") &
        (decisions["last_event_date"] >= "2015-01-01"))
    )

    write_matching(
        "liuzza-produce-farm-2015",
        (emp_up.str.contains("LIUZZA (PRODUCE|FARM)") &
        (decisions["last_event_date"] >= "2015-01-01"))
    )

    write_matching(
        "crystal-rock-and-castle-rock",
        emp_up.str.contains("(CASTLE|CRYSTAL).?ROCK")
    )
