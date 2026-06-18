#install.packages("readr")
library(readr)
library(car)


robot_data <- read_csv("robot_dataset_final.csv")

#Translation note:
#X = left-right, Y = forward-backward
head(robot_data, 10)
summary(robot_data)
colSums(is.na(robot_data))
#No missing data! 

avg_footforce <- mean(robot_data$footforce)
median_footforce <- median(robot_data$footforce)
stddev_footforce <- sd(robot_data$footforce)
min_footforce <- min(robot_data$footforce, na.rm = TRUE)
max_footforce <- max(robot_data$footforce, na.rm = TRUE)
range_footforce <- max_footforce-min_footforce

avg_d_footforce_dt <- mean(robot_data$d_footforce_dt)
median_d_footforce_dt<- median(robot_data$d_footforce_dt)
stddev_d_footforce_dt <- sd(robot_data$d_footforce_dt)
min_d_footforce_dt <- min(robot_data$d_footforce_dt, na.rm = TRUE)
max_d_footforce_dt <- max(robot_data$d_footforce_dt, na.rm = TRUE)
range_d_footforce_dt <- max_d_footforce_dt-min_d_footforce_dt

avg_torque <- mean(robot_data$total_torque)
median_torque <- median(robot_data$total_torque)
stddev_torque <- sd(robot_data$total_torque)
min_torque <- min(robot_data$total_torque, na.rm = TRUE)
max_torque <- max(robot_data$total_torque, na.rm = TRUE)
range_torque <- max_torque-min_torque

data_exploration_df <- data.frame(
  Statistic = c("Mean", "Median", "Std Dev", "Min", "Max", "Range"),
  FootForce = c(avg_footforce, median_footforce, stddev_footforce, min_footforce, max_footforce, range_footforce),
  dFootForce_dt = c(avg_d_footforce_dt, median_d_footforce_dt, stddev_d_footforce_dt, min_d_footforce_dt, max_d_footforce_dt, range_d_footforce_dt),
  Torque = c(avg_torque, median_torque, stddev_torque, min_torque, max_torque, range_torque)
)

print(data_exploration_df)
robot_data$environment <- as.factor(robot_data$environment)
levels(robot_data$environment)

robot_data$log_abs_dfootforce <- log(abs(robot_data$d_footforce_dt) + 1)

sum(robot_data$d_footforce_dt > 0)
sum(robot_data$d_footforce_dt < 0)

#Our results are significantly different if we only look at positive values of the derivative, so we will analyze this subset separately.
positive_data <- subset(robot_data, d_footforce_dt > 0)

hist(robot_data$footforce, main = "Histogram of Foot Force")
hist(robot_data$d_footforce_dt, main = "Histogram of Foot Force Derivative")
hist(robot_data$total_torque, main = "Histogram of Torque")

hist(log(robot_data$footforce), main = "Histogram of Log-Transformed Foot Force")
hist(robot_data$log_abs_dfootforce, main = "Log(|dFootForce/dt| + 1)")
hist(log(robot_data$total_torque), main = "Histogram of Log-Transformed Torque")

plot(robot_data$footforce, robot_data$total_torque, xlab = "Foot Force", ylab = "Jerk Magnitude", main = "Foot Force vs. Torque Plot")
plot(robot_data$footforce, robot_data$total_torque, xlab = "Foot Force", ylab = "Jerk Magnitude", log='xy', main = "Foot Force vs. Torque Log Plot")

plot(robot_data$d_footforce_dt, robot_data$total_torque, xlab = "Foot Force Derivative", ylab = "Torque", main = "Foot Force Derivative vs. Torque Plot")
plot(positive_data$d_footforce_dt, positive_data$total_torque, xlab = "Foot Force Derivative", ylab = "Torque", log='xy', main = "Foot Force Derivative vs. Torque Log Plot")

boxplot(formula = total_torque ~ environment, data = robot_data, main = "Box Plot of Torque by Environment", xlab = "Environment", ylab = "Torque")

unifootforcemodel <- lm(log(total_torque) ~ log(footforce), data=robot_data)
unifootforcederivativemodel <- lm(log(total_torque) ~ log(d_footforce_dt), data=robot_data)
unienvironmentmodel <- lm(log(total_torque) ~ environment, data=robot_data)
summary(unifootforcemodel)
summary(unifootforcederivativemodel)
summary(unienvironmentmodel)





#log(d_footforce_dt) restricts analysis to positive derivative observations.
model1 <- lm(log(total_torque) ~ log(footforce) + environment + log(footforce):environment, data = robot_data)   
summary(model1)
anova(model1)

model2 <- lm(log(total_torque) ~ log(d_footforce_dt) + environment + log(d_footforce_dt):environment, data = robot_data)
summary(model2)
anova(model2)

model3 <- lm(log(total_torque) ~ log(footforce) + log(d_footforce_dt) + environment + log(footforce):environment + log(d_footforce_dt):environment, data = robot_data)
summary(model3)
anova(model3)

#Full-data exploratory regression (includes negative derivatives)
model_final_candidate <- lm(log(total_torque) ~ log(footforce) + log_abs_dfootforce + environment + log(footforce):environment + log_abs_dfootforce:environment, data = robot_data)
summary(model_final_candidate)
anova(model_final_candidate)

#Final modeling restricted to loading phase (positive derivatives)
model_positive <- lm(log(total_torque) ~ log(footforce) + log(d_footforce_dt) + environment + log(footforce):environment + log(d_footforce_dt):environment, data = positive_data)

summary(model_positive)
anova(model_positive)

plot(model_positive, 4, id.n = 5, sub.caption = "Interactive Comprehensive Model")
outliers <- which(cooks.distance(model_positive) > 4/length(model_positive$fitted.values))
length(outliers)
clean_data <- positive_data[-outliers, ]
model_clean <- lm(formula(model_positive), data = clean_data)

summary(model_clean)
anova(model_clean)

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

model_reduced <- lm(
  log(total_torque) ~
  log(footforce) +
  log(d_footforce_dt) +
  environment,
  data = clean_data
)

AIC(model_clean, model_reduced)
BIC(model_clean, model_reduced)

#AIC and BIC of full model is significantly better.

rmse <- sqrt(mean(residuals(model_clean)^2))
rmse

pred <- fitted(model_clean)
actual <- log(clean_data$total_torque)

plot(pred, actual,
     xlab = "Predicted log(Torque)",
     ylab = "Observed log(Torque)",
     main = "Observed vs Predicted (Linear Regression)")

abline(0, 1, col = "red", lwd = 2)