import pandas as pd
import matplotlib.pyplot as plt
import re
import basic_renderer as br


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
'''
print(strike_rate(85, 53))
print(economy(31, 4))
print(extract_ball_speeds())
'''

#Importing dataset
df = pd.read_csv('main.csv')

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


# Fall of wickets calculation
score = 0
outs = 0
balls = 0

for row in df.itertuples():
    score = score + row.run
    #if row.wide is not 1 or  row.nb is not 1 or row.lb is not 1:
    balls = balls + 1
    if row.out is 'c' or row.out is 'b':
        outs = outs + 1
        #balls = list_action[row.Index]
        
        print(str(score)+'-'+str(outs)+" ("+ row.batsman +", "+str(balls//6)+'.'+str(balls%6)+")")
  

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
    nrow = [batsman,dismissal,runs,balls,nfours,nsixes,strike_rate(runs,balls)]
    #print(nrow)
    batsman_stat.loc[len(batsman_stat)] = nrow
    count += 1
    
batsman_stat.to_csv('batsman_stat.csv')
        
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
plt.scatter([runslist[x] for x in wicketslist], wicketslist, c = 'red')
plt.show()   

