import json

with open(".\\config\\headers.json", "r", encoding="utf-8-sig") as f:
    transit_times = json.load(f)
    new_headers = {}
    for key, value in transit_times.items():
        new_headers[key] = {}
        for header_key, header_value in value.items():
            new_headers[key].update({header_value: header_key})

with open(".\\config\\headers.json", "w", encoding="utf-8-sig") as f:
    json.dump(new_headers, f, indent=4)
