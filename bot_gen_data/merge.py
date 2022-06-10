import sys, json

file1 = open(sys.argv[1], "r")
file2 = open(sys.argv[2], "r")

dataest1 = file1.readlines()
dataest2 = file2.readlines()

merged_file = open('merged.json', "w")

for ds in [dataest1, dataest2]:
    for s in ds:
        d = json.loads(s)
        print(json.dumps(d), file=merged_file)

