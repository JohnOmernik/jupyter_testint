#!/usr/bin/python

# Base imports for all integrations, only remove these at your own risk!
import json
import sys
import os
import time
import pandas as pd
from collections import OrderedDict

from integration_core import Integration

from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)
from IPython.core.display import HTML

# Your Specific integration imports go here, make sure they are in requirements!
import requests

#import IPython.display
from IPython.display import display_html, display, Javascript, FileLink, FileLinks, Image
import ipywidgets as widgets

@magics_class
class Testint(Integration):
    # Static Variables
    # The name of the integration
    name_str = "testint"

    # These are the variables in the opts dict that allowed to be set by the user. These are specific to this custom integration and are joined
    # with the base_allowed_set_opts from the integration base
    custom_allowed_set_opts =  [name_str + '_base_url', name_str + '_verbose_errors']
 
    myopts = {}
    myopts[name_str + '_verbose_errors'] = [False, "Show more verbose errors if available"]
    myopts[name_str + "_user"] = ["johnyfive", "Username to connect with"]
    myopts[name_str + "_base_url"] = ["https://icanhazip.com", "Basic URL for connection"]


    # Class Init function - Obtain a reference to the get_ipython()
    def __init__(self, shell, pd_display_grid="html", *args, **kwargs):
        super(Testint, self).__init__(shell)
        self.opts['pd_display_grid'][0] = pd_display_grid
        if pd_display_grid == "qgrid":
            try:
                import qgrid
            except:
                print ("WARNING - QGRID SUPPORT FAILED - defaulting to html")
                self.opts['pd_display_grid'][0] = "html"

        #Add local variables to opts dict
        for k in self.myopts.keys():
            self.opts[k] = self.myopts[k]



    def disconnect(self):
        if self.connected == True:
            print("Disconnected %s Session from %s" % (self.name_str.capitalize(), self.opts[self.name_str + '_base_url'][0]))
        else:
            print("%s Not Currently Connected - Resetting All Variables" % self.name_str.capitalize())
        self.mysession = None
        self.connected = False

    def connect(self, prompt=False):

        if self.connected == False:
            if prompt == True or self.opts[self.name_str + '_user'][0] == '':
                print("User not specified in JUPYTER_%s_USER or user override requested" % self.name_str.upper())
                tuser = input("Please type user name if desired: ")
                self.opts[self.name_str + '_user'][0] = tuser
            print("Connecting as user %s" % self.opts[self.name_str + '_user'][0])
            print("")

            result = self.auth()
            if result == 0:
                self.connected = True
                print("%s - %s Connected!" % (self.name_str.capitalize(), self.opts[self.name_str + '_base_url'][0]))
            else:
                print("Connection Error - Perhaps Bad Usename/Password?")

        if self.connected != True:
            self.disconnect()

    def auth(self):
        self.session = None
        result = -1
        self.session = requests.Session()
        self.session.allow_redirects = False
        print("Connected as %s" % self.opts[self.name_str + "_user"][0])
        result = 0
        return result


    def validateQuery(self, query):
        bRun = True
        bReRun = False
        if self.last_query == query:
            # If the validation allows rerun, that we are here:
            bReRun = True
        # Ok, we know if we are rerun or not, so let's now set the last_query 
        self.last_query = query

        # Example Validation

        # Warn only - Don't change bRun
        # This one is looking for a ; in the query. We let it run, but we warn the user
        # Basically, we print a warning but don't change the bRun variable and the bReRun doesn't matter
        if query.find(";") >= 0:
            print("WARNING - Do not type a trailing semi colon on queries, your query will fail (like it probably did here)")

        # Warn and don't submit after first attempt - Second attempt go ahead and run
        # If the query doesn't have a day query, then maybe we want to WARN the user and not run the query.
        # However, if this is the second time in a row that the user has submitted the query, then they must want to run without day
        # So if bReRun is True, we allow bRun to stay true. This ensures the user to submit after warnings
        if query.lower().find("limit ") < 0:
            print("WARNING - Queries shoud have a limit so you don't bonkers your DOM")
        # Warn and do not allow submission
        # There is no way for a user to submit this query 
#        if query.lower().find('limit ") < 0:
#            print("ERROR - All queries must have a limit clause - Query will not submit without out")
#            bRun = False
        return bRun

    def customQuery(self, query):

        myjson = [{"hey": "gal", "some": 1, "q": query}, {"hey": "guy", "some": 1, "q": query}]
        mydf = pd.read_json(json.dumps(myjson))
        status = "Success"
        return mydf, status


# Display Help must be completely customized, please look at this Hive example
    def customHelp(self):
        print("jupyter_testing is a interface that allows you to use the magic function %testint to interact with an Testing")
        print("")
        print("jupyter_testint has two main modes %testint and %%testint")
        print("%testint is for interacting with a Hive installation, connecting, disconnecting, seeing status, etc")
        print("%%testint is for running queries and obtaining results back from the Hive cluster")
        print("")
        print("%testint functions available")
        print("###############################################################################################")
        print("")
        print("{: <30} {: <80}".format(*["%testint", "This help screen"]))
        print("{: <30} {: <80}".format(*["%testint status", "Print the status of the Hive connection and variables used for output"]))
        print("{: <30} {: <80}".format(*["%testint connect", "Initiate a connection to the Hive cluster, attempting to use the ENV variables for Hive URL and Hive Username"]))
        print("{: <30} {: <80}".format(*["%testint connect alt", "Initiate a connection to the Hive cluster, but prompt for Username and URL regardless of ENV variables"]))
        print("{: <30} {: <80}".format(*["%testint disconnect", "Disconnect an active Hive connection and reset connection variables"]))
        print("{: <30} {: <80}".format(*["%testint set %variable% %value%", "Set the variable %variable% to the value %value%"]))
        print("{: <30} {: <80}".format(*["%testint debug", "Sets an internal debug variable to True (False by default) to see more verbose info about connections"]))
        print("")
        print("Running queries with %%testint")
        print("###############################################################################################")
        print("")
        print("Some query notes:")
        print("- If the number of results is less than pd_display.max_rows, then the results will be diplayed in your notebook")
        print("- You can change pd_display.max_rows with %hive set pd_display.max_rows 2000")
        print("- The results, regardless of display will be place in a Pandas Dataframe variable called prev_hive")
        print("- prev_testint is overwritten every time a successful query is run. If you want to save results assign it to a new variable")


    # This is the magic name.
    @line_cell_magic
    def testint(self, line, cell=None):
        if cell is None:
            line = line.replace("\r", "")
            line_handled = self.handleLine(line)
            if not line_handled: # We based on this we can do custom things for integrations. 
                if line.lower() == "testintwin":
                    print("You've found the custom testint winning line magic!")
                else:
                    print("I am sorry, I don't know what you want to do with your line magic, try just %" + self.name_str + "for help options")
        else: # This is run is the cell is not none, thus it's a cell to process  - For us, that means a query
            cell = cell.replace("\r", "")
            self.handleCell(cell)

