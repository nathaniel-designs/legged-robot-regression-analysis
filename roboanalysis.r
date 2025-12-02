#install.packages("readr")
library(readr)
library(car)


robot_data <- read_csv("robot_dataset.csv")

#Translation note:
#X = left-right, Y = forward-backward
head(robot_data, 10)
summary(robot_data)
colSums(is.na(robot_data))
#No missing data! 

avg_angularmag <- mean(robot_data$angular_mag)
median_angularmag <- median(robot_data$angular_mag)
stddev_angularmag <- sd(robot_data$angular_mag)
min_angularmag <- min(robot_data$angular_mag, na.rm = TRUE)
max_angularmag <- max(robot_data$angular_mag, na.rm = TRUE)
range_angularmag <- max_angularmag-min_angularmag

avg_jmag <- mean(robot_data$jmag)
median_jmag <- median(robot_data$jmag)
stddev_jmag <- sd(robot_data$jmag)
min_jmag <- min(robot_data$jmag, na.rm = TRUE)
max_jmag <- max(robot_data$jmag, na.rm = TRUE)
range_jmag <- max_jmag-min_jmag

data_exploration_df <- data.frame(
  Statistic = c("Mean", "Median", "Std Dev", "Min", "Max", "Range"),
  AngularMag = c(avg_angularmag, median_angularmag, stddev_angularmag, min_angularmag, max_angularmag, range_angularmag),
  JerkMag = c(avg_jmag, median_jmag, stddev_jmag, min_jmag, max_jmag, range_jmag)
)

print(data_exploration_df)
robot_data$Environment <- as.factor(robot_data$Environment)
levels(robot_data$Environment)

hist(robot_data$angular_mag, main = "Histogram of Angular Magnitude")
hist(robot_data$jmag, main = "Histogram of Jerk Magnitude")

hist(log(robot_data$angular_mag), main = "Histogram of Log-Transformed Angular Magnitude")
hist(log(robot_data$jmag), main = "Histogram of Log-Transformed Jerk Magnitude")

plot(robot_data$angular_mag, robot_data$jmag, xlab = "Angular Magnitude", ylab = "Jerk Magnitude", main = "Angular Magnitude vs. Jerk Magnitude Plot")
plot(robot_data$angular_mag, robot_data$jmag, xlab = "Angular Magnitude", ylab = "Jerk Magnitude", log='xy', main = "Angular Magnitude vs. Jerk Magnitude Log Plot")

boxplot(formula = jmag ~ Environment, data = robot_data, main = "Box Plot of Jerk Magnitude by Environment", xlab = "Environment", ylab = "Jerk Magnitude")

uniangularmodel <- lm(log(jmag) ~ log(angular_mag), data=robot_data)
unienvironmentmodel <- lm(log(jmag) ~ Environment, data=robot_data)
summary(uniangularmodel)
summary(unienvironmentmodel)

model <- lm(log(jmag) ~ log(angular_mag) + Environment + log(angular_mag):Environment, data = robot_data)   
summary(model)
anova(model)

plot(model, 4, id.n = 5, sub.caption = "Interactive Comprehensive Model")
outliers <- which(cooks.distance(model) > 4/length(model$fitted.values))
length(outliers)
clean_data <- robot_data[-outliers, ]
model_clean <- lm(formula(model), data = clean_data)

summary(model_clean)
anova(model_clean)

#Take another look at our univariate models with clean data.

clean_uniangularmodel <- lm(log(jmag) ~ log(angular_mag), data=clean_data)
clean_unienvironmentmodel <- lm(log(jmag) ~ Environment, data=clean_data)
summary(clean_uniangularmodel)
summary(clean_unienvironmentmodel)

plot(model_clean$fitted.values, residuals(model_clean),
    xlab = "Predicted Values",
    ylab = "Residuals",
    main = "Residuals Plot")
lines(lowess(model_clean$fitted.values, residuals(model_clean)), col = "red", lwd = 2)
abline(h = 0, col="blue", lty=2)

Residuals <- residuals(model_clean)
hist(Residuals, breaks = 30, xlab = "Residuals")

qqnorm(residuals(model_clean))
qqline(residuals(model_clean), col = "red")
vif(model_clean)

model_reduced <- lm(log(jmag) ~ log(angular_mag) + Environment, data = clean_data)

AIC(model_clean, model_reduced)
BIC(model_clean, model_reduced)

#AIC and BIC of full model is significantly better.

rmse <- sqrt(mean(residuals(model_clean)^2))
rmse