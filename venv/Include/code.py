import re
import pandas as pd
import matplotlib.pyplot as plt


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


hasWide = False
for i in range(0,len(list_action)):
    lsplit = list_action[i].split(',')
    
    
    w=r=l=nb=0
    lo='none'
    ou='not out'
        
    
    if ('wide' in lsplit[1]):
        w=1
        r=1
        hasWide = True
        
        

    elif ('leg byes' in lsplit[1]):
        l=1
        r=dictionary1[lsplit[2].strip()]
        
    elif 'out' in lsplit[1]:

        v = lsplit[1].split('!')[0].split(' ')
        
        if 'bowled' == v[2]:
            ou = dictionary1[v[2]]
            lo = lsplit[0].split('to')[0]
            
        elif 'caught' == v[2]:
            ou = dictionary1[v[2]]
            
            bowlern = lsplit[0].split(' ')[0:2]
            name = bowlern[0]
            if len(name) is 1:
                name = name + " " + bowlern[1]
            
            lo = "c " + v[4] + " b " + name
            
            
            
           
            
        #NO LBWs FOUND!!NO RUN OUTS FOUND!!
        
    elif 'no ball' in lsplit[1]:
        nb=1
        

    else:
        r=dictionary1[lsplit[1].strip()]
        
    if w is not 1:
        batsman.append(lsplit[0].split('to')[1])
        bowler.append(lsplit[0].split('to')[0])
        if hasWide:
            w += 1
            
        wide.append(w)
        run.append(r)
        lb.append(l)
        no_ball.append(nb)
        lout.append(lo)
        out.append(ou)
        hasWide = False
    
    
    

        



# Creating the dataset
i,lis=0,list()
lis.append(list_over_deliveries[0])
        
for i in list_over_deliveries:
    if(i not in lis):
        lis.append(i)
df_columns = ['over','batsman', 'bowler', 'run', 'wide', 'lb', 'nb', 'out', 'out_by']
df = pd.DataFrame({'1':lis,'2': batsman, '3': bowler, '4': run, '5': wide,'6': lb, '7': no_ball, '8': out, '9': lout})
df.columns=df_columns
df.to_csv('main.csv',index=False)

tweets = []
for row in list_other_combined:
    say = row.split(' ')
    
    try:
        print(say[1])
        if say[1] == 'says:' or say[2] == 'says:':
            tweets.append(row)
    except:
        pass
