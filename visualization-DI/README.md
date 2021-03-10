This is the data for recreating visualizations conveniently in Excel. If you're interested in more specifics of how the original visualizations were created, visit the `ghrp_viz.py` file in the main branch. If you're interested in how these datasets were put together from the  datasets that were used in the original visualizations, see `di_data_share.py` for the exact procedure.

The data were reconfigured to be easily compatible with other visualization programs, namely Excel. The original visualizations were made with Python and the Altair package, which I take to be somewhat more flexible than Excel (though this is purely speculation--I have no experience using Excel for visualization). If I have speculated poorly about the form of data that would be most easily visualized in Excel, please do let me know!

### A few important notes on the original visualizations and this data:

The COVID-19 case and deaths data is from the Our World in Data [Coronavirus Pandemic GitHub Page](https://github.com/owid/covid-19-data). The COVID-19 data in this repository is current as of 31 December 2020, the end date of the GHRP.

The same is true for data on COVID-19 humanitarian financing--the figures are drawn from Mark Brough's Humanitarian Portal at Development Initiatives, which uses FTS data. The funding data in this repository is current as of 31 December 2020, the end date of the GHRP.

This especially applies to the `delays_histogram_data.csv` file. A previous version of the file in this repository was calculuating the unpaid days since committment by, I believe, some day in March (the file was coded to take the current day (i.e. the day it was being run) as the end date. That has since been ammended to find the unpaid days since committment, ending at 31 December 2020.

#### Please let me know via email if you have any questions about the specifics of the data!
