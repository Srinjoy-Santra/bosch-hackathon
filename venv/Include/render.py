import analysis as an
import pandas as pd
import code as cd

team_innings = "King's IX Punjab" + " Innings"
batsman_stat = an.batsman_stat
bowler_stat = an.DataBowlers
fall_of_wickets = an.fall_of_wickets


def add_stat(stat):
    tr = ""
    for row in stat.itertuples():
        tr = tr + "<tr>"
        tr = tr + "<td><a href='" + an.name_to_url(str(row[1])) + "' style='color:#2279FC;font-size:18'>"+str(row[1])+"</a></td>"
        for data in row[2:]:
            tr = tr + "<td>" + str(data) + "</td>"
        tr = tr + "\n</tr>"

    return tr


body = """
    <body>
        <table>
           <caption>
               <span>""" + team_innings + """</span>
               <span>""" + an.final_score + """</span>
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
                <td>""" + an.fall_of_wickets + """</td>
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
       
        <div class="flex-container">
		<img src="https://seeklogo.com/images/I/ipl-kings-xi-punjab-logo-6747D5C02B-seeklogo.com.png" alt='kxip' />
		
		<div>
			<h3>Trivia</h3>
			<b>
			<blockquote>Fastest Ball by """+an.get_name(an.fastest_bowler[0].strip().lower())+" with a speed of "+str(an.fastest_bowler[1])+""" </blockquote>     
        <blockquote>Best Hitter """+an.best_batter[0]+" scoring "+str(an.best_batter[1])+""" points</blockquote>     
        <blockquote>Best Thrower """+an.best_baller[0]+" scoring "+str(an.best_baller[1]/10)+""" points</blockquote>       
        <blockquote>Most Tweeted player of the innings """+an.get_name(cd.find_most_tweet()[0])+"""</blockquote> 
			</b>
		</div>
		<img src="https://seeklogo.com/images/K/kolkata-knight-riders-logo-532F9512B0-seeklogo.com.jpg" alt='kkr' />
		</div>
		
		
		
		
        <br/>
		<p style="color: red"; font-size="12px; float:center-right">Red dot in IMG(1) denotes fall of wickets; in IMG(2) denotes end of overs</p>
		<div class="flex-container">
			<img src="run_vs_ball.png" alt='runs vs balls'/>
			<img src="runrate.png" alt='run rate'/>
			
		<div/>
		

        
    </body>
"""

head = """<html>
    <head>
        <title>Scorecard Mockup</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                margin:5px;
            }
            td{
                border-bottom: 0.5px solid lightgray;
                margin:5px;
            }
            caption {
                background-color: black;
                color: aliceblue;
                padding: 10px;
                font-family: monospace;
            }
            div{
                padding:10px;
                margin:10px;
                }
            .flex-container{
				display:flex;
			}
        </style>
    </head>
    """ + body + """
</html>
"""

# Creating the HTML output file
f = open('output.html', "w+")
f.write(head)
print(an.batsman_stat)
