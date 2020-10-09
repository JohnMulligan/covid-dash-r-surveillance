#much of what follows comes from this walkthrough: http://surveillance.r-forge.r-project.org/hoehle-surveillance.pdf
#the datasets come from NCHS & CDC. see "proposed analysis workflow"


library('surveillance')
library(readr)
library(tidyr)
library(dplyr)
w<-1
b<-3
nfreq<-52
steps_back<- 28
alpha<-0.05

#jurisdictions<-c('TX','CA')
#causes<-c('Alzheimer disease and dementia','Cerebrovascular diseases','Heart failure')

print(jurisdictions)
print(causes)


#Using the cause of death demographic dataset
counts <- read_csv("Weekly_counts_of_death_by_jurisdiction_and_cause_of_death.csv")
#print(counts)
#have to clean a lot of detail out of this in order to make the pivot work properly

counts_filtered<-filter(counts,Type=='Unweighted')

#filter by jurisdiction
counts_filtered<-filter(counts_filtered,`State Abbreviation` %in% jurisdictions)

#filter by cause group
counts_filtered<-filter(counts_filtered,`Cause Group` %in% causes)

#cut out all but Date info and mortality counts
reduced_dataset<-counts_filtered[,!colnames(counts_filtered) %in% c('Type','Jurisdiction','State Abbreviation','Cause Group','Cause Subgroup','Time Period','Suppress','Note','Average Number of Deaths in Time Period','Difference from 2015-2019 to 2020','Percent Difference from 2015-2019 to 2020')]

#and then roll up the death counts in our selcted dataset
counts_aggregated<-aggregate(`Number of Deaths` ~ `Week Ending Date`+Week+Year,reduced_dataset,sum)

start<-c(min(counts_aggregated[,'Year']),min(counts_aggregated[,'Week']))
freq<-max(counts_aggregated[,'Week'])

#but "observed" must be a numeric matrix
numeric_data<-data.matrix(counts_aggregated)[order(counts_aggregated[,'Year'],counts_aggregated[,'Week']),]

#strip out now-extraneous columns
numeric_data<-numeric_data[,'Number of Deaths']

#sts <- new("sts",epoch=1:288,start=start,freq=52,observed=numeric_data)
sts <- new("sts",epoch=1:length(numeric_data),start=start,freq=52,observed=numeric_data)

end_idx<-as.numeric(dim(sts)[1])
start_idx=end_idx-steps_back

cntrlFar <- list(range=start_idx:end_idx,w=w,b=b,alpha=alpha)
surveil_ts_4_far <- farrington(sts,control=cntrlFar)
far_df<-tidy.sts(surveil_ts_4_far)
far_df

