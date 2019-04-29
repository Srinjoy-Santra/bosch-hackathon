import re

def strike_rate(runs_scored, balls_faced):
    return "%.2f" % (( runs_scored / balls_faced ) * 100)


def economy(runs_conceded, overs_balled):
    return "%.2f" % ( runs_conceded / overs_balled )


def extract_six_length(line):
    print(re.search(pattern=r"[0-9]{+}\.[0-9]km/h",string=line))


# Tests
print(strike_rate(85, 53))
print(economy(31, 4))
print(extract_six_length("Prasidh to Agarwal, no run, slower one, short of length wide outside off, 104.8km/h (Jadeja bowled"))

# Finding all the ball speeds
f = open('BOSCH_HACKATHON/Data.txt', "r+").read()
print(f)
bowling_speeds = re.findall(pattern="[0-9]+[.][0-9]+km/h", string=f)
print(bowling_speeds)
print(max(bowling_speeds))


