#!/usr/bin/env python
import pandas as pd
import dateutil.parser
import namestand
import us
import glob
import sys, os
import itertools
import re
flatten = lambda x: list(itertools.chain.from_iterable(x))

t = namestand.translator
standardizer = namestand.combine([
    namestand.downscore,
    t(re.compile(r"address(\d)"), r"address_\1"),
    t(re.compile(r"(number|nbr)"), r"no"),
    t(re.compile(r"(visa_type|visa_class|case_type)"), "visa_type"),
    t("recent_decision_date", "last_event_date"),
    t("decision_date", "last_event_date"),
    t("last_sig_event", "case_status"),
    t("case_num", "case_no"),
    t("emp_", "employer_"),
    t("num_aliens", "no_workers_requested"),
    t("no_workers_requsted", "no_workers_requested"),
    t("npc_submitted_date", "case_received_date"),
])

year_pat = re.compile(r"FY(\d+)")
def get_fy_from_path(path):
    last = path.split("/")[-1]
    found = int(re.search(year_pat, last).group(1))
    fy = found if found > 99 else 2000 + found
    return fy

visa_type_pat = re.compile(r"H-?2(A|B)")
def get_visa_type_from_path(path):
    last = path.upper().split("/")[-1]
    v_type = "H-2" + re.search(visa_type_pat, last).group(1)
    return v_type

def parse_date(x):
    if isinstance(x, basestring):
        d = dateutil.parser.parse(x)
    else:
        d = x
    try: return d.date()
    except: return d

def read_file(path):
    if path[-3:] == "csv":
        raw = pd.read_csv(path)
    else:
        raw = pd.read_excel(path)
    renamed = raw.rename(columns=dict(zip(raw.columns, standardizer(raw.columns))))

    # Note: FY2006 H-2A data has no decision date / last event date.
    if "last_event_date" in renamed.columns:
        renamed["last_event_date"] = renamed["last_event_date"].apply(parse_date)

    renamed["fy"] = get_fy_from_path(path)
    renamed["visa_type"] = get_visa_type_from_path(path)
    return renamed

def read_all(src_dir):
    paths = glob.glob(os.path.join(src_dir, "*"))
    dfs = map(read_file, paths)
    return dfs

def norm_name(row):
    if row[0]: name = row[0]
    else: name = "{0} {1}".format(*row[1:])
    return name.strip().upper()

def norm_law(row):
    return row[0] if len(row[0].strip()) > 0 else row[1]

def get_state_abbr(x):
    if isinstance(x, basestring) and len(x) > 2:
        return us.states.lookup(x)
    else:
        return x

def combine(src_dir):
    # Read in all spreadsheets
    dfs = read_all(src_dir)
    decisions = pd.concat(dfs)

    # Normalize employer_state to postal abbreviations
    decisions["employer_state"] = decisions["employer_state"].apply(get_state_abbr)

    # Uppercase addresses and cities
    for_upping = [ "employer_address_1", "employer_address_2", "employer_city" ]
    decisions[for_upping] = decisions[for_upping].fillna("")\
        .applymap(lambda x: unicode(x).upper().strip())

    # Classify certifications and expired certifications
    def is_certified(x):
        return "CERTIF" in x.upper()

    def is_expired(x):
        return "EXPIR" in x.upper()

    decisions["is_certified"] = decisions["case_status"]\
        .apply(is_certified).astype(bool)

    decisions["is_expired"] = decisions["case_status"]\
        .apply(is_expired).astype(bool)

    # Fill in n_certified data, if missing, based on other columns
    decisions["n_certified"] = (decisions["no_workers_certified"]\
        .fillna(decisions["no_workers_requested"]) * decisions["is_certified"])\
        .fillna(0)\
        .astype(int)

    # Don't count as certified in the (relatively rare) scenario
    # that the number of workers certified is null or 0
    decisions["is_certified"] = decisions["n_certified"] > 0

    # If an entry includes one these organization flags,
    # it's a duplicate/umbrella application 
    decisions["is_duplicate"] = decisions["organization_flag"].isin([
        "A",
        "Association - Joint Employer (H-2A Only)"
    ])

    core_cols = [
        "visa_type",
        "fy",
        "last_event_date",
        "case_no",
        "case_status",
        "n_certified",
        "employer_name",
        "employer_state",
        "employer_city",
        "employer_address_1",
        "employer_address_2",
        "is_certified",
        "is_expired",
        "is_duplicate",
    ]
    return decisions[core_cols].sort([ "fy", "visa_type", "last_event_date" ])

if __name__ == "__main__":
    combined = combine(sys.argv[1])
    combined.to_csv(sys.stdout, index=False, encoding="utf-8")
