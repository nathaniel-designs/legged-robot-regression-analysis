import pandas as pd

environment_instability_df = ['environments/corridor/corridor_instability.csv', 'environments/grass/grass_instability.csv', 'environments/indoor/indoor_instability.csv', 'environments/parking/parking_instability.csv', 'environments/running/running_instability.csv']

instability_list = []

for file in environment_instability_df:
    temp = pd.read_csv(file)
    temp['environment'] = file.split("/")[1]
    instability_list.append(temp)

combined_instability = pd.concat(instability_list, ignore_index=True)
combined_instability.to_csv('robot_instability_dataset.csv', index=False)

for file in environment_instability_df:
    temp = pd.read_csv(file)
    print(file)
    print(temp["instability_index"].describe())
    print()
    
print((combined_instability["instability_index"] > 1).groupby(combined_instability["environment"]).sum())