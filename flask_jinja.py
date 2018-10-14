from flask import Flask
from flask import render_template_string
import operator


app=Flask(__name__)

@app.route("/")
def update_table(data):
    #test data
    '''
    data = {"artist::song": 3, 
            "artist1::song1": 2,
            "artist2::song2": 5,
            "artist3::song3": 4
            }
    '''

    sorted_data = sorted(data.items(), key=operator.itemgetter(1))[::-1]

    table_data = []

    for i in sorted_data:
        a = i[0].split('::')[0]
        b = i[0].split('::')[1]
        c = i[1]
        table_data.append((a,b,c))

    print(table_data)

    html = """
    <!DOCTYPE html>
    <html lang="en">

      <head>

        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="">
        <meta name="author" content="">

        <title>Vote Now</title>

        <!-- Bootstrap Core CSS -->
        <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

        <!-- Custom Fonts -->
        <link href="vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
        <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,700,300italic,400italic,700italic" rel="stylesheet" type="text/css">
        <link href="vendor/simple-line-icons/css/simple-line-icons.css" rel="stylesheet">

        <!-- Custom CSS -->
        <link href="css/stylish-portfolio.min.css" rel="stylesheet">

      </head>

      <body id="page-top">


        <!-- Header -->
        <header class="masthead d-flex">
          <div class="container text-center my-auto">
            <h2 class="mb-1">Text To Vote</h2>
            <h4 class="mb-1">Song Name::Artist Name</h4>
            <h2 class="mb-1">630-812-7643</h2>
          </div>
          <div class="overlay"></div>
          <div class="container text-center">
            <div class="row">
              <div class="col-lg-10 mx-auto">
                <table class="table table-striped table-dark table-hover">
                  <thead>
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">Artist</th>
                      <th scope="col">Song Name</th>
                      <th scope="col"># Votes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {% for row in table_data %}
                    <tr>
                       <th scope="row">{{table_data.index(row) + 1}} 
                      <td>{{row[0]}}</td>
                      <td>{{row[1]}}</td>
                      <td>{{row[2]}}</td>
                    <tr>
                    {% endfor %}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </header>
      </body>
    </html>
    """
    rendered_html = render_template_string(html, table_data=table_data)

    return rendered_html
    
if __name__ == "__main__":
    app.run(debug=True)
