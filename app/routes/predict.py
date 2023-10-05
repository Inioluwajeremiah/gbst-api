from flask import jsonify, Blueprint
from app.databaseModel import db, User, Enrollment, MedicalHistory, ClinicalHistory, ChildBirthOutcome, ObstetricInformation, Predict
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user
import pickle
import pandas as pd
from datetime import date

from datetime import date
from flask_mail import Message
from app import mail
predict_blueprint = Blueprint("predict", __name__)

# send code to email
def sendEmail(eml, result):
    msg = Message("Notification", recipients=[eml])
    logo_url = "https://firebasestorage.googleapis.com/v0/b/gbst-cc5c3.appspot.com/o/icon3.png?alt=media&token=0e87eed5-9ea1-4fa7-8b46-0fd0a10b9c81"
    msg.html = f"""
                <div style='background-color:#f0efef; padding: 2rem 1rem;'>
                    <div style='background-color:#fff; max-width:32rem; width:90%; margin: 2rem auto; padding: 2rem 1rem'> 
                        <div style='display:flex; align-items:center; justify-items:center;'>
                            <img src={logo_url} alt="virtual church logo" style="width:5rem; height:5rem;"/>
                            <h1> <a href="" style='color:#66CA98; font-size:1.5em;'>GBST</a></h1>
                        </div>
                        <h3 style='padding:5px 2px; font-size:2em'>Result Notification</h3> 
                        <p style='font-size:1.2em;'>Thank you for subscribing to our service. Your health is our priority!</p> 
                        <p style="font-size:1.2em;">
                            {result}
                        </p> 
                        
                    </div>
                </div>
            """
    mail.send(msg)


@predict_blueprint.get('/')
@login_required
def predict():
    
    model = pickle.load(open('model.pkl', 'rb'))
    current_date = date.today()
    current_date_str = current_date.strftime("%Y-%m-%d")

    user_id = current_user.id

    user = User.query.filter_by(id=user_id).first()
    childBirthOutcome = ChildBirthOutcome.query.filter_by(user_id=user_id,date=current_date_str).first()
    medicalHistory = MedicalHistory.query.filter_by(user_id=user_id).first()
    clinicalHistory = ClinicalHistory.query.filter_by(user_id=user_id).first()
    enrollment = Enrollment.query.filter_by(user_id=user_id).first()
    obstetricInformation = ObstetricInformation.query.filter_by(user_id=user_id).first()
    

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
                message = "Your result shows that you don't have GDM"
                sendEmail(user.email, message)
                return {'message': "You don't have GDM"}, HTTP_200_OK
                
            if prediction_outcome == 0:
                message = "Your result shows that you have GDM"
                sendEmail(user.email, message)
                return {'message': 'You have GDM'}, HTTP_200_OK
        except Exception as e:
            return {"message":f"{e}{dictionary_data}"}
    


# dd