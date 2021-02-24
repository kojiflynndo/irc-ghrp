# File for quickly filtering the actors to sense-check and creating csv files
# for ECHO, USAID, and 

library('tidyverse')
library('readxl')


iatiDF <- read_excel("~/IRC/COVID/code/input/transactions_sectors_countries_regions.xlsx")

iatiDF %>%
  count(covid_relevant)

# Contributors -----

# for both ECHO and Germany, all flows are reported as covid_relevant = MAYBE
echo <- iatiDF %>%
  filter(reporting_org_ref == "XI-IATI-EC_ECHO") %>%
  mutate(transaction_date = as.Date(transaction_date),
         id = ...1) %>%
  filter(transaction_date >= as.Date('2020-01-01'),
         transaction_date <= as.Date('2020-12-31'),
         covid_relevant != 'NO')

germany <- iatiDF %>%
  filter(reporting_org_ref == "XM-DAC-5-7") %>%
  mutate(transaction_date = as.Date(transaction_date),
         id = ...1) %>%
  filter(transaction_date >= as.Date('2020-01-01'),
         transaction_date <= as.Date('2020-12-31'),
         covid_relevant != 'NO')

# USAID reported 660 MAYBE, 11147 NO, 1906 YES
usaid <- iatiDF %>%
  filter(reporting_org_ref == "US-GOV-1") %>%
  mutate(transaction_date = as.Date(transaction_date),
         id = ...1) %>%
  filter(transaction_date >= as.Date('2020-01-01'),
         transaction_date <= as.Date('2020-12-31'),
         covid_relevant != 'NO')


# NGOs -----
actionaid <- iatiDF %>%
  filter(reporting_org_ref == "GB-CHC-274467") %>%
  mutate(transaction_date = as.Date(transaction_date),
         id = ...1) %>%
  filter(transaction_date >= as.Date('2020-01-01'),
         transaction_date <= as.Date('2020-12-31'),
         covid_relevant != 'NO')

novib <- iatiDF %>%
  filter(reporting_org_ref == "NL-KVK-27108436") %>%
  mutate(transaction_date = as.Date(transaction_date),
         id = ...1) %>%
  filter(transaction_date >= as.Date('2020-01-01'),
         transaction_date <= as.Date('2020-12-31'),
         covid_relevant != 'NO')

drc <- iatiDF %>%
  filter(reporting_org_ref == "DK-CVR-20699310") %>%
  mutate(transaction_date = as.Date(transaction_date),
         id = ...1) %>%
  filter(transaction_date >= as.Date('2020-01-01'),
         transaction_date <= as.Date('2020-12-31'),
         covid_relevant != 'NO')

# Multilateral -----

unhcr <- iatiDF %>%
  filter(reporting_org_ref == "XM-DAC-41121") %>%
  mutate(transaction_date = as.Date(transaction_date),
         id = ...1) %>%
  filter(transaction_date >= as.Date('2020-01-01'),
         transaction_date <= as.Date('2020-12-31'),
         covid_relevant != 'NO')


# Sending to CSV -----
dfs <- c(echo,
         germany,
         usaid,
         
         actionaid,
         novib,
         drc,
         
         unhcr)

write_csv(echo, file = 'echo_iati.csv')
write_csv(germany, file = 'germany_iati.csv')
write_csv(usaid, file = 'usaid_iati.csv')
write_csv(actionaid, file = 'actionaid_iati.csv')
write_csv(novib, file = 'novib_iati.csv')
write_csv(drc, file = 'drc_iati.csv')
write_csv(unhcr, file = 'unhcr_iati.csv')


