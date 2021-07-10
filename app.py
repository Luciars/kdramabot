import flask
from api.api import api_bp

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app.register_blueprint(api_bp, url_prefix="/api/v1")

@app.route('/', methods=['GET'])
def version():
    return "This is the index page"

app.run()