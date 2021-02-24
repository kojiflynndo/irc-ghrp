# Visualizations for IATI data

library(tidyverse)

setwd("~/IRC/COVID/code")

options(scipen=999)

custom <- theme_minimal() +
  theme(text = element_text(family = 'serif', size = 14))

# Recipients -----
ActionAid <- read.csv('output/iati_speed/actionaid_speed.csv')
Novib <- read.csv('output/iati_speed/novib_speed.csv')
DRC <- read.csv('output/iati_speed/drc_speed.csv')
UNHCR <- read.csv('output/iati_speed/unhcr_speed.csv')


## ActionAid UK -----
ActionAid %>%
  ggplot() +
  geom_point(aes(x = as.Date(date), y = total_inflow, group = total_inflow), 
             color = '#1b9e77',
             alpha = 0.6,
             size = 2) + 
  geom_point(aes(x = as.Date(date), y = total_outflow, group = total_outflow),
             color = '#d95f02',
             alpha = 0.6,
             size = 2) +
  custom + 
  labs(title = 'ActionAid UK Incoming Funding (Green) vs Outgoing Funding (Orange)') +
  scale_y_continuous(name = 'USD',
                     labels = scales::dollar_format()) +
  scale_x_date(name = NULL)

ggsave('output/iati_speed/graphs/actionaid.png')

## Oxfam Novib -----
Novib %>%
  ggplot() +
  geom_point(aes(x = as.Date(date), y = total_inflow, group = total_inflow), 
             color = '#1b9e77',
             alpha = 0.6,
             size = 2) + 
  geom_point(aes(x = as.Date(date), y = total_outflow, group = total_outflow),
             color = '#d95f02',
             alpha = 0.6,
             size = 2) +
  custom + 
  labs(title = 'Oxfam Novib Incoming Funding (Green) vs Outgoing Funding (Orange)') +
  scale_y_continuous(name = 'USD',
                     labels = scales::dollar_format()) +
  scale_x_date(name = NULL)

ggsave('output/iati_speed/graphs/novib.png')

## Danish Refugee Council -----
DRC %>%
  ggplot() +
  geom_point(aes(x = as.Date(date), y = total_inflow, group = total_inflow), 
             color = '#1b9e77',
             alpha = 0.6,
             size = 2) + 
  geom_point(aes(x = as.Date(date), y = total_outflow, group = total_outflow),
             color = '#d95f02',
             alpha = 0.6,
             size = 2) +
  custom + 
  labs(title = 'Danish Refugee Council Incoming Funding (Green) vs Outgoing Funding (Orange)') +
  scale_y_continuous(name = 'USD',
                     labels = scales::dollar_format()) +
  scale_x_date(name = NULL)

ggsave('output/iati_speed/graphs/drc.png')

## UNHCR -----
UNHCR %>%
  ggplot() +
  geom_point(aes(x = as.Date(date), y = total_inflow, group = total_inflow), 
             color = '#1b9e77',
             alpha = 0.6,
             size = 2) + 
  geom_point(aes(x = as.Date(date), y = total_outflow, group = total_outflow),
             color = '#d95f02',
             alpha = 0.6,
             size = 2) +
  custom + 
  labs(title = 'UNHCR Incoming Funding (Green) vs Outgoing Funding (Orange)') +
  scale_y_continuous(name = 'USD',
                     labels = scales::dollar_format()) +
  scale_x_date(name = NULL)

ggsave('output/iati_speed/graphs/unhcr.png')






# Contributors -----

## USAID -----
USAID <- read.csv('output/iati_speed/usaid_speed.csv')

USAID50 <- USAID %>%
  mutate(days50 = ifelse(pc50 == '',
                         as.Date('2020-12-31') - as.Date(commit_date),
                         as.Date(pc50) - as.Date(commit_date)
                         )
         )

# median
median(USAID50$days50, na.rm = T)
#standard deviation
sd(USAID50$days50, na.rm = T)
#number of rows, which is number of flows
USAID50 %>% 
  nrow()

# Days before 50 percent paid
USAID50 %>%
  filter(days50 >= 0) %>%
  ggplot() + 
  geom_jitter(aes(x = source, y = days50),
            height = 0.2, width = 0.1,
            alpha = 0.5, 
            color = '#1f78b4') +
  geom_violin(aes(x = source, y = days50), 
              alpha = 0,
              color = '#1f78b4') + 
  geom_boxplot(aes(x = source, y = days50), 
               width = 0.1,
               alpha = 0) +
  labs(title = 'Days From Committment to 50% Fund Disbursal, 452 Flows',
       subtitle = 'Plot displays density distribution',
       caption = 'Data from IATI.  Median: 153 Days; SD: 66 Days',
       y = 'Days to 50% Disbursal',
       x = NULL) +
  custom


ggsave('output/iati_speed/graphs/usaid.png')



## Germany-----
Germany <- read.csv('output/iati_speed/germany_speed.csv')


Germany50 <- Germany %>%
  mutate(days50 = ifelse(pc50 == '',
                         as.Date('2020-12-31') - as.Date(commit_date),
                         as.Date(pc50) - as.Date(commit_date)
                         )
         )

# median
median(Germany50$days50, na.rm = T)
#standard deviation
sd(Germany50$days50, na.rm = T)
#number of rows, which is number of flows
Germany50 %>% 
  nrow()

# Days before 50 percent paid
Germany50 %>%
  filter(days50 >= 0) %>%
  ggplot() + 
  geom_jitter(aes(x = source, y = days50),
              height = 0.2, width = 0.1,
              alpha = 0.5, 
              color = '#1f78b4') +
  geom_violin(aes(x = source, y = days50), 
              alpha = 0,
              color = '#1f78b4') + 
  geom_boxplot(aes(x = source, y = days50), 
               width = 0.1,
               alpha = 0) +
  labs(title = 'Days From Committment to 50% Fund Disbursal, 47 Flows',
       subtitle = 'Plot displays density distribution',
       caption = 'Data from IATI.  Median: 0 Days; SD: 45 Days',
       y = 'Days to 50% Disbursal',
       x = NULL) +
  custom

ggsave('output/iati_speed/graphs/germany.png')

## ECHO -----

ECHO <- read.csv('output/iati_speed/echo_speed.csv')


ECHO50 <- ECHO %>%
  mutate(days50 = ifelse(pc50 == '',
                         as.Date('2020-12-31') - as.Date(commit_date),
                         as.Date(pc50) - as.Date(commit_date)
                         )
         ) %>%
  mutate(days50 = ifelse(commit_date == '',
                         0,
                         days50)) %>%
  view()

# median
median(ECHO50$days50, na.rm = T)
#standard deviation
sd(ECHO50$days50, na.rm = T)
#number of rows, which is number of flows
ECHO50 %>% 
  nrow()

# Days before 50 percent paid
ECHO50 %>%
  filter(days50 >= 0) %>%
  ggplot() + 
  geom_jitter(aes(x = source, y = days50),
              height = 0.2, width = 0.1,
              alpha = 0.5, 
              color = '#1f78b4') +
  geom_violin(aes(x = source, y = days50), 
              alpha = 0,
              color = '#1f78b4') + 
  geom_boxplot(aes(x = source, y = days50), 
               width = 0.1,
               alpha = 0) +
  labs(title = 'Days From Committment to 50% Fund Disbursal; 437 Flows',
       subtitle = 'Plot displays density distribution',
       caption = 'Data from IATI.  Median: 0 Days; SD: 70 Days',
       y = 'Days to 50% Disbursal',
       x = NULL) +
  custom

ggsave('output/iati_speed/graphs/echo.png')
