#install.packages("readr")
library(readr)
library(car)

#analyze_data <- function(input_file, output_file){

analyze_data <- function(input_file){
  robot_data <- read_csv(input_file)
  #Translation note:
  #X = left-right, Y = forward-backward
  head(robot_data, 10)
  summary(robot_data)
  colSums(is.na(robot_data))
  #No missing data! 

  avg_velocity <- mean(robot_data$velocity)
  median_velocity <- median(robot_data$velocity)
  stddev_velocity <- sd(robot_data$velocity)
  min_velocity <- min(robot_data$velocity, na.rm = TRUE)
  max_velocity <- max(robot_data$velocity, na.rm = TRUE)
  range_velocity <- max_velocity-min_velocity

  avg_roll <- mean(robot_data$roll)
  median_roll<- median(robot_data$roll)
  stddev_roll <- sd(robot_data$roll)
  min_roll <- min(robot_data$roll, na.rm = TRUE)
  max_roll <- max(robot_data$roll, na.rm = TRUE)
  range_roll <- max_roll-min_roll

  avg_pitch <- mean(robot_data$pitch)
  median_pitch<- median(robot_data$pitch)
  stddev_pitch <- sd(robot_data$pitch)
  min_pitch <- min(robot_data$pitch, na.rm = TRUE)
  max_pitch <- max(robot_data$pitch, na.rm = TRUE)
  range_pitch <- max_pitch-min_pitch

  avg_instability <- mean(robot_data$instability_index)
  median_instability <- median(robot_data$instability_index)
  stddev_instability <- sd(robot_data$instability_index)
  min_instability <- min(robot_data$instability_index, na.rm = TRUE)
  max_instability <- max(robot_data$instability_index, na.rm = TRUE)
  range_instability <- max_instability-min_instability

  data_exploration_df <- data.frame(
    Statistic = c("Mean", "Median", "Std Dev", "Min", "Max", "Range"),
    Velocity = c(avg_velocity, median_velocity, stddev_velocity, min_velocity, max_velocity, range_velocity),
    Roll = c(avg_roll, median_roll, stddev_roll, min_roll, max_roll, range_roll),
    Pitch = c(avg_pitch, median_pitch, stddev_pitch, min_pitch, max_pitch, range_pitch),
    Instability = c(avg_instability, median_instability, stddev_instability, min_instability, max_instability, range_instability)
  )

  print(data_exploration_df)
  robot_data$environment <- as.factor(robot_data$environment)
  levels(robot_data$environment)

  #robot_data$log_abs_dfootforce <- log(abs(robot_data$d_footforce_dt) + 1)

  #Our results are significantly different if we only look at positive values of the derivative, so we will analyze this subset separately.
  #positive_data <- subset(robot_data, d_footforce_dt > 0)

  hist(robot_data$velocity, main = "Histogram of Velocity")
  hist(robot_data$roll, main = "Histogram of Roll")
  hist(robot_data$pitch, main = "Histogram of Pitch")
  hist(robot_data$instability_index, main = "Histogram of Instability Index")

  hist(log(robot_data$velocity), main = "Histogram of Log-Transformed Velocity")
  hist(log(robot_data$roll), main = "Histogram of Log-Transformed Roll")
  hist(log(robot_data$pitch), main = "Histogram of Log-Transformed Pitch")
  hist(log(robot_data$instability_index), main = "Histogram of Log-Transformed Instability Index")

  log_instability <- log(robot_data$instability_index / (1 - robot_data$instability_index))

  hist(log_instability, main = "Histogram of Logit Instability Index")

  plot(robot_data$velocity, robot_data$instability_index, xlab = "Velocity", ylab = "Instability", main = "Velocity vs. Instability")
  plot(robot_data$velocity, log_instability, xlab = "Velocity", ylab = "Instability", main = "Velocity vs. Logit Instability Log Plot")

  plot(robot_data$roll, robot_data$instability_index, xlab = "Roll", ylab = "Instability", main = "Roll vs. Instability Plot")
  plot(robot_data$roll, log_instability, xlab = "Roll", ylab = "Instability", main = "Roll vs. Logit Instability Log Plot")

  plot(robot_data$pitch, robot_data$instability_index, xlab = "Pitch", ylab = "Instability", main = "Pitch vs. Instability Plot")
  plot(robot_data$pitch, log_instability, xlab = "Pitch", ylab = "Instability", main = "Pitch vs. Logit Instability Log Plot")

  boxplot(formula = instability_index ~ environment, data = robot_data, main = "Box Plot of Instability by Environment", xlab = "Environment", ylab = "Instability")
  boxplot(formula = log_instability ~ environment, data = robot_data, main = "Box Plot of Logit Instability by Environment", xlab = "Environment", ylab = " Instability")

  #unifootforcemodel <- lm(log(total_torque) ~ log(footforce), data=robot_data)
  #unifootforcederivativemodel <- lm(log(total_torque) ~ log(d_footforce_dt), data=robot_data)
  #unienvironmentmodel <- lm(log(total_torque) ~ environment, data=robot_data)
  #summary(unifootforcemodel)
  #summary(unifootforcederivativemodel)
  #summary(unienvironmentmodel)

  #log(d_footforce_dt) restricts analysis to positive derivative observations.
  #model1 <- lm(log(total_torque) ~ log(footforce) + environment + log(footforce):environment, data = robot_data)   
  #summary(model1)
  #anova(model1)

  #model2 <- lm(log(total_torque) ~ log(d_footforce_dt) + environment + log(d_footforce_dt):environment, data = robot_data)
  #summary(model2)
  #anova(model2)

  #model3 <- lm(log(total_torque) ~ log(footforce) + log(d_footforce_dt) + environment + log(footforce):environment + log(d_footforce_dt):environment, data = robot_data)
  #summary(model3)
  #anova(model3)

  #Full-data exploratory regression (includes negative derivatives)
  #model_final_candidate <- lm(log(total_torque) ~ log(footforce) + log_abs_dfootforce + environment + log(footforce):environment + log_abs_dfootforce:environment, data = robot_data)
  #summary(model_final_candidate)
  #anova(model_final_candidate)

  #Final modeling restricted to loading phase (positive derivatives)
  #model_positive <- lm(log(total_torque) ~ log(footforce) + log(d_footforce_dt) + environment + log(footforce):environment + log(d_footforce_dt):environment, data = positive_data)

  #summary(model_positive)
  #anova(model_positive)

  #plot(model_positive, 4, id.n = 5, sub.caption = "Interactive Comprehensive Model")
  #outliers <- which(cooks.distance(model_positive) > 4/length(model_positive$fitted.values))
  #length(outliers)
  #clean_data <- positive_data[-outliers, ]
  #model_clean <- lm(formula(model_positive), data = clean_data)

  #summary(model_clean)
  #anova(model_clean)

  #plot(model_clean$fitted.values, residuals(model_clean),
      #xlab = "Predicted Values",
      #ylab = "Residuals",
      #main = "Residuals Plot")
  #lines(lowess(model_clean$fitted.values, residuals(model_clean)), col = "red", lwd = 2)
  #abline(h = 0, col="blue", lty=2)

  #Residuals <- residuals(model_clean)
  #hist(Residuals, breaks = 30, xlab = "Residuals")

  #qqnorm(residuals(model_clean))
  #qqline(residuals(model_clean), col = "red")
  #vif(model_clean)

  #model_reduced <- lm(
    #log(total_torque) ~
    #log(footforce) +
    #log(d_footforce_dt) +
    #environment,
    #data = clean_data
  #)

  #AIC(model_clean, model_reduced)
  #BIC(model_clean, model_reduced)

  #AIC and BIC of full model is significantly better.

  #pred <- fitted(model_clean)
  #actual <- log(clean_data$total_torque)

  #plot(pred, actual,
  #    xlab = "Predicted log(Torque)",
  #    ylab = "Observed log(Torque)",
  #    main = "Observed vs Predicted (Linear Regression)")

  #abline(0, 1, col = "red", lwd = 2)

  #summary(model_clean)
  #rmse <- sqrt(mean(residuals(model_clean)^2))
  #mae <- mean(abs(residuals(model_clean)))
  #rmse
  #mae
  #vif(model_clean)

  #Prevent it from scrambling the categorical variables.
  #clean_data$row_id <- seq_len(nrow(clean_data))

  #write.csv(clean_data, output_file, row.names = FALSE)

  #return (clean_data)
}

test <- analyze_data("robot_instability_dataset.csv")