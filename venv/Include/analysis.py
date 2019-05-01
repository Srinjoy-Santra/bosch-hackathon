import pandas as pd
import matplotlib.pyplot as plt
import re


def strike_rate(runs_scored, balls_faced):
    return "%.2f" % ((runs_scored / balls_faced) * 100)


def economy(runs_conceded, overs_balled):
    return "%.2f" % (runs_conceded / overs_balled)


def extract_ball_speeds():
    # Finding all the ball speeds
    f = open(r'BOSCH_HACKATHON/Data.txt', "r+").read()
    # print(f)
    bowling_speeds = re.findall(pattern="[0-9]+[.][0-9]+km/h", string=f)
    #print(bowling_speeds)
    m = max(bowling_speeds)
    #print(m)

    f = f.split('\n')
    for i in f:
        if str(m) in i:
            return [i.split(' ')[0], m]


def best_batsman(bdf):
    scores = dict()
    for bat in bdf.itertuples():
        score = float(bat[3])*0.5+float(bat[4])*0.5+bat[5]*1
        if bat[3] >= 100:
            score += 8
        elif bat[3] >= 50:
            score += 4
        scores[score] = bat.batsman

    m = max(list(scores.keys()))
    return [scores[m], m]


def best_bowler(bdf):
    scores = dict()
    for bal in bdf.itertuples():
        score = 0
        d = 0
        if bal[4] is not 0:
            if bal[4] is 4:
                d = 4
            elif bal[4] is 5:
                d = 8
            score += bal[4]*10+bal[2]*4 + d
        else:
            score += bal[2]*4
        scores[score] = bal.bowler
        
    m = max(list(scores.keys()))
    return [scores[m], m]


# Importing dataset
df = pd.read_csv('main.csv')

# Calculating the final score
total_runs = sum(df.run) + sum(df.wide)
no_of_wickets = 0
for verdict in df.out:
    if verdict is 'c' or verdict is 'b':
        no_of_wickets = no_of_wickets + 1
overs = len(df.bowler) / 6
if overs > 20:
    overs = 20

final_score = str(total_runs) + "-" + str(no_of_wickets) + " (" + str(overs) + ")"


def get_name(name):
    return {
        'rahul': 'Lokesh Rahul',
        'gayle': 'Chris Gayle',
        'agarwal': 'Mayank Agarwal',
        'sarfaraz khan': 'Sarfaraz Khan',
        'miller': 'David Miller',
        'mandeep': 'Mandeep Singh',
        'ferguson': 'Lockie Ferguson',
        'a russell': 'Andre Russell',
        'chawla': 'Piyush Chawla',
        'prasidh': 'Prasidh Krishna',
        'kuldeep yadav': 'Kuldeep Yadav',
        'narine': 'Sunil Narine'
    }.get(name, "IPL")


def name_to_url(name):
    return "https://en.wikipedia.org/wiki/" + name.replace(" ", '_')


# Fall of wickets calculation
score = 0
outs = 0
balls = 0
fall_of_wickets = ''
for row in df.itertuples():
    score = score + row.run
    # if row.wide is not 1 or  row.nb is not 1 or row.lb is not 1:
    balls = balls + 1
    if row.out is 'c' or row.out is 'b':
        outs = outs + 1
        # balls = list_action[row.Index]

        fow = str(score) + '-' + str(outs) + " (" + get_name(row.batsman.strip()) + ", " + str(balls // 6) + '.' + str(
            balls % 6) + "),"
        print(fow)
        fall_of_wickets = fow + fall_of_wickets

# Batsman Table
batsman_stat = pd.DataFrame(columns=['batsman', 'dismissal',
                                     'R', 'B', '4s', '6s', 'SR'])

batsmen = list(dict.fromkeys(df.batsman))
count = 0
for batsman in batsmen:
    nsixes = 0
    nfours = 0
    runs = 0
    balls = 0
    dismissal = 'not out'
    for row in df.itertuples():

        if batsman == row.batsman:
            # print([batsman,row.batsman])
            balls = balls + 1
            if row.out != 'not out':
                dismissal = row.out_by
                # print(row.out)
                break
            if row.run is 6:
                nsixes += 1
            elif row.run is 4:
                nfours += 1
            else:
                runs += row.run
                runs -= row.lb
                # runs += row.wide

    runs = runs + 4 * nfours + 6 * nsixes
    nrow = [get_name(batsman.strip()), dismissal, runs, balls, nfours, nsixes, strike_rate(runs, balls)]
    # print(nrow)
    batsman_stat.loc[len(batsman_stat)] = nrow
    count += 1

