import subprocess
import hashlib
import json
import os

# Function to run dnstwist on a domain
def run_dnstwist(domain):
    cmd = f'dnstwist -f json {domain}'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout

# Function to load previous run data
def load_previous_data():
    if os.path.exists('previous_data.json'):
        with open('previous_data.json', 'r') as file:
            return json.load(file)
    else:
        return {}

# Function to save current run data
def save_current_data(data):
    with open('previous_data.json', 'w') as file:
        json.dump(data, file, indent=4)

# Function to compare current run data with previous run data
def compare_results(current_data, previous_data):
    changes = []
    for domain, current_info in current_data.items():
        previous_info = previous_data.get(domain)
        if not previous_info or current_info != previous_info:
            changes.append((domain, current_info))
    return changes

# List of domains to check
domains = ["accentcinti.com", "abdeburr.com", "cmitcincy.com"]

# Load previous run data
previous_data = load_previous_data()

# Dictionary to store current run data
current_data = {}

# Run dnstwist for each domain and store the output
for domain in domains:
    result = run_dnstwist(domain)
    current_data[domain] = hashlib.sha256(result.encode()).hexdigest()

# Compare current run data with previous run data
changes = compare_results(current_data, previous_data)

# Notify if changes are detected
if changes:
    print("Changes detected:")
    for domain, info in changes:
        print(f"Domain: {domain}")
        print(f"Info: {info}")
else:
    print("No changes detected")

# Save current run data for future comparison
save_current_data(current_data)
