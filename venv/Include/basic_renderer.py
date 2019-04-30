import pandas as pd


team_innings = "King's IX Hyderabad" + " Innings"
final_score = "181-3(20)"
batsman_stat = pd.read_csv('batsman_stat.csv')[1:]


bowler_stat = pd.DataFrame(data=[['Prasidh Krishna', 4, 0, 31, 0, 1, 2, 7.75],
                                 ['Piyush Chawla', 3, 0, 23, 1, 0, 0, 7.67]],
                           columns=['bowler', 'O', 'M', 'R', 'W', 'NB', 'WD', 'ECO'])

fall_of_wickets = " cdvd "
# print(batsman_stat)
def name_to_url(name):
    return "https://en.wikipedia.org/wiki/" + name.replace(" ", '_')

def add_stat(stat):
    tr = ""
    for row in stat.itertuples():
        tr = tr + "<tr>"
        tr = tr + "<td><a href='" + name_to_url(str(row[2])) + "'>"+str(row[2])+"</a></td>"
        for data in row[2:]:
            tr = tr + "<td>" + str(data) + "</td>"
        tr = tr + "\n</tr>"

    return tr


body = """
    <body>
        <table>
           <caption>
               <span>""" + team_innings + """</span>
               <span>""" + final_score + """</span>
            </caption>
            <tr>
            <th>Batsman</th>
            <th></th>
            <th>R</th> 
            <th>B</th>
            <th>4s</th>
            <th>6s</th>
            <th>SR</th>
            </tr>

            """ + add_stat(batsman_stat) + """
        </table>
        <table>
            <tr><th>Fall of Wickets</th></tr>
            <tr>
                <td>""" + fall_of_wickets + """</td>
            </tr>
        </table>
        <table>
            <tr>
                <th>Bowler</th>
                <th>O</th>
                <th>M</th>
                <th>R</th>
                <th>W</th>
                <th>NB</th>
                <th>WD</th>
                <th>ECO</th>
            </tr>
            """ + add_stat(bowler_stat) + """
        </table>
        <h3>Trivia</h3>
        <blockquote>Fastest Bowler?</blockquote>     
        <blockquote>Biggest Six?</blockquote>     
        <blockquote>Did you really expect one more?</blockquote>     
        <a href="https://en.wikipedia.org/wiki/Ashok_Dinda">Person</a>
    </body>

"""

head = """<html>
    <head>
        <title>Scorecard Mockup</title>
        <style>
            *{
                text-align: left;
            }
            table {
                      border-collapse: collapse;

                      width:100%;
                }
            th {
                background-color: lightgray;
                font-weight: bold;
            }
            td{
                border-bottom: 0.5px solid lightgray;
            }
            caption {
                background-color: black;
                color: aliceblue;
                padding: 4px;
                font-family: monospace;
            }

            caption > span {
                justify-content: flex-end;
            }
        </style>
    </head>
    """ + body + """
</html>
"""

# print(add_batsman_stat(batsman_stat))
print(head)

f = open('output.html', "w+")
f.write(head)

print(batsman_stat)