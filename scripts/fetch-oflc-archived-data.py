#!/usr/bin/env python
import requests
import lxml.html
import zipfile
import sys, os
import re
import subprocess
import tempfile
import itertools
import StringIO

flatten = lambda x: list(itertools.chain.from_iterable(x))

data_pattern = re.compile(r"download/.*\d{4}.zip$")

URLS = [
    "http://www.flcdatacenter.com/CaseH2A.aspx",
    "http://www.flcdatacenter.com/CaseH2B.aspx"
]

def is_data(href):
    return re.search(data_pattern, href)

def get_urls_from_page(page_url):
    html = requests.get(page_url).content
    dom = lxml.html.fromstring(html)
    dom.make_links_absolute(page_url)
    hrefs = [ a.attrib["href"] for a in dom.cssselect("a")
        if "href" in a.attrib ]
    data_hrefs = filter(is_data, hrefs)
    return data_hrefs
    
def get_zip_urls():
    hrefs = flatten(map(get_urls_from_page, URLS))
    return hrefs

def extract_csv_from_mdb_zip(file_like_object):
    with zipfile.ZipFile(file_like_object, "r") as z:
        mdb_name = [ name for name in z.namelist()
            if name[-3:] == "mdb" ][0]
        mdb = tempfile.NamedTemporaryFile("w")
        mdb.write(z.read(mdb_name))
        table_name = subprocess.Popen(["mdb-tables", "-1", mdb.name ],
           stdout=subprocess.PIPE
        ).communicate()[0].strip()
        table_stdout, table_stderr = subprocess.Popen(
            ["mdb-export", mdb.name, table_name ],
           stdout=subprocess.PIPE
        ).communicate()
        return "".join(table_stdout)

def download(dest_dir):
    zip_urls = get_zip_urls()
    for url in zip_urls:
        sys.stderr.write("Downloading {0}...\n".format(url))
        zip_raw = StringIO.StringIO(requests.get(url).content)
        fname = url.split("/")[-1].split(".")[0]
        csv_str = extract_csv_from_mdb_zip(zip_raw)
        path = os.path.join(dest_dir, fname + ".csv")
        with open(path, "w") as f:
            f.write(csv_str)
    
if __name__ == "__main__":
   download(sys.argv[1]) 

