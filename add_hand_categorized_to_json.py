import sys, os, json

with open('new_categories.cpy.json') as f:
    category_to_line = json.load(f)

with open('category_keys.json') as f:
    category_to_key = {
        int(k): v 
        for k, v in json.load(f).items()
    }

with open('residue_to_category.json') as f:
    residue_to_category = json.load(f)


residue = []
for ln, category_idx in residue_to_category.items():
    if category_idx:
        category = category_to_key[category_idx]
        try:
            category_to_line[category].append(ln)
        except KeyError:
            category_to_line[category] = [ln]
    else:
        residue.append(ln)

with open('20190713_residue.json', 'w') as f:
    json.dump(residue, f, indent=4)

with open('20190713_categories_updated.json', 'w') as f:
    json.dump(category_to_line, f, indent=4)