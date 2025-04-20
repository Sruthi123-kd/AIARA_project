from flask import *
from public import *
from admin import *
from user import *


app=Flask(__name__)

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(user)

app.secret_key="sdfghj"


app.run(debug=True,port=5005)