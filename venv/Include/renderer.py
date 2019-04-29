from yattag import Doc
import html2py

doc, tag, text = Doc().tagtext()

batting_team = "Sunriser's Hyderabad"
final_score = "181-3(20)"
batsman heading

with tag('table'):
    with tag('caption'):
        with tag('span'):
            text(batting_team + ' Innings')
        with tag('span'):
            text(final_score)
    with tag('tr'):
        with


print(doc.getvalue())


html2py.converter()