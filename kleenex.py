import json

with open(".\\config\\headers.json", "r", encoding="utf-8-sig") as f:
    curr_headers = json.load(f)

with open(".\\config\\data_types.json", "r", encoding="utf-8-sig") as f:
    new_headers = json.load(f)

headers_2 = {}
for file_type, headers in curr_headers.items():
    headers_2.update({file_type: {}})
    for header in headers.keys():
        if header in new_headers.get(file_type, {}):
            headers[header] = new_headers[file_type][header]

with open(".\\config\\headers2.json", "w", encoding="utf-8-sig") as f:
    json.dump(curr_headers, f, indent=4)
