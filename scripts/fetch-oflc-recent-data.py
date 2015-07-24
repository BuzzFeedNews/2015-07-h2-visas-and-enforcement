#!/usr/bin/env python
import requests
import lxml.html
import sys, os
import re

VISA_TYPES = [ "H[_-]?2[_-]?A", "H[_-]?2[_-]?B" ]
BASE_URL = "http://www.foreignlaborcert.doleta.gov/performancedata.cfm"

data_pattern = re.compile(r"/({0})[^/]*xlsx?$".format("|".join(VISA_TYPES)))

def is_data(href):
    return re.search(data_pattern, href)

def get_urls():
    html = requests.get(BASE_URL).content
    dom = lxml.html.fromstring(html)
    dom.make_links_absolute(BASE_URL)
    hrefs = [ a.attrib["href"] for a in dom.cssselect("a")
        if "href" in a.attrib ]
    data_hrefs = filter(is_data, hrefs)
    return data_hrefs

def download(dest_dir):
    urls = get_urls()
    for u in urls:
        sys.stderr.write("Downloading {0}...\n".format(u))
        data = requests.get(u).content
        fname = os.path.split(u)[-1]
        with open(os.path.join(dest_dir, fname), "w") as f:
            f.write(data)
    
if __name__ == "__main__":
   download(sys.argv[1]) 
