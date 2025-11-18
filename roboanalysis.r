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

hist(robot_data$angular_mag)
hist(robot_data$jmag)

hist(log(robot_data$angular_mag))
hist(log(robot_data$jmag))

plot(robot_data$angular_mag, robot_data$jmag, xlab = "Angular Magnitude", ylab = "Jerk Magnitude")
plot(robot_data$angular_mag, robot_data$jmag, xlab = "Angular Magnitude", ylab = "Jerk Magnitude", log='xy')

boxplot(formula = jmag ~ Environment, data = robot_data, main = "Box Plot of Jerk Magnitude by Environment", xlab = "Environment", ylab = "Jerk Magnitude")

model <- lm(log(jmag) ~ log(angular_mag) + Environment + log(angular_mag):Environment, data = robot_data)   
summary(model)
anova(model)

plot(model$fitted.values, residuals(model), xlab = "Predicted Values", ylab = "Residuals",)
Residuals <- residuals(model)
hist(Residuals, breaks = 30, xlab = "Residuals")

qqnorm(residuals(model))
qqline(residuals(model), col = "red")
vif(model)
plot(model, 4, id.n = 5)
which(cooks.distance(model) > 4/length(model$fitted.values))

model_reduced <- lm(log(jmag) ~ log(angular_mag) + Environment, data = robot_data)

AIC(model, model_reduced)
BIC(model, model_reduced)