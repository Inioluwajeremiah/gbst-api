from flask import Blueprint, request
from app.databaseModel import db, User, Predict, Notifications
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user
from datetime import date
from flask_mail import Message
from app import mail

notification_blueprint = Blueprint("notification", __name__)

"""
check if the user has checked his blood pressure and send email if they haven't - do this thrice per day
also save this response incookies and display in flatlist in notifications screen
"""

# send code to email
def sendEmail(eml, message):
    msg = Message("Notification", recipients=[eml])
    logo_url = "https://firebasestorage.googleapis.com/v0/b/gbst-cc5c3.appspot.com/o/icon3.png?alt=media&token=0e87eed5-9ea1-4fa7-8b46-0fd0a10b9c81"
    msg.html = f"""
                <div style='background-color:#f0efef; padding: 2rem 1rem;'>
                    <div style='background-color:#fff; max-width:32rem; width:90%; margin: 2rem auto; padding: 2rem 1rem'> 
                        <div style='display:flex; align-items:center; justify-items:center;'>
                            <img src={logo_url} alt="virtual church logo" style="width:5rem; height:5rem;"/>
                            <h1> <a href="" style='color:#66CA98; font-size:1.5em;'>GBST</a></h1>
                        </div>
                        <h3 style='padding:5px 2px; font-size:2em'>Notification</h3> 
                        <p style='font-size:1.2em;'>Thank you for subscribing to our service. Your health is our priority!</p> 
                        <p style=" font-size:1.2em;">
                           {message}
                        </p> 
                        
                    </div>
                </div>
            """
    mail.send(msg)


"""
    send email rhrice per day "9,15,19 i.e 9,3,7
    using flask_apscheduler
"""

"""
    second case scenario, allow the admin to send notifcations,
    check if user is admin and then query the prediction table
"""

# send notification
@notification_blueprint.post('/')
@login_required
def admin_notification():
    current_date = date.today()
    current_date_str = current_date.strftime("%Y-%m-%d")

    # get admin user
    admin_user = User.query.filter_by(id=current_user.id, email='adewarainioluwa@gmail.com').first()

    if not admin_user:
       return{"message":"Unauthorized access"}, HTTP_400_BAD_REQUEST

    if admin_user:
        # get all verified users
        verified_users = User.query.filter_by(is_verified=True).all()
        # get users with prediction
        predictions = Predict.query.filter_by(date=current_date).all()

        
        # set comprehension to create set of user id
        prediction_user_ids = {prediction.user_id for prediction in predictions}
        
        for verified_user in verified_users:
            if verified_user.id not in prediction_user_ids:
                email = verified_user.email
                message = "We would like to inform you that you have not checked your Gestational Blood Sugar status. Kindly do so in order to keep up with your schedule."
                sendEmail(email, message)
                # notifications table
                notifications = Notifications(notification=message, user_id=verified_user.id)
                db.session.add(notifications)
                db.session.commit()
                return {"message": f"Notification sent to {email}"}, HTTP_200_OK
            return{"message":"All users already tested their GDM"}, HTTP_200_OK
        return {"message": "Invalid request"}, HTTP_400_BAD_REQUEST
        

# retrieve saved notifications
@notification_blueprint.get('/')
@login_required
def get_notifications():
    notifications = Notifications.query.filter_by(user_id = current_user.id).all()

    if not notifications:
        return {"message": "No notification"}
    if notifications:
        notifications_data = [
            {'id': notification.id, 'notification': notification.notification, "user_id": notification.user_id, "date": notification.date} 
            for notification in notifications
        ]

        return {"message": "Notifications retrieved successfully", "data": notifications_data}, HTTP_200_OK
    # return {"message": "Invalid request"}, HTTP_400_BAD_REQUEST

# delete notification
@notification_blueprint.delete('/')
@login_required
def delete_notification():

    items = request.json['items']
    user_id = current_user.id
    notifications = Notifications.query.filter_by(user_d=user_id).all()

    for nots in notifications:
        if nots.id in items:
            notification = Notifications.query.get(nots.id)
            db.session.delete(notification)
            db.session.commit()
            return {"message": "Record deleted successsfully"}
        return{"message": "Record not found"}





