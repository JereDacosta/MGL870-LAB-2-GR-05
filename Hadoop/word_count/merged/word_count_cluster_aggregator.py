import pandas as pd

df = pd.read_csv('parsed-word-count-merged.csv')

df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df = df.sort_values(by='Datetime')

def split_and_aggregate_by_cluster(df, time_interval, error_threshold, anomaly_clusters):
    df.set_index('Datetime', inplace=True)

    cluster_counts = df.groupby([pd.Grouper(freq=time_interval), 'Cluster ID']).size().unstack(fill_value=0)
    cluster_counts['Anomaly'] = '0'

    for index, row in cluster_counts.iterrows():
        if anomaly_clusters:
            if row[anomaly_clusters].sum() >= error_threshold:
                cluster_counts.at[index, 'Anomaly'] = '1'
        else:
            if row.sum() >= error_threshold:
                cluster_counts.at[index, 'Anomaly'] = '1'

    if anomaly_clusters:
        cluster_counts.drop(columns=anomaly_clusters, inplace=True)

    return cluster_counts

time_interval = '3T'  # fixed windows of 1 minute intervals
anomaly_clusters = [243, 249, 252, 261, 262, 267, 90, 92, 110, 182, 184, 216, 218, 233, 244, 246, 247, 250, 259, 263, 270]  # anomalous cluster IDs
error_threshold = 1  # max number or error before labeling as an anomaly chunk

result_df = split_and_aggregate_by_cluster(df, time_interval, error_threshold, anomaly_clusters)
result_df.reset_index(inplace=True)

result_df.to_csv('parsed-word-count-aggregated.csv', index=False)
