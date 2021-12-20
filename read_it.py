import json

def convert_readable(filename):
    print(filename) 
    with open(filename) as f:
        all_data = json.load(f)
    
    readable_file = 'temp.json'
    
    with open(readable_file, 'w') as f:
        json.dump(all_data, f, indent=4)
