
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
import re
import pandas as pd

config = TemplateMinerConfig()

# Step 1: Train Drain model on training log data
drain_parser = TemplateMiner(config=config)

# Updated log pattern with Content capture
log_pattern = re.compile(
    r"(?P<Date>\d{4}-\d{2}-\d{2})\s"  # Date (e.g., 2015-10-17)
    r"(?P<Time>\d{2}:\d{2}:\d{2},\d{3})\s"  # Time (e.g., 21:24:12,647)
    r"(?P<Level>\w+)\s"  # Log level (e.g., INFO)
    r"\[(?P<Thread>[^\]]+)\]\s"  # Thread name (e.g., AsyncDispatcher event handler)
    r"(?P<Class>[^\s]+)\s"  # Class/Logger name (e.g., org.apache.hadoop.mapreduce.v2.app.job.impl.TaskImpl)
    r"(?P<Content>.*)"  # Content (e.g., task_1445087491445_0001_m_000006 Task Transitioned from NEW to SCHEDULED)
)

with open('word_count_merged.log', 'r') as log_file:
    for line in log_file:
        # Remove any leading/trailing whitespace from the line
        line = line.strip()
        match = log_pattern.match(line)
        if match:
            log_content = match.group("Content")  # Extract the Content field
            result = drain_parser.add_log_message(log_content)

log_data = []

with open('word_count_merged.log', 'r') as log_file:
    for line in log_file:
        line = line.strip()  # Remove leading/trailing whitespace
        match = log_pattern.match(line)

        # Debugging: print out matched groups
        if match:
            log_content = match.group("Content")
            date = match.group("Date")
            time = match.group("Time")
            level = match.group("Level")
            thread = match.group("Thread")
            class_name = match.group("Class")

            # Match the log content with Drain to find the associated template
            result = drain_parser.match(log_content)

            # Check if the result is None
            if result is None:
                print(f"No match found for content: {log_content}")
                # Optionally, assign default values or skip this entry
                matched_template = "Unknown"
                cluster_id = "Unknown"
            else:
                matched_template = result.get_template()
                cluster_id = result.cluster_id

            # Create log entry
            log_entry = {
                "Date": date,
                "Time": time,
                "Level": level,
                "Thread": thread,
                "Class": class_name,
                "Content": log_content,
                "Matched Template": matched_template,
                "Cluster ID": cluster_id
            }

            # Append the dictionary to the list
            log_data.append(log_entry)
        else:
            print(f"Unmatched line: {line}")

# If no data was found, print a message
if not log_data:
    print("No log data was processed. Please check the log pattern and log file content.")

# Convert the list of log entries into a DataFrame and save to a CSV file
if log_data:
    df = pd.DataFrame(log_data)
    df.to_csv('parsed-word-count-merged.csv', index=False)
    print("Log data has been parsed and saved to 'parsed-word-count-merged.csv'.")