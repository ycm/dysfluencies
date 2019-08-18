import sys, json
with open(sys.argv[1]) as f:
    with open(sys.argv[2], 'w') as o_f:
        json.dump(json.load(f), o_f, indent=4)
