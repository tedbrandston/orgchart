from orgchart import flask_app

@flask_app.route('/')
@flask_app.route('/index')
def index():
    return "Hello, World!"
