import pandas as pd

def find_anomalies_in_logs(file_path, fatal_level='FATAL', exception_keyword='exception'):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Initialize an empty list for unique cluster IDs
    anomaly_cluster_ids = []

    # Flag to indicate if anomalies were found
    contains_anomaly = False

    # Filter for rows with log level "FATAL"
    fatal_logs = df[df['Level'].str.upper() == fatal_level.upper()]

    # Filter for rows where 'Content' contains "exception"
    exception_logs = df[df['Content'].str.contains(exception_keyword, case=False, na=False)]

    # Combine both fatal and exception logs without duplicates
    anomaly_logs = pd.concat([fatal_logs, exception_logs]).drop_duplicates()

    # If there are any anomalies, set the flag to True and extract unique Cluster IDs
    if not anomaly_logs.empty:
        contains_anomaly = True
        anomaly_cluster_ids = anomaly_logs['Cluster ID'].unique().tolist()

    return anomaly_cluster_ids, contains_anomaly

def save_cluster_ids(cluster_ids, output_file):
    # Write unique cluster IDs to output file
    with open(output_file, 'w') as file:
        for cluster_id in cluster_ids:
            file.write(f"{cluster_id}\n")

# File paths and settings
file_path = 'parsed-word-count-merged.csv'
output_file = 'anomaly_cluster_ids.txt'

# Find anomalies and write the cluster IDs to a file
cluster_ids, has_anomalies = find_anomalies_in_logs(file_path)
save_cluster_ids(cluster_ids, output_file)

print(f"Cluster IDs have been written to '{output_file}'.")
print(f"Anomalies detected: {has_anomalies}")
