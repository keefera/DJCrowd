from flask import Flask
from flask import render_template
import operator


app=Flask(__name__)

@app.route("/")
def update_table():
    #test data
    data = {"artist::song": 3, 
            "artist1::song1": 2,
            "artist2::song2": 5,
            "artist3::song3": 4
            }

    sorted_data = sorted(data.items(), key=operator.itemgetter(1))[::-1]

    table_data = []

    for i in sorted_data:
        a = i[0].split('::')[0]
        b = i[0].split('::')[1]
        c = i[1]
        table_data.append((a,b,c))

    #looks in templates folder for index1.html
    return render_template("index1.html", table_data=table_data)
    
if __name__ == "__main__":
    app.run(debug=True)
