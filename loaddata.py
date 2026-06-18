import pandas as pd

environment_files = ['corridor/corridor_model_data.csv', 'indoor/indoor_model_data.csv', 'parking/parking_model_data.csv', 'running/running_model_data.csv']

file_list = [pd.read_csv(file) for file in environment_files]

combined_data = pd.concat(file_list, ignore_index=True)

combined_data.to_csv('robot_dataset_final.csv', index=False)