# How to Use:

(If you have any questions, comments, or feedback, please get in touch. Contact me at kojiflynndo [AT] gmail.com)

## For people who want to see the data:

### Raw Data

To see new datasets, go to `ouput`. 

If you're interested in...

... each flow for each funder by day, go to `funding_by_day.csv`.

... cumulative funding for each funder each week, go to `cumulative_funding_weekly.csv`.

... total contributions, paid contributions, and committed contributes for each funder on the final day (31 December, 2020) go to `end_totals`.

... COVID-19 cases in GHRP countries each week, go to `covid-cases.csv`.

... when each flow was committed and/or paid, go to `contribution_dates.csv`.

... the proportion of funding going to different classes (i.e. UN, WHO, Red Cross, governments, NGOs), go to `ngo_normalized.csv`.

### Visualizations:

Go to the `docs` folder and follow links in the description.

## For technical users who want to understand and run the code:

To replicate the entire analysis, download the repository and go to `run_all.py`. In `runAll()`, uncomment each of the function calls then run the file. It may take several minutes to complete the entire analysis.

#### Documentation for Key Scripts

##### `ghrp_tracker.py`

This is the main file for processing, analyzing, and creating datasets. The core functions are `cumulativeByWeek()` and `cumulativeCovidCases()`, each of which create new datasets tracking humanitarian contributions and COVID-19 cases, respectively. `cumulativeByWeek()` calls several helper functions, specifically `fundingByDay()` to get data on each funder for each day from the Development Initiatives dataset, `getMondays()` to get each Monday in the year, and `isNGO()` to see if the recipient was an NGO; then, it outputs `cumulative_funding_weekly.csv`. `cumulativeCovidCases()` takes the COVID-19 dataset from Our World in Data and filters out non-GHRP countries and non-Monday days (again with `getMondays()`. Then, it outputs `covid-cases.csv`.

Also included in `ghrp_tracker.py` are other helper functions to clean dataframe columns (`cleandf()`), check if the implementing recipient is missing (`checkImplementerBlank()`), compute some statistics about COVID-19 cases I was interested in (`covidStats()`), and pull all contributors' names (`getFunders()`).

##### `fts_analysis.py`

`fts_analysis.py` analyzes files scraped directly from Mark Brough's (Development Initiatives) GitHub. First, run `gh_scraping.py` to scrape the SHAs (stored in `gh_sha.txt` in `output`) and `gh_processing.py` and convert them into interesting data. 

FTS does not report the date that a flow was pledged, committed, or paid. Instead, it shows the date a flow was reported and its current status. This is a major failing, since one would naturally like to know when a flow was pledged, and also when a flow was committed, and also when a flow was paid. To get around this, I ran through all of the files Mark scraped from FTS. Mark was scraping FTS each day (and for a while, each hour) to see new humanitarian aid flows. `gh_processing.py` goes through each of these copies of the data by day, from earliest to most recent, and compares them to the previous copies. In this way, one can see the date that a flow was updated from committment to payment, for example. These three scripts are where `contribution_dates.csv` and `funding_speed.csv` come from. 


##### `ghrp_viz.py`

This is the main file for visualizing the results of the analysis and processing. It also contains a few functions for processing data for those visualizations. The visualizations are made with the `altair` package. Most functions should be fairly self-explanatory.

`stacked()` creates the vertically concatenated chart with COVID-19 cases (`plotCovid()`) and cumulative humanitarian funding (`plotCumulative()`). 

`plotNGO()` creates two charts: one stacked area chart, sorted by the class of recipient (eg UN, WHO, NGO, governments) called `ngoArea` and one normalized area chart (i.e. fills 100% of the chart) which does the same called `ngoNormalized`. The function uses `getNGOdata()` to get the distribution of funding across those classes of recipients.

`plotUnpaid()` also creates two charts: one bar chart which shows the percentage of unpaid flows by all contributors with more than 15 flows, and the other which shows the number of unpaid flows by the same contributors.

`plotDelays()` creates a bar chart showing how long flows have been committed and not paid. 


