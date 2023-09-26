from flask import jsonify, Blueprint
from app.databaseModel import db, Enrollment, MedicalHistory, ClinicalHistory, ChildBirthOutcome, ObstetricInformation, Predict
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user
import pickle
import pandas as pd
from datetime import date

predict_blueprint = Blueprint("predict", __name__)


@predict_blueprint.get('/')
@login_required
def predict():
    # Pregnancies	Glucose	BloodPressure	SkinThickness	Insulin	BMI	DiabetesPedigreeFunction	Age
    
    model = pickle.load(open('model.pkl', 'rb'))
    current_date = date.today()
    current_date_str = current_date.strftime("%Y-%m-%d")

    Enrollment, MedicalHistory, ClinicalHistory, ChildBirthOutcome, ObstetricInformation

    childBirthOutcome = ChildBirthOutcome.query.filter_by(user_id=current_user.id,date=current_date_str).first()
    medicalHistory = MedicalHistory.query.filter_by(user_id=current_user.id).first()
    clinicalHistory = ClinicalHistory.query.filter_by(user_id=current_user.id).first()
    enrollment = Enrollment.query.filter_by(user_id=current_user.id).first()
    obstetricInformation = ObstetricInformation.query.filter_by(user_id=current_user.id).first()
    

    age = obstetricInformation.gestationalAge
    noOfPregnancies = obstetricInformation.noOfPregnancies
    gestationPeriod = obstetricInformation.gestationPeriod
    bmi = clinicalHistory.bmi
    history = medicalHistory.history
    unexplainedPrenatalLoss = obstetricInformation.unexplainedPrenatalLoss
    fourKgBirthWeight = obstetricInformation.fourKgBirthWeight
    pcos = medicalHistory.pcos
    systolicBP = obstetricInformation.systolicBP
    dialstolicBP = obstetricInformation.dialstolicBP
    sedentary = enrollment.sedentary

    if not age:
        return jsonify({'message': 'Input Gestational age under Obstetric History'}), HTTP_400_BAD_REQUEST
    if not noOfPregnancies:
        return jsonify({'message': 'Fill number of previous pregnancies field in Obstetric History'}), HTTP_400_BAD_REQUEST
    if not gestationPeriod:
        return jsonify({'message': 'Fill gestation in previous pregnancy field in Obstetric History'}), HTTP_400_BAD_REQUEST
    if not bmi:
        return jsonify({'message': 'Input BMI under Clinical History'}), HTTP_400_BAD_REQUEST
    if not history:
        return jsonify({'message': 'Fill history of Gestational Diabetes Mellitus in Medical History'}), HTTP_400_BAD_REQUEST
    if not unexplainedPrenatalLoss:
        return jsonify({'message': 'Fill unexplained prenatal loss in Obstetric History'}), HTTP_400_BAD_REQUEST
    if not fourKgBirthWeight:
        return jsonify({'message': 'Fill baby with a birth weight of 4kg and above in Obstetric History'}), HTTP_400_BAD_REQUEST
    if not pcos:
        return jsonify({'message': 'Fill Polycytist Ovary Syndrome in Medical History'}), HTTP_400_BAD_REQUEST
    if not systolicBP:
        return {"message": "Fill Systolic blood pressure in Obstetric History"}, HTTP_400_BAD_REQUEST
    if not dialstolicBP:
        return {"message":"Fill Diastolic blood pressure in Obstetric History"}, HTTP_400_BAD_REQUEST
    if not enrollment:
        return {"message": "Fill sedentary lifestyle in Enrollment ID"}, HTTP_400_BAD_REQUEST
    
    else:
        if  history == "No":
            history = 1
        else:
            history = 0

        if  unexplainedPrenatalLoss == "No":
            unexplainedPrenatalLoss = 1
        else:
            unexplainedPrenatalLoss = 0
        
        if fourKgBirthWeight == "No":
            fourKgBirthWeight = 1
        else:
            fourKgBirthWeight = 0
        
        if pcos == "No":
            pcos = 1
        else:
            pcos = 0
        
        if sedentary == "No" or not sedentary:
            sedentary = 1
        else:
            sedentary = 0
        try:

            dictionary_data = {'Case Number': 1, 'Age':age, 'No of Pregnancy':noOfPregnancies, 'Gestation in previous Pregnancy':gestationPeriod,
                            'BMI':bmi, 'HDL': 0, 'Family History':history, 'unexplained prenetal loss':unexplainedPrenatalLoss, 
                                'Large Child or Birth Default':fourKgBirthWeight, 'PCOS':pcos, 'Sys BP':systolicBP,  'Dia BP':dialstolicBP,  
                                'OGTT': 0, 'Hemoglobin': 0, 'Sedentary Lifestyle':sedentary
                            }
            # dictionary_data = {"Pregnancies": preganancies, "Glucose": glucose, "BloodPressure": blood_pressure,
            #                    "SkinThickness": skin_thickness, "Insulin": insulin, "BMI": bmi, "DiabetesPedigreeFunction": dpf, "Age": age}

            x_test = pd.DataFrame(dictionary_data, index=[0])
            predict_gbst = model.predict(x_test)

            # print(predict_gbst)
            prediction_outcome = predict_gbst.tolist()[0]
            predict.result = prediction_outcome
            db.session.commit()
            if prediction_outcome == 1:
                return {'message': "You don't have GDM"}, HTTP_200_OK
            if prediction_outcome == 0:
                return {'message': 'You have GDM'}, HTTP_200_OK
        except Exception as e:
            return {"message":f"{e}{dictionary_data}"}
    


# dd