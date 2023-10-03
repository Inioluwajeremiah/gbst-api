from flask import Blueprint, request
from markupsafe import Markup
from app.databaseModel import db, MedicalHistory
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user
from app import create_app
import eventlet
from rq import Queue
from redis import Redis

app, socketio = create_app()
queue = Queue(connection=Redis())
eventlet.monkey_patch() 

notification_blueprint = Blueprint("notification", __name__)

@socketio.on('connect')
def connect():
    print('@socketio.on("connect")')

def push_notification(data):
    socketio.emit("notifications", data)

@notification_blueprint.get('/')
def notification():
    data = {"nessage":"You have not checked your blood sugar today"}
    result = queue.enqueue(push_notification, data)
    return {"message": "Notification sent successfully"}