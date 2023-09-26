"""
    note that if data are to be taken periodically,
    the user_id in each table shoud be set to unique=False

    for the periodical prediction, add date to each table then
    filter by user_id and date to get the different records of each
    user and the different dates which can then be filtered to 
    get date specifically wanted 

    let users be aware that readings will be taken every two 
    weeks after registration. send alerts to them and also notification
    on the app using the notification screen. this will allow them to
    fill appropriate data

"""
"""
        as per the prediction, add date to each database table by default.
        to make a new prediction, first check for the date of the previous
        prediction, then use the date to filter the data needed, for making new
        predictions. that will be last_date_of_prediction + two_weeks.
        Then make the new prediction, date field should be automatically saved
        in the prediction table 

        also on the prediction, it should be a 'block-prediction' in the sense
        that previous data used for the various predictions within a two-week
        timeframe will not be used again after that two weeks. i.e users can
        make various predictions within two weeks using fresh data for that 
        two weeks. Not using data from the previous two weeks then making
        new preictions say data from 2.1 weeks, 3 weeks 2days, no.

        so the data will then be compared after the project and the result, 
        I think this the summary of the entire project


        NB => forget two weeks, predict each time a user enters the appropriate data
        it should be a daily exercise, alert the user if he fails to do so.
        just filter the X_test data by the current date and predict by the current date
"""

"""

def predict():
    # Pregnancies	Glucose	BloodPressure	SkinThickness	Insulin	BMI	DiabetesPedigreeFunction	Age
    model = pickle.load(open('model.pkl', 'rb'))
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
        dictionary_data = {'Case Number': 1, 'Age': , 'No of Pregnancy': , 'Gestation in previous Pregnancy': ,
                           'BMI': , 'HDL': , 'Family History': , 'unexplained prenetal loss': , 
                            'Large Child or Birth Default': , 'PCOS': , 'Sys BP': ,  'Dia BP': ,  
                            'OGTT': , 'Hemoglobin': , 'Sedentary Lifestyle'
                        }
        # dictionary_data = {"Pregnancies": preganancies, "Glucose": glucose, "BloodPressure": blood_pressure,
        #                    "SkinThickness": skin_thickness, "Insulin": insulin, "BMI": bmi, "DiabetesPedigreeFunction": dpf, "Age": age}

        x_test = pd.DataFrame(dictionary_data, index=[0])
        predict_gbst = model.predict(x_test)

        print(predict_gbst)
        return jsonify({'result': predict_gbst.tolist()[0]})
    


# dd
"""
