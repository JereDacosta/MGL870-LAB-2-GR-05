import pandas as pd

# Load the parsed logs CSV file
df = pd.read_csv('parsed-openstack-logs.csv')

# List of VM IDs with anomalies
anomalous_vms = [
    "544fd51c-4edc-4780-baae-ba1d80a0acfc",
    "ae651dff-c7ad-43d6-ac96-bbcd820ccca8",
    "a445709b-6ad0-40ec-8860-bec60b6ca0c2",
    "1643649d-2f42-4303-bfcd-7798baec19f9"
]

# Filter the logs for those containing any of the anomalous VM IDs
abnormal_logs = df[df['Content'].str.contains('|'.join(anomalous_vms))]

# Extract unique Cluster IDs of the abnormal logs
unique_cluster_ids = sorted(abnormal_logs['Cluster ID'].unique())

# Write the unique Cluster IDs to a .txt file
with open("abnormal_cluster_ids.txt", "w") as file:
    for cluster_id in unique_cluster_ids:
        file.write(f"{cluster_id}\n")

print("Unique Cluster IDs of abnormal logs written to abnormal_cluster_ids.txt")
