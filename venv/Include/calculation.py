import re

def strike_rate(runs_scored, balls_faced):
    return "%.2f" % (( runs_scored / balls_faced ) * 100)


def economy(runs_conceded, overs_balled):
    return "%.2f" % ( runs_conceded / overs_balled )


def extract_ball_speeds():
    # Finding all the ball speeds
    f = open('BOSCH_HACKATHON/Data.txt', "r+").read()
    print(f)
    bowling_speeds = re.findall(pattern="[0-9]+[.][0-9]+km/h", string=f)
    print(bowling_speeds)
    m = max(bowling_speeds)
    print(m)

    f = f.split('\n')
    for i in f:
        if str(m) in i:
            return i


# Tests
print(strike_rate(85, 53))
print(economy(31, 4))
print(extract_ball_speeds())





