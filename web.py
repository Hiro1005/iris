import numpy as np

def insert_csv(data):
    import csv
    import uuid
    tuid = str(uuid.uuid1())
    with open("./logs/"+tuid+".csv", "a") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(["sepalLength","sepalWidth","petalLength","petalWidth"])
        writer.writerow(data)
    return tuid

def predictIris(params):
    from sklearn.externals import joblib
    # load the model
    forest = joblib.load('./rfcParam.pkl')
    # predict
    params = params.reshape(1,-1)
    pred = forest.predict(params)
    return pred

def getIrisName(irisId):
    if irisId == 0:
        return "ヒオウギアヤメ(Iris Setosa)"
    elif irisId == 1:
        return "ブルーフラッグ(Iris Versicolour)"
    elif irisId == 2:
        return "バージニカ(Iris Virginica)"
    else:
        return "Error"

from flask import Flask, render_template, request, flash
from wtforms import Form, FloatField, SubmitField, validators, ValidationError, StringField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)

# Generated using import binascii & binascii.hexlify(os.urandom(24))
app.config['SECRET_KEY'] = '7c129b305b0d2d0116aed983f82a84b7a2be6872e51a8fd1'

# Flask-Bootstrap requires this line
bootstrap = Bootstrap(app)

class IrisForm(Form):
    sepalLength = FloatField("Sepal Length (cm) がくの長さ(0〜10の値) :",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=10)])
    sepalWidth = FloatField("Sepal Width (cm) がくの幅(0〜10の値) :",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=10)])
    petalLength = FloatField("Petal Length (cm) 花びらの長さ(0〜10の値) :",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=10)])
    petalWidth = FloatField("Petal Width (cm) 花びらの幅(0〜10の値) :",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=10)])
    submit = SubmitField("予測する：Predict")

@app.route('/', methods = ['GET', 'POST'])
def irisPred():
    form = IrisForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            flash("You need all parameters")
            return render_template('irisPred.html', form = form)
        else:
            sepalLength = float(request.form["sepalLength"])
            sepalWidth = float(request.form["sepalWidth"])
            petalLength = float(request.form["petalLength"])
            petalWidth = float(request.form["petalWidth"])
            params = np.array([sepalLength, sepalWidth, petalLength, petalWidth])
            print(params)
            insert_csv(params)
            pred = predictIris(params)
            irisName = getIrisName(pred)

            return render_template('success.html', irisName=irisName)
    elif request.method == 'GET':
        return render_template('irisPred.html', form = form)

if __name__ == "__main__":
    app.debug = True
    # app.run(host='0.0.0.1')
    app.run(host='127.0.0.1', port=5000)