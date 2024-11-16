import pandas as pd

df = pd.read_csv('parsed-word-count-merged.csv')

df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df = df.sort_values(by='Datetime')

def split_and_aggregate_by_cluster(df, time_interval, error_threshold, anomaly_clusters):
    """
    Splits the DataFrame into time chunks and counts occurrences of each Cluster ID in each chunk.
    Adds an 'Anomaly' column based on the frequency of certain 'Cluster ID's or log levels.

    :param df: The DataFrame containing log data.
    :param time_interval: The frequency for splitting (e.g., '30T' for 30 minutes).
    :param error_threshold: The number of certain clusters that triggers the anomaly label.
    :param anomaly_clusters: A list of Cluster IDs that are considered anomalous.
    :return: A new DataFrame where each row is a time chunk and each column is a Cluster ID count,
             along with an 'Anomaly' label column.
    """

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

time_interval = '1T'  # fixed windows of 1 minute intervals
anomaly_clusters = [243, 249, 252, 261, 262, 267, 90, 92, 110, 182, 184, 216, 218, 233, 244, 246, 247, 250, 259, 263, 270]  # anomalous cluster IDs
error_threshold = 3  # max number or error before labeling as an anomaly chunk

result_df = split_and_aggregate_by_cluster(df, time_interval, error_threshold, anomaly_clusters)
result_df.reset_index(inplace=True)

result_df.to_csv('parsed-word-count-aggregated.csv', index=False)