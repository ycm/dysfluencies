import sys, os, json

with open('uncategorized_lines.json') as f:
    residual_lines = json.load(f)

with open('new_categories.cpy.json') as f:
    categories = json.load(f)

num_to_category = {
    idx + 1: category
    for idx, category in enumerate(sorted(list(categories.keys())))
}

prompt = 'Categories:\n'
for k, v in list(num_to_category.items()):
    prompt += str(k) + ' ' + str(v) + '\n'

line_to_categories = {}
for line in residual_lines: 
    print(prompt)
    print(line)
    print()
    num = input('> ')
    if not num: line_to_categories[line] = 0
    else: line_to_categories[line] = int(num)

with open('residue_to_category.json', 'w') as f:
    json.dump(line_to_categories, f, indent=4)

with open('category_keys.json', 'w') as f:
    json.dump(num_to_category, f, indent=4)
