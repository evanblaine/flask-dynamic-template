import threading
import time
from datetime import datetime

from flask import Flask, render_template
from turbo_flask import Turbo

app = Flask(__name__,
            template_folder="templates"
            )
turbo = Turbo(app)


def update_data():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template(
                'data.html'), "data"))


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_data).start()


@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def inject():
    dt = datetime.now()
    data = dt.time().strftime("%H:%M:%S")
    return {"data": data}


if __name__ == "__main__":
    app.run(debug=True)
