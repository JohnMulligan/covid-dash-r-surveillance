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


#Using the cause of death demographic dataset
counts <- read_csv("Weekly_counts_of_death_by_jurisdiction_and_cause_of_death.csv")
#print(counts)
#have to clean a lot of detail out of this in order to make the pivot work properly

counts<-counts[,!colnames(counts) %in% c('Cause Subgroup','Time Period','Suppress','Note','Average Number of Deaths in Time Period','Difference from 2015-2019 to 2020','Percent Difference from 2015-2019 to 2020')]
wide_counts_by_cause<-pivot_wider(counts,names_from='Cause Group',values_from='Number of Deaths',values_fn=(`Cause Group`=sum))
#wide_counts_by_cause[1,]
#print(wide_counts_by_cause)
wide_state <- filter(wide_counts_by_cause,`State Abbreviation`==jurisdiction)
#print(wide_state)
wide_state <- filter(wide_state,Type=='Unweighted')
#print(wide_state)
wide_state[is.na(wide_state)] <-0
#print(wide_state)
important_columns=c('Alzheimer disease and dementia','Cerebrovascular diseases','Heart failure','Hypertensive dieases','Ischemic heart disease','Other diseases of the circulatory system','Malignant neoplasms','Diabetes','Renal failure','Sepsis','Chronic lower respiratory disease','Influenza and pneumonia','Other diseases of the respiratory system','Residual (all other natural causes)')


all_columns <- append(c('Year','Week'),important_columns)
#print(wide_state)
selected_wide_state<-wide_state[, names(wide_state) %in% all_columns]

#print(selected_wide_state)


#print(selected_wide_state)


start<-c(min(selected_wide_state[,'Year']),min(selected_wide_state[,'Week']))
#print(start)
freq<-max(selected_wide_state[,'Week'])
year_week_pairs<-unique(select(selected_wide_state,'Year','Week'))
year_week_date_triples<-unique(select(counts,'Year','Week','Week Ending Date'))

#print(start)
#print(freq)
#print(year_week_pairs)


#but "observed" must be a numeric matrix, so I need to roll up the different subgroups into columns (currently in rows) for the same jurisdiction/year/week pair
numeric_wide_state<-data.matrix(selected_wide_state,rownames.force=NA)[order(selected_wide_state[,'Year'],selected_wide_state[,'Week']),]

numeric_wide_state<-numeric_wide_state[,!colnames(numeric_wide_state) %in% c('Year','Week')]


#print(numeric_wide_state)
#print(freq)
sts <- new("sts",epoch=1:nrow(numeric_wide_state),start=start,freq=freq,observed=numeric_wide_state)

sts_4 <- aggregate(sts[,important_columns],nfreq=nfreq)
#plot(sts_4,type = observed ~ time)
#plot(sts_4,type = observed ~ time | unit)
end_idx<-as.numeric(dim(sts_4)[1])
start_idx=end_idx-steps_back

cntrlFar <- list(range=start_idx:end_idx,w==w,b==b,alpha==alpha)
surveil_ts_4_far <- farrington(sts_4,control=cntrlFar)
far_df<-tidy.sts(surveil_ts_4_far)
far_df
