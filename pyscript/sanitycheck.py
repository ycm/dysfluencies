import sys, os, json

with open('20190713_categories_updated.json') as f:
    category_to_line = json.load(f)

print(sum([len(v) for k, v in category_to_line.items()]))