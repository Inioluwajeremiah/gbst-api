from flask import jsonify, Blueprint, request
import pickle
import pandas as pd
from  markupsafe import Markup
import validators
# from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy

predict_blueprint = Blueprint("predict", __name__)

model = pickle.load(open('model.pkl', 'rb'))

@predict_blueprint.post('/predict')
def predict():
    # Pregnancies	Glucose	BloodPressure	SkinThickness	Insulin	BMI	DiabetesPedigreeFunction	Age
    preganancies = request.get_json().get('pregnancies', '')
    glucose = request.get_json().get('glucose', '')
    blood_pressure = request.get_json().get('blood_pressure', '')
    skin_thickness = request.get_json().get('skin_thickness', '')
    insulin = request.get_json().get('insulin', '')
    bmi = request.get_json().get('bmi', '')
    dpf = request.get_json().get('dpf', '')
    age = request.get_json().get('age', '')

    preganancies = Markup.escape(preganancies)
    glucose = Markup.escape(glucose)
    blood_pressure =  Markup.escape(Markup.escape)
    skin_thickness = Markup.escape(skin_thickness)
    insulin = Markup.escape(insulin)
    bmi = Markup.escape(bmi)
    dpf = Markup.escape(dpf)
    age = Markup.escape(age)

    if preganancies == '':
        return jsonify({'error': 'pregnancy field is empty'})
    elif glucose == '':
        return jsonify({'error': 'Glucose field is empty'})
    elif blood_pressure == '':
        return jsonify({'error': 'BloodPressure field is empty'})
    elif skin_thickness == '':
        return jsonify({'error': 'SkinThickness field is empty'})
    elif insulin == '':
        return jsonify({'error': 'Insulin field is empty'})
    elif bmi == '':
        return jsonify({'error': 'BMI field is empty'})
    elif dpf == '':
        return jsonify({'error': 'DiabetesPedigreeFunction field is empty'})
    elif age == '':
        return jsonify({'error': 'Age field is empty'})
    else:
        dictionary_data = {"Pregnancies": preganancies, "Glucose": glucose, "BloodPressure": blood_pressure,
                           "SkinThickness": skin_thickness, "Insulin": insulin, "BMI": bmi, "DiabetesPedigreeFunction": dpf, "Age": age}

        x_test = pd.DataFrame(dictionary_data, index=[0])
        predict_gbst = model.predict(x_test)
        # result =

        print(predict_gbst)
        return jsonify({'result': predict_gbst.tolist()[0]})