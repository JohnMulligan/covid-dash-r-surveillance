from rpy2.rinterface_lib import openrlib
from rpy2 import robjects as ro
import pandas as pd
import datetime
def serial_date_to_string(srl_no):
        new_date = datetime.datetime(1970,1,1,0,0) + datetime.timedelta(srl_no - 1)
        return new_date.strftime("%Y-%m-%d")


def multi(jurisdictions,causes):
        with openrlib.rlock:
                r=ro.r
                ro.globalenv['jurisdictions']=jurisdictions
                ro.globalenv['causes']=causes
                r_df=r.source('farrington_multiselect.R')
                cause_fac=ro.FactorVector(r_df[0][1])
                cause_group = [cause_fac.levels[i-1] for i in r_df[0][1]]
                week_ending = [serial_date_to_string(i) for i in r_df[0][6]]
                observed = [int(i) for i in r_df[0][7]]
                alarm = [['','x'][int(i)] for i in r_df[0][9]]
                upperbound = [float(i) for i in r_df[0][10]]
                lowerbound = [float(i) for i in r_df[0][11]]
                df={
                'week_ending':week_ending,
                'observed':observed,
                'alarm':alarm,
                'upperbound':upperbound,
                'lowerbound':lowerbound}
                pass
        return df

def bystate(jurisdiction):
	with openrlib.rlock:
		r=ro.r
		print('jurisdiction=',jurisdiction,'endtest')
		ro.globalenv['jurisdiction']=jurisdiction
		r_df=r.source('farrington_bystate.R')
		cause_fac=ro.FactorVector(r_df[0][1])
		cause_group = [cause_fac.levels[i-1] for i in r_df[0][1]]
		week_ending = [serial_date_to_string(i) for i in r_df[0][6]]
		observed = [int(i) for i in r_df[0][7]]
		alarm = [['','x'][int(i)] for i in r_df[0][9]]
		upperbound = [float(i) for i in r_df[0][10]]
		lowerbound = [float(i) for i in r_df[0][11]]
		df={
		'cause_group':cause_group,
		'week_ending':week_ending,
		'observed':observed,
		'alarm':alarm,
		'upperbound':upperbound,
		'lowerbound':lowerbound}
		pass
	return df

