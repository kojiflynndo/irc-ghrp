This is a somewhat hackey workflow. I was trying out using both R and Python on the same project.

To run this, I start with `iati_select.R` to select the rows that match the funders we're interested in, then export those as csv files. This could also be accomplished by writing some Python code using pandas to select the rows you want.

Then, I run `iati_processsing.py` to pull out the data and dates we want and export those as csv files. Finally, I run `iati_viz.R` to visualize the findings.

Like I said, hackey and could be accomplished in one Python script. I just wanted to stretch my R legs a little!
