from pathlib import Path
import pickle
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
import re
import pandas as pd

config = TemplateMinerConfig()
drain_parser = TemplateMiner(config=config)

log_pattern = re.compile(
    r"(?P<LogFile>[\w-]+\.log\.\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2})\s"
    r"(?P<Date>\d{4}-\d{2}-\d{2})\s"
    r"(?P<Time>\d{2}:\d{2}:\d{2}\.\d+)\s"
    r"(?P<PID>\d+)\s"
    r"(?P<Level>\w+)\s"
    r"(?P<Component>[^\[]+)\s"
    r"\[(?P<RequestID>[^\]]+)\]\s"
    r"(?P<Content>.*)"
)

log_file_path = Path("W:/ETS/MLG870/TP2/os-abnormal.log")

with open(log_file_path, 'r') as log_file:
    for line in log_file:
        line = line.strip()
        match = log_pattern.match(line)
        if match:
            log_content = match.group("Content")  
            result = drain_parser.add_log_message(log_content)

log_data = []
with open(log_file_path, 'r') as log_file:
    for log in log_file:
        match = log_pattern.match(log)
        if match:
            log_file_name = match.group("LogFile")
            date = match.group("Date")
            time = match.group("Time")
            pid = match.group("PID")
            level = match.group("Level")
            component = match.group("Component").strip()
            request_id = match.group("RequestID")
            log_content = match.group("Content")

            result = drain_parser.match(log_content)

            log_entry = {
                "LogFile": log_file_name,
                "Date": date,
                "Time": time,
                "PID": pid,
                "Level": level,
                "Component": component,
                "RequestID": request_id,
                "Content": log_content,
                "Matched Template": result.get_template(),
                "Cluster ID": result.cluster_id
            }
            
            log_data.append(log_entry)

df = pd.DataFrame(log_data)
df.to_csv('parsed-openstack-logs.csv', index=False)

print("Parsed logs saved to parsed-openstack-logs.csv")
