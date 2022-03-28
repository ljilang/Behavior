#*********************
#
# Statistics III: Repeated measurements
# Day 2, Exercise 1 Random Intercept Model
#
#*********************

#__________________________
# Import packages          \_________________________________________________________________________________

library(psych)
library(dplyr)
library(rstatix)
library(emmeans)
library(lme4)
library(ggplot2)
library(stats)

#__________________________
# Import & open data       \_________________________________________________________________________________

dep_df <- read.delim("~/Documents/Courses/Extra/Statistics_III/WicksellLongComplete.txt")
View(dep_df)

#__________________________
# Prep work                \_________________________________________________________________________________

# Delete all subjects from Group 2

dep_df <- dep_df[dep_df$Group == 1, ]
nrow(dep_df) 

# Create a categorical time and subject variable 
dep_df$TimeCat <- as.factor(dep_df$Time)
dep_df$Subj_fac <- as.factor(dep_df$Subject)


# Plot individual subjects' scores over time, in grid
dep_df$Subj_fac <- as.factor(dep_df$Subject)
ggplot(data = dep_df, aes(x = Time, y = dv)) + geom_line() +
  facet_wrap(~Subj_fac)

# Or: all subjects in same plot
ggplot(data = dep_df, mapping = aes(x = Time, y = dv, color = Subj_fac)) +
  geom_line()

# Or, fit a reg line
ggplot(data = dep_df, mapping = aes(x = Time, y = dv)) + geom_point() +
  stat_smooth(method = "lm", se = FALSE, color = 'indianred', size = 0.5) + facet_wrap(~Subj_fac)

#__________________________
# Analysis                 \_________________________________________________________________________________

# Time as continuous variable
model_cont <- lmer(dv~Time + (1|Subject), data= dep_df)
summary(model_cont) # average decrease in depression score over one month: 24.62; Intercept 292.95
anova(model_cont) # F-value: 45.59
confint(model_cont) 

# Check the normality of the residuals
qqnorm(resid(model_cont))
qqline(resid(model_cont))

# Check the normality of the random effects
blups<-unlist(ranef(model_cont)$Subject)
qqnorm(blups); qqline(blups, col = c("red"))

# Plot residuals vs fitted values 
xb<-predict(model_cont, re.form=NA)
res<-residuals(model_cont)
plot(xb, res)

# Time as categorical variable 
model_cat <- lmer(dv~TimeCat + (1|Subject), data= dep_df)
summary(model_cat) # Intercept: 304.33
anova(model_cat) # F-value: 15.1
confint(model_cat)

# Mean scores, pairwise comparisons and CIs for model_cat
testTimeCat<-emmeans(model_cat, ~TimeCat)
summary(testTimeCat) # average depression score at time point 6 is 149
confint(pairs(testTimeCat), adj="none")

# Predict average dv score for average participant at month 5 and 7
extrapData <- dep_df[1,]
extrapData$Time <- 5
predict(model_cont , newdata = extrapData, re.form=NA)

extrapData <- dep_df[1,]
extrapData$Time <- 7
predict(model_cont , newdata = extrapData, re.form=NA)

# Use bootstrapping to get estimated CIs 
b <- bootMer(model_cont, nsim=1000, seed = 24,
             FUN=function(x)predict(x, newdata=extrapData, re.form=NA)) # add seed argument
quantile(b$t, probs=c(0.025, 0.975))

# Plot random effects with fixed slopes
dep_df %>% 
# save predicted values
  mutate(pred_dist = fitted(model_cont)) %>% 
  ggplot(aes(x=Time, y=pred_dist, group=Subject, color=Subj_fac)) + 
  theme_classic() +
  geom_line(size=0.75) +
  geom_point(mapping = aes(x = Time, y = dv, color = Subj_fac)) +
  labs(x="Time", y="Depression score") + #, title="Individual estimated depression scores over time") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_color_discrete(name = "Subject") +
  geom_smooth(aes(group = 1), method = "lm", size = 0.75, color = "black", se = FALSE) 
  