This sort of template would allow people who need R packages (lots of legacy tools in there!) but use pandas to hook into a web visualizer.

![dash 1](https://github.com/JohnMulligan/covid-dash-r-surveillance/blob/master/dash1.png)

![dash 2](https://github.com/JohnMulligan/covid-dash-r-surveillance/blob/master/dash2.png)

For now, only works single-threaded, that is, not in production, unless someone can figure out how to limit the web server to a single thread. I've had surprisingly little luck with apache and wsgi.
(rpy2 crashes with multithreading)

So, install necessary r packages, test by running one of the farrington R scripts in here (you'll have to pass it state and cause parameters)

And then launch in dev mode (exposes on port 8050):

python3 flask_app.py

##October 7 update

Have split this into 2 dashboards:
* flask_app_multiselect.py (which allows you to roll up causes & states together and re-calculate)
* flask_app_bystate.py (which calculates all the causes in a state, then lets you select by cause on-page)

##October 8 update

Now using latest data (October 7) from CDC/NCHS: https://data.cdc.gov/NCHS/Weekly-counts-of-death-by-jurisdiction-and-cause-o/u6jv-9ijr/



I also have a custom R package working with this example, showing a full confidence interval from the farrington epidemiological outbreak detection algorithm, both because that's important in itself and because it shows the utility of having an R vm template ready to go.

[custom r package](https://github.com/JohnMulligan/surveillance-1)
