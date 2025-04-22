from flask import Flask, render_template
from test import import_test, list_kari

app = Flask("shiritori")

@app.route("/")
def test():
    return render_template(
        'index.html',
        message = 'shiritori apuri !!',
        msg = import_test(),
        list_kari = list_kari
        )



if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')