from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def hello():
    return """
    <html>
      <head>
        <title>BLABLABLA</title>
      </head>
      <body>
        <h1>ALLOHA</h1>
        <h2>PRIVET</h2>
        <h3>BONJUR</h3>
        <p>Скажи мне привет адвраыурарацу</p>
      </body>
    </html>    """


@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)