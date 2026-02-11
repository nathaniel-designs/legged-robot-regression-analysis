# legged-robot-regression-analysis

Currently, legged robots often struggle the most with remaining bal-
anced in unpredictable real-world environments. This study builds upon
the new advancements in custom odometry for the Unitree Go1 robot that
has been developed to combat the unreliable sensor data that can impact
a legged robot’s stability. Particularly, regression models for jerk magni-
tude were used to try to represent and predict instability based on
the magnitude of the angular velocity and the environment the robot was
in, using the recorded data from Ou’s improved robot. Due to the limita-
tions in the linear regression techniques, several machine learning models
were introduced to take nonlinear relationships into account, with Ran-
dom Forest (RF) attaining a multiple R2 value of approximately 0.376.
Therefore, more diverse sensor data is needed to make stronger predic-
tions. Nonetheless, the model successfully predicts a correlation between
robot motion and instability indicators.
