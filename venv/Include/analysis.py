import pandas as pd
import matplotlib.pyplot as plt
import re
#from BowlingAnalysis import BowlingAnalysis


def strike_rate(runs_scored, balls_faced):
    return "%.2f" % (( runs_scored / balls_faced ) * 100)


def economy(runs_conceded, overs_balled):
    return "%.2f" % ( runs_conceded / overs_balled )


def extract_ball_speeds():
    # Finding all the ball speeds
    f = open('BOSCH_HACKATHON/Data.txt', "r+").read()
    #print(f)
    bowling_speeds = re.findall(pattern="[0-9]+[.][0-9]+km/h", string=f)
    print(bowling_speeds)
    m = max(bowling_speeds)
    print(m)

    f = f.split('\n')
    for i in f:
        if str(m) in i:
            return [i.split(' ')[0],m]


    


# Importing dataset
df = pd.read_csv('main.csv')

# Tests
'''
print(strike_rate(85, 53))
print(economy(31, 4))
'''
fastest_bowler = extract_ball_speeds()

# Calculating the final score    
total_runs = sum(df.run)+sum(df.wide)
no_of_wickets = 0
for verdict in df.out:
    if verdict is 'c' or verdict is 'b':
        no_of_wickets = no_of_wickets + 1
overs = len(df.bowler)/6
if overs > 20:
    overs = 20
    
final_score = str(total_runs)+"-"+str(no_of_wickets)+" ("+str(overs)+")"


def get_name(name):
    return {
        ' rahul': 'Lokesh Rahul',
        ' gayle': 'Chris Gayle',
        ' agarwal': 'Mayank Agarwal',
        ' sarfaraz khan': 'Sarfaraz Khan',
        ' miller': 'David_Miller',
        ' mandeep': 'Mandeep Singh',
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
    #if row.wide is not 1 or  row.nb is not 1 or row.lb is not 1:
    balls = balls + 1
    if row.out is 'c' or row.out is 'b':
        outs = outs + 1
        #balls = list_action[row.Index]

        fow = str(score)+'-'+str(outs)+" ("+ get_name(row.batsman) +", "+str(balls//6)+'.'+str(balls%6)+"),"
        print(fow)
        fall_of_wickets = fow + fall_of_wickets
  

#Batsman Table
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
            #print([batsman,row.batsman])
            balls = balls + 1
            if row.out != 'not out':
                dismissal = row.out_by
                print(row.out)
                break
            if row.run is 6:
                nsixes += 1
            elif row.run is 4:
                nfours += 1
            else:
                runs += row.run
                runs -= row.lb
                #runs += row.wide
            
    
    runs = runs+4*nfours+6*nsixes
    nrow = [get_name(batsman),dismissal,runs,balls,nfours,nsixes,strike_rate(runs,balls)]
    #print(nrow)
    batsman_stat.loc[len(batsman_stat)] = nrow
    count += 1
    
batsman_stat.to_csv('batsman_stat.csv',index=False)
        
runslist = []
wicketslist = []
ru=0
for row in df.itertuples():
    ru += row.run
    runslist.append(ru)
    if row.out != 'not out':
        wicketslist.append(row.Index)
 

# Plot runs vs balls
plt.title('Progress of scores')
plt.xlabel('Runs')
plt.ylabel('Balls')
plt.legend()
plt.plot(runslist,df.index)
plt.scatter([runslist[x] for x in wicketslist], wicketslist, c = 'red', label='dismissals')

plt.savefig('run_vs_ball.png')  
plt.show()

###################################################

'''   Bowler score card generator '''
'''
bowl, overs, maiden, runs, wickets, NB, wides, eco = list(), list(), list(), list(), list(), list(), list(), list()
df2 = pd.DataFrame()

i, lis = 0, list()
lis.append(df.iloc[:, 2].values[0])

for i in df['bowler']:
    if (i not in lis):
        lis.append(i)
for i in lis:
    counter = 0
    m = 0
    df2 = df.loc[df['bowler'] == i]
    bowl.append(i)
    overs.append(len(df2['bowler']) // 6)
    wides.append(sum(df2['wide']))
    NB.append(sum(df2['nb']))
    wickets.append(len(df2.loc[df2['out'] != 'not out']['out']))
    runs.append(sum(df2['run']))
    eco.append(economy(sum(df2['run']), len(df2['bowler'])))#(sum(df2['run'])) / (len(df2['bowler']) // 6)
    h = int(df['over'].reshape(-1)[0].split('.')[0])
    r = 0
    for j in df2['over']:
        k = float(j)
        if int(k) != 0 and (k <= float(int(k) + 0.6)) and (h % int(k) == 0):
            r = r + df2['run'].reshape(-1)[m]
            m = m + 1
            h = int(j.split('.')[0])
        elif int(k) == 0:
            if (k <= float(int(k) + 0.6)):
                r = r + df2['run'].reshape(-1)[m]
                m = m + 1
                h = int(j.split('.')[0])

        else:
            if r == 0:
                counter = counter + 1
            else:
                counter = 0
            r = 0
            r = r + df2['run'].reshape(-1)[m]
            m = m + 1
            h = int(j.split('.')[0])
    maiden.append(counter)

DataBowlers = pd.DataFrame({'1': bowl, '2': overs, '3': maiden, '4': runs, '5': wickets, '6': NB, '7': wides, '8': eco})
Bowler_columns = ['bowler', 'overs', 'maiden', 'runs', 'wickets', 'NB', 'wide', 'eco']
DataBowlers.columns = Bowler_columns
DataBowlers.to_csv('Bowler_Data.csv', index=False)

# Bowling Facts
   Highest Wicket Taker Taking into Consideration of their Economy rates  
d = DataBowlers.loc[DataBowlers['wickets'] == max(DataBowlers['wickets'])]
d = d.loc[d['eco'] == min(d['eco'])]

  Best Economy Rates  taking into consideration no. of maidens included   
d2 = DataBowlers.loc[DataBowlers['eco'] == min(DataBowlers['eco'])]
d2 = d2.loc[d2['maiden'] == max(d2['maiden'])]

runrate = list()
count, m, r = 1, 0, 0
for i in df['over']:
    k = float(i)
    if (k < float(int(k) + 0.6)):
        r = r + df['run'].reshape(-1)[m]
        m = m + 1

    elif k == float(int(k) + 0.6):
        r = r + df['run'].reshape(-1)[m]
        m = m + 1
        runrate.append(r / count)
        count = count + 1

o = list(range(1, 21, 1))
plt.scatter(x=o, y=runrate, c='r')
plt.plot(o, runrate, c='b')
plt.show()
'''