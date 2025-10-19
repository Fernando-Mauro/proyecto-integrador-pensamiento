#json
import json
import os
def write(score, name, filename='scores.json'):
    # Check if the file exists
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    # Update the score if the name exists and the new score is higher
    if name in data:
        if score > data[name]:
            data[name] = score
    else:
        data[name] = score

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def read(filename='scores.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            # Sort the data by score in descending order
            sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
            return sorted_data
    return {}
