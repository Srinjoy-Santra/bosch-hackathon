import re

import pandas as pd


file = open(r'C:\Users\nEW u\PycharmProjects\bosch\venv\Include\BOSCH_HACKATHON\Data.txt')
list_all_lines, list_over_deliveries, list_action, list_in_btwn_overs, list_action_otherwise = list(), list(), list(), list(), list()
for line in reversed(file.readlines()):
    list_all_lines.append(line.rstrip().lower())
string1, string2 = "", ""
for i in list_all_lines:

    if i is not '' and i is not ' ' and ord(i[0]) in list(range(48, 58, 1)) and len(i) <= 4:

        if ('.' in i) and type(float(i)).__name__ == 'float':
            string1 = string1.replace(string2, "")
            list_action.append(string1)
            list_action_otherwise.append(string2)
            list_over_deliveries.append(i)
            string1 = ""
            string2 = ""
        else:
            if string1 is not ' ':
                list_in_btwn_overs.append(string1)
            string1 = ""
            string2 = ""
    else:
        string2 = string1
        string1 = string1 + "" + i

list_other_combined = list(set(list_action_otherwise + list_in_btwn_overs))
l = list()
for i in list_other_combined:
    if (i != ''):
        l.append(i)
list_other_combined = l
del l
lsplit = list()
bowler = list()
batsman = list()
run = list()
speed = list()
wide = list()
no_ball = list()
lb = list()
out = list()
lout = list() # b-bowled,c-caught

dictionary1 = {'1 run': 1, 'bowled': 'b', 'caught': 'c', 'no run': 0, 'six': 6, 'four': 4,'5 runs': 5, 'wide': 1, '2 runs': 2, 'leg byes': 1, '4': 4, '6': 6}

for i in list_action:
    lsplit = i.split(',')

    batsman.append(lsplit[0].split('to')[1])
    bowler.append(lsplit[0].split('to')[0])
    if ('wide' in lsplit[1]):
        wide.append(1)
        lout.append('none')
        run.append(1)
        lb.append(0)
        out.append('not out')
        no_ball.append(0)

    elif ('leg byes' in lsplit[1]):
        lb.append(1)
        run.append(dictionary1[lsplit[2].strip()])
        out.append('not out')
        lout.append('none')
        wide.append(0)
        no_ball.append(0)
        
    elif 'out' in lsplit[1]:

        v = lsplit[1].split('!')[0].split(' ')
        
        if 'bowled' == v[2]:
            out.append(dictionary1[v[2]])
            run.append(0)
            wide.append(0)
            lb.append(0)
            no_ball.append(0)
            lout.append(lsplit[0].split('to')[0])
        elif 'caught' == v[2]:
            out.append(dictionary1[v[2]])
            run.append(0)
            wide.append(0)
            lb.append(0)
            
            bowlern = lsplit[0].split(' ')[0:2]
            name = bowlern[0]
            if len(name) is 1:
                name = name + " " + bowlern[1]
            
            lout.append("c " + v[4] + " b " + name)
            no_ball.append(0)
            
        #NO LBWs FOUND!!NO RUN OUTS FOUND!!
        
    elif 'no ball' in lsplit[1]:
        no_ball.append(1)
        out.append('not out')
        run.append(0)
        wide.append(0)
        lb.append(0)
        lout.append('none')

    else:
        wide.append(0)
        lb.append(0)
        out.append('not out')
        lout.append('none')
        run.append(dictionary1[lsplit[1].strip()])
        no_ball.append(0)

'''data=pd.DataFrame()
data['Batsman']=batsman()
data['Bowler']=bowler()
data['Run']=run()
data['Wide']=wide()
data['LB']=lb()
data['NB']=no_ball()
data['Out']=out()
data['Out By']=  ()'''

#print(batsman,'\n\t',bowler,'\n\t',run,'\n\t',wide,'\n\t',lb,'\n\t',no_ball,'\n\t',out,'\n\t',lout)

# Creating the dataset
df_columns=['batsman','bowler','runs','wide','lb','nb','out','out_by']
df = pd.DataFrame({
        'batsman':batsman,'bowler':bowler,'run':run,'wide':wide,
        'lb':lb,'nb':no_ball,'out':out,'out_by':lout})

# Calculating the final score    
total_runs = sum(run)
no_of_wickets = 0
for verdict in out:
    if verdict is 'c' or verdict is 'b':
        no_of_wickets = no_of_wickets + 1
overs = len(bowler)/6
if overs > 20:
    overs = 20
    
final_score = str(total_runs)+"-"+str(no_of_wickets)+" ("+str(overs)+")"


# Fall of wickets calculation [Error]
score = 0
outs = 0
balls = 0

for row in df.itertuples():
    score = score + row.run
    if row.wide is not 1 or  row.nb is not 1 or row.lb is not 1:
        balls = balls + 1
    if row.out is 'c' or row.out is 'b':
        outs = outs + 1
        #balls = list_action[row.Index]
        
        print(str(score)+'-'+str(outs)+" ("+ row.batsman +", "+str(balls//6)+'.'+str(balls%6)+")")
        balls = balls - 1
    #else:
        
        #print(str(balls) + " = "+ str(balls//6)+'.'+str(balls%6) + ":" + str(row.Index))
  

#Batsman Table
batsman_stat = pd.DataFrame(columns=['batsman', 'dismissal',
                                     'R', 'B', '4s', '6s', 'SR'])

batsmen = list(dict.fromkeys(batsman))
count = 0
for batsman in batsmen:
    nsixes = 0
    nfours = 0
    runs = 0
    balls = 0
    dismissal = ''
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
            
    #batsman_stat.loc[count] = [batsman,dismissal]
    print([batsman,dismissal,runs+4*nfours+6*nsixes,balls,nfours,nsixes,0])
    count += 1
        
        

        