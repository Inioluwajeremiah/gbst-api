from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from .config import Config
from flask_login import LoginManager
from datetime import timedelta

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(test_config)


    # CORS(app,  resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
    db.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.remember_cookie_duration = timedelta(days=30)
    from .databaseModel import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.get('/')
    def home():
        return "GBST APP"

    # import blueprints
    from .routes.bloodsugarTest import  blood_sugar_test_blueprint
    from .routes.childbirthOutcome import child_birth_outcome_blueprint
    from .routes.clinicalHistory import clinical_history_blueprint
    from .routes.diet import diet_blueprint
    from .routes.enrollment import enrollment_blueprint
    from .routes.exercise import exercise_blueprint
    from .routes.FetalKickCount import fetal_kick_count_blueprint
    from .routes.medicalHistory import medical_history_blueprint
    from .routes.obstetricInformation import obstetric_information_blueprint
    from .routes.predict import predict_blueprint
    from .routes.profile import profile_blueprint
    from .routes.signup import  signup_blueprint
    from .routes.signin import  signin_blueprint
    from .routes.signout import signout_blueprint
    from .routes.verify import verify_blueprint

     # Register blueprints
    app.register_blueprint(blood_sugar_test_blueprint, url_prefix="/blood_sugar_test")
    app.register_blueprint(child_birth_outcome_blueprint, url_prefix="/child_birth_outcome")
    app.register_blueprint(clinical_history_blueprint, url_prefix="/clinical_history")
    app.register_blueprint(diet_blueprint, url_prefix="/diet")
    app.register_blueprint(enrollment_blueprint, url_prefix="/enrollment")
    app.register_blueprint(exercise_blueprint, url_prefix="/exercise")
    app.register_blueprint(fetal_kick_count_blueprint, url_prefix="/fetal_kick_count")
    app.register_blueprint(medical_history_blueprint, url_prefix="/medical_history")
    app.register_blueprint(obstetric_information_blueprint, url_prefix="/obstetric_information")
    app.register_blueprint(predict_blueprint , url_prefix="/predict")
    app.register_blueprint(profile_blueprint , url_prefix="/profile")
    app.register_blueprint(signup_blueprint, url_prefix="/signup")
    app.register_blueprint(signin_blueprint, url_prefix='/signin')
    app.register_blueprint(signout_blueprint, url_prefix='/signout')
    app.register_blueprint(verify_blueprint, url_prefix="/verify")


    return app

