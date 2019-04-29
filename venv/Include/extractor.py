
f = open('BOSCH_HACKATHON/Data.txt', "r+")

for line in reversed(list(f)):
    print(line.rstrip())