# H-2 Visa/Enforcement Data and Analysis

This repository contains the data and code supporting several passages in the BuzzFeed News article, ["The New American Slavery: Invited To The U.S., Foreign Workers Find A Nightmare"](http://www.buzzfeed.com/jessicagarrison/the-new-american-slavery-invited-to-the-us-foreign-workers-f), published July 24, 2015.

## Data

The analyses below depend on two major datasets from the Department of Labor, the agency responsible for protecting workers and vetting employers seeking visas:

- The Wage and Hour Division's WHISARD database, obtained via a Freedom of Information Act request. The database contains information on employers, violations, fines, and other details corresponding to investigations concluded between October 1, 2001 and March 31, 2015. (Note: The WHD has redacted some tables and columns per FOIA exemption 5.) You can download a copy of the data dictionary [here](docs/Standard_WH_Dictionary for FOIA 773130.xls?raw=true). To decompress the data file, run `make data/whd-enforcement-database` from this repository's root directory. Once you do so, the data can be found in [`data/whd-enforcement-database`](data/whd-enforcement-database).

- The Office of Foreign Labor Certification's records of visa-certification decisions for the H-2 visa program. (The visa comes in two types: H-2A for agricultural workers and H-2B for non-agricultural unskilled workers.) Obtained from [here](http://www.foreignlaborcert.doleta.gov/performancedata.cfm) and [here](http://www.flcdatacenter.com/). The raw and processed data can be found in [`data/oflc-decisions`](data/oflc-decisions).

## Analyses

- __Passage__: "Since 2005, Labor Department investigation records show, at least 800 employers have subjected more than 23,000 H-2 guest workers to violations of the federal laws designed to protect them from exploitation, including more than 16,000 instances of H-2 workers being paid less than the promised wage."
- __Analysis__: For the methodology and calculations, see [this notebook](notebooks/h2-violation-aggregates.ipynb).

***

- __Passage__: "Those numbers almost certainly understate the problem, as the federal government doesn’t check up on the vast majority of companies that bring guest workers into this country."
- __Analysis__: For the methodology and calculations, see [this notebook](notebooks/h2-employers-investigated.ipynb).

***

- __Passage__: "[Crystal Rock chief executive Arthur] Gillette, whose company has been certified for at least 358 visas since 2002, [...]"
- __Analysis__: See [this spreadsheet of visa certifications](output/certification-lists/crystal-rock-and-castle-rock.csv).

***

- __Passage__: "A Labor Department investigation opened in 2011 found that Harvest Time owed workers more than $52,000 in back wages for 167 violations of worker protection laws."
- __Analysis__: See [case details here](notebooks/harvest-time-case-1620475.ipynb).

***

- __Passage__: "The Labor Department’s Wage and Hour Division investigated the Arkansas-based Superior Forestry — the largest forestry contractor in the country, according to the department — at least 15 times between 2000 and 2014. [...] But over the course of the Labor Department’s 15 investigations, the agency pinned only minor violations on the company, ordering Superior to repay its workers a total of just $12,652 in back wages over a dozen years."
- __Analysis__: For a listing of cases and back wages, see [this notebook](notebooks/superior-forestry-cases.ipynb)

***

- __Passage__: "Over the previous five years, government investigations found at least 12 firms underpaid H-2 workers by more than $100,000. Yet only one of them was debarred. Five — including an onion producer that had more than 1,400 violations and owed its Mexican workers $2.3 million in back wages — have been certified for more than 2,000 additional visas this year alone."
- __Analysis__: For computation of back wages owed to H-2 workers, see [this notebook](notebooks/top-employer-back-wages.ipynb). For debarment and visa certification details, see [this spreadsheet](data/manual-entry/top-total-h2-backwages-2010-2014-with-details.csv), and the debarment lists in the [`docs` folder](docs/).

## Technical Notes

To re-run the analyses above, you'll need Python 2.7, as well as the Python libraries listed in [requirements.txt](requirements.txt).

## Feedback

If you have questions or feedback about the data or analyses, contact Jeremy Singer-Vine at jeremy.singer-vine@buzzfeed.com.

