
from flask import Flask, render_template, request
import skfuzzy as skf
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

age = ctrl.Antecedent(np.arange(10,81,1), 'age')
chestpain = ctrl.Antecedent(np.arange(0,11,1),'chestpain')
bloodpressure  = ctrl.Antecedent(np.arange(100,201,1),'bloodpressure')
cholestrol  = ctrl.Antecedent(np.arange(100,271,1),'cholestrol')
heartrate  = ctrl.Antecedent(np.arange(60,201,1),'heartrate')
diagnosis = ctrl.Consequent(np.arange(0,3,1),'diagnosis')

range = ['low','medium','high']
age.automf(3, names=range)
chestpain.automf(3, names=range)
bloodpressure.automf(3, names=range)
cholestrol.automf(3, names=range)
heartrate.automf(3, names=range)
diagnosis.automf(3, names=range)

rule1 = ctrl.Rule(age['low'], diagnosis['low'])
rule2 = ctrl.Rule(age['medium'], diagnosis['medium'])
rule3 = ctrl.Rule(age['high'], diagnosis['high'])
rule4 = ctrl.Rule(chestpain['low'], diagnosis['low'])
rule5 = ctrl.Rule(chestpain['medium'], diagnosis['high'])
rule6 = ctrl.Rule(chestpain['high'], diagnosis['high'])
rule7 = ctrl.Rule(bloodpressure['low'], diagnosis['low'])
rule8 = ctrl.Rule(bloodpressure['medium'], diagnosis['medium'])
rule9 = ctrl.Rule(bloodpressure['high'], diagnosis['high'])
rule10 = ctrl.Rule(cholestrol['low'], diagnosis['low'])
rule11 = ctrl.Rule(cholestrol['medium'], diagnosis['medium'])
rule12 = ctrl.Rule(cholestrol['high'], diagnosis['high'])
rule13 = ctrl.Rule(heartrate['low'], diagnosis['low'])
rule14 = ctrl.Rule(heartrate['medium'], diagnosis['medium'])
rule15 = ctrl.Rule(heartrate['high'], diagnosis['high'])

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/index")
def instruction():
    return render_template("index.html")


@app.route("/question", methods=["GET", "POST"])
def question():
    if request.method == "GET":
        return render_template("question.html")
    else:
        diagnosis_result = ctrl.ControlSystem(
            [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11,
             rule12, rule13, rule14, rule15])
        result = ctrl.ControlSystemSimulation(diagnosis_result)
        result.input['age'] = float(request.form.get("age"))
        result.input['chestpain'] = float(request.form.get("chestpain"))
        result.input['bloodpressure'] = float(request.form.get("bloodpressure"))
        result.input['cholestrol'] = float(request.form.get("cholestrol"))
        result.input['heartrate'] = float(request.form.get("heartrate"))
        result.compute()
        diagnosis.view(sim=result)
        plt.savefig('static/image.png')
        print_result = float(result.output['diagnosis'])
        return render_template("result.html", print_result=print_result)


@app.route("/result")
def result():
    return render_template("result.html", diagnosis=diagnosis)

