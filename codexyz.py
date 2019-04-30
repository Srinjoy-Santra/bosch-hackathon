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
lout = list()  # b-bowled,c-caught

dictionary1 = {'1 run': 1, 'bowled': 'b', 'caught': 'c', 'no run': 0, 'six': 6, 'four': 4, '5 runs': 5, 'wide': 1,
               '2 runs': 2, 'leg byes': 1, '4': 4, '6': 6}

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

        # NO LBWs FOUND!!

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


# Preparing the Grand Dataset
df_columns = ['over','batsman', 'bowler', 'run', 'wide', 'lb', 'nb', 'out', 'out_by']
df = pd.DataFrame({'1':list_over_deliveries,'2': batsman, '3': bowler, '4': run, '5': wide,'6': lb, '7': no_ball, '8': out, '9': lout})
df.columns=df_columns
     
total_runs = sum(run)
no_of_wickets = 0
for verdict in out:
    if verdict is 'c' or verdict is 'b':
        no_of_wickets = no_of_wickets + 1
df.to_csv('cricketresults.csv',index=False) 

## Preparing The Bowler Dataset as a subset of the Grand Dataset

'''   Bowler score card generator '''

bowl,overs,maiden,runs,wickets,NB,wides,eco=list(),list(),list(),list(),list(),list(),list(),list()
df2=pd.DataFrame()

bowl_er=list(set(bowler))
for i in bowl_er:
    counter=0
    m=0
    df2=df.loc[df['bowler'] == i]
    bowl.append(i)
    overs.append(len(df2['bowler'])//6)
    wides.append(sum(df2['wide']))
    NB.append(sum(df2['nb']))
    wickets.append(len(df2.loc[df2['out']!='not out']['out']))
    runs.append(sum(df2['run']))
    eco.append((sum(df2['run']))/(len(df2['bowler'])//6))
    h=int(df['over'].reshape(-1)[0].split('.')[0])
    r=0
    for j in df2['over']:
        k=float(j)
        if int(k)!=0 and (k<=float(int(k)+0.6)) and (h%int(k)==0):
           r=r+df2['run'].reshape(-1)[m]
           m=m+1
           h=int(j.split('.')[0])
        elif int(k)==0:
            if (k<=float(int(k)+0.6)):
              r=r+df2['run'].reshape(-1)[m]
              m=m+1
              h=int(j.split('.')[0])
           
        else:
            if r==0:
                counter=counter+1
            else:
                counter=0
            r=0
            r=r+df2['run'].reshape(-1)[m]
            m=m+1
            h=int(j.split('.')[0])
    maiden.append(counter)
        
              
    
DataBowlers=pd.DataFrame({ '1':bowl,'2':overs,'3':maiden,'4':runs,'5':wickets,'6':NB,'7':wides,'8':eco}) 
Bowler_columns=['bowler','overs','maiden','runs','wickets','NB','wide','eco']
DataBowlers.columns=Bowler_columns
DataBowlers.to_csv('Bowler_Data.csv',index=False)

# Bowling Facts
'''   Highest Wicket Taker Taking into Consideration of their Economy rates  '''
d=DataBowlers.loc[DataBowlers['wickets']==max(DataBowlers['wickets'])]
d=d.loc[d['eco']==min(d['eco'])]

'''  Best Economy Rates  taking into consideration no. of maidens included   '''
d2=DataBowlers.loc[DataBowlers['eco']==min(DataBowlers['eco'])]
d2=d2.loc[d2['maiden']==max(d2['maiden'])]


## Saving Memory Spaces 
del bowl,overs,maiden,runs,wickets,NB,wides,eco,counter,m,h,r,k,lsplit,bowler,batsman,run,speed ,wide ,no_ball ,lb ,out,lout 

## Data Structures in hand

#  * llist_all_lines, 
#  * list_over_deliveries, 
#  * list_action, 
#  *list_in_btwn_overs, 
#  *list_action_otherwise 
#  * d, d2
