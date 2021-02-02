# How to Use:

## For people who want to see the data:

### Raw Data

To see new datasets, go to `ouput`. 

If you're interested in...

... each flow for each funder by day, go to `funding_by_day.csv`.

... cumulative funding for each funder each week, go to `cumulative_funding_weekly.csv`.

... total contributions, paid contributions, and committed contributes for each funder on the final day (31 December, 2020) go to `end_totals`.

... COVID-19 cases in GHRP countries each week, go to `covid-cases.csv`.

... when each flow was committed and/or paid, go to `contribution_dates`.

### Visualizations:

Go to the `docs` folder and follow links in the description.

## For technical users who want to understand and run the code:

To replicate the entire analysis, download the repository and go to `run_all.py`. In `runAll()`, uncomment each of the function calls then run the file. It may take several minutes to complete the entire analysis.

#### Documentation for Key Scripts

##### `ghrp_tracker.py`

This is the main file for processing, analyzing, and creating datasets. The core functions are `cumulativeByWeek()` and `cumulativeCovidCases()`, each of which create new datasets tracking humanitarian contributions and COVID-19 cases, respectively. `cumulativeByWeek()` calls several helper functions, specifically `fundingByDay()` to get data on each funder for each day from the Development Initiatives dataset, `getMondays()` to get each Monday in the year, and `isNGO()` to see if the recipient was an NGO; then, it outputs `cumulative_funding_weekly.csv`. `cumulativeCovidCases()` takes the COVID-19 dataset from Our World in Data and filters out non-GHRP countries and non-Monday days (again with `getMondays()`. Then, it outputs `covid-cases.csv`.

Also included in `ghrp_tracker.py` are other helper functions to clean dataframe columns (`cleandf()`), check if the implementing recipient is missing (`checkImplementerBlank()`), compute some statistics about COVID-19 cases I was interested in (`covidStats()`), and pull all contributors' names (`getFunders()`).
