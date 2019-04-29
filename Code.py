import re
import pandas as pd


file = open('C:\\Users\\Swayamdipta Biswas\\Downloads\\Data.txt')
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

    elif ('leg byes' in lsplit[1]):
        lb.append(1)
        run.append(dictionary1[lsplit[2].strip()])
        out.append('not out')
        lout.append('none')
        wide.append(0)
        no_ball.append(0)
    elif 'out' in lsplit[1]:

        v = lsplit[1].split('!')[0].split(' ')
        if 'bowled' == v[1]:
            out.append(dictionary1[v[1]])
            run.append(0)
            wide.append(0)
            lb.append(0)
            no_ball.append(0)
            lout.append(lsplit[0].split('to')[0])
        elif 'caught' == v[1]:
            out.append(dictionary1[v[1]])
            run.append(0)
            wide.append(0)
            lb.append(0)
            lout.append(v[3])
            no_ball.append(0)
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
data['Out By']=lout()'''

print(batsman,'\n\t',bowler,'\n\t',run,'\n\t',wide,'\n\t',lb,'\n\t',no_ball,'\n\t',out,'\n\t',lout)



