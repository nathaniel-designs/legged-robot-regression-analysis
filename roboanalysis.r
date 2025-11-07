#install.packages("readr")
library(readr)

robot_data <- read_csv("robot_dataset.csv")

#Translation note:
#X = left-right, Y = forward-backward
head(robot_data, 10)
summary(robot_data)

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

plot(robot_data$angular_mag, robot_data$jmag, xlab = "Angular Magnitude", ylab = "Jerk Magnitude")
plot(robot_data$angular_mag, robot_data$jmag, xlab = "Angular Magnitude", ylab = "Jerk Magnitude", log='xy')

model <- lm((robot_data$jmag) ~ robot_data$angular_mag + robot_data$Environment + (robot_data$angular_mag * robot_data$Environment))
summary(model)
anova(model)

plot(model$fitted.values, residuals(model), xlab = "Predicted Values", ylab = "Residuals",)
Residuals <- residuals(model)
hist(Residuals, breaks = 30, xlab = "Residuals")