batsman_stat.to_csv('batsman_stat.csv', index=False)
print(batsman_stat)
best_batter = best_batsman(batsman_stat)
fastest_bowler = extract_ball_speeds()

runslist = []
wicketslist = []
ru = 0
for row in df.itertuples():
    ru += row.run
    runslist.append(ru)
    if row.out != 'not out':
        wicketslist.append(row.Index)

# Plot runs vs balls
plt.title('Progress of runs with each ball')
plt.xlabel('Runs')
plt.ylabel('Balls')
plt.plot(runslist, df.index)
plt.scatter([runslist[x] for x in wicketslist], wicketslist, c='red', label='dismissals')

plt.savefig('run_vs_ball.png')
plt.show()

####
'''  Bowling analysis Part   '''

bowl, overs, maiden, runs, wickets, NB, wides, eco = list(), list(), list(), list(), list(), list(), list(), list()
df2 = pd.DataFrame()

i, lis, ll = 0, list(), list()
lis.append(df.iloc[:, 2].values[0])

for i in df['bowler']:
    if i not in lis:
        lis.append(i)

for i in lis:
    counter = 0
    m = 0
    df2 = df.loc[df['bowler'] == i]
    bowl.append(get_name(i.strip()))
    overs.append(len(df2['bowler']) // 6)
    wides.append(sum(df2['wide']))
    NB.append(sum(df2['nb']))
    wickets.append(len(df2.loc[df2['out'] != 'not out']['out']))
    runs.append(sum(df2['run']) + sum(df2['wide']))

    eco.append(economy(sum(df2['run']) + sum(df2['wide']), len(df2['bowler']) // 6))
    h = int(df['over'].reshape(-1)[0])
    r = 0
    for j in df2['over']:
        # k=float(j)
        if int(j) != 0 and (j <= float(int(j) + 0.6)) and (h % int(j) == 0):
            r = r + df2['run'].reshape(-1)[m]
            m = m + 1
            h = int(j)
        elif int(j) == 0:
            if j <= float(int(j) + 0.6):
                r = r + df2['run'].reshape(-1)[m]
                m = m + 1
                h = int(j)

        else:
            if r == 0:
                counter = counter + 1
            else:
                counter = 0
            r = 0
            r = r + df2['run'].reshape(-1)[m]
            m = m + 1
            h = int(j)
    maiden.append(counter)

DataBowlers = pd.DataFrame({'1': bowl, '2': overs, '3': maiden, '4': runs, '5': wickets, '6': NB, '7': wides, '8': eco})
Bowler_columns = ['bowler', 'overs', 'maiden', 'runs', 'wickets', 'NB', 'wide', 'eco']
DataBowlers.columns = Bowler_columns
DataBowlers.to_csv('bowler_stat.csv', index=False)
best_baller = best_bowler(DataBowlers)

# Bowling Facts
'''   Highest Wicket Taker Taking into Consideration of their Economy rates  '''
d = DataBowlers.loc[DataBowlers['wickets'] == max(DataBowlers['wickets'])]
d = d.loc[d['eco'] == min(d['eco'])]

'''  Best Economy Rates  taking into consideration no. of maidens included   '''
d2 = DataBowlers.loc[DataBowlers['eco'] == min(DataBowlers['eco'])]
d2 = d2.loc[d2['maiden'] == max(d2['maiden'])]

runrate = list()
count, m, r = 1, 0, 0
for i in df['over']:
    k = float(i)
    if k < float(int(k) + 0.6):
        r = r + df['run'].reshape(-1)[m]
        m = m + 1

    elif k == float(int(k) + 0.6):
        r = r + df['run'].reshape(-1)[m]
        m = m + 1
        runrate.append(r / count)
        count = count + 1

import matplotlib.pyplot as plt2

o = list(range(1, 21, 1))
plt2.title('Run rate per over')
plt2.xlabel('Overs')
plt2.ylabel('Runrate')
plt2.scatter(x=o, y=runrate, c='r')
plt2.plot(o, runrate, c='b')
plt.savefig('runrate.png')
plt2.show()



