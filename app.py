# import libraries
import os
from forms.forms import SafetyModule1, SafetyModule2, DeleteFromSafety, LoginForm, RegistrationForm, DisasterForm, SiteLogIn, HealthRiskForm
from models.model import safety_questionnaire_database, db, login_manager, User, CouncilDisasterData
from flask import Flask, render_template, url_for, redirect, session, flash, abort, request, jsonify
from flask_sqlalchemy import SQLAlchemy
#database migrate import
from flask_migrate import Migrate
from flask_login import login_user, login_required, logout_user
from io import TextIOWrapper
import csv
import pickle
##importing the machine learning libraries
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
# dataset spliting
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

#imports ended
########################################################################################################
#configuring the application for the secret key and database related sqlalchemy
app = Flask(__name__)
#app.config["GEOIPIFY_API_KEY"] = "at_m1iB0SYZsloy7l3LldR1GelQpnLQO"
#configure the secret key

app.config['SECRET_KEY'] = '45363125e0c551946d961ef0'

#set the base directory for the flask database
basedir = os.path.abspath(os.path.dirname(__file__))

#setup the database uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
#turn off track modifications for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## configuring the SimpleGeoIP
##simple_geoip = SimpleGeoIP(app)

#create a db instance
db.init_app(app)
#migrate db with app
Migrate(app,db)

#configure the login manager
login_manager.init_app(app)
login_manager.login_view = 'login'



########################################################################################################
#view for the main page
#@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

########################################################################################################
#site login
@app.route('/')
@app.route('/siteentry',methods=['GET','POST'])
def siteentry():
    form = SiteLogIn()
    if form.validate_on_submit():
        entered_data = form.password.data
        if entered_data == "superman":
            return redirect('index')
        else:
            return render_template('siteentry.html', form=form)
    return render_template('siteentry.html', form=form)




########################################################################################################
########################################################################################################
#view for the general home safety page
#@app.route('/generalsafety')
#def generalsafety():
#    return render_template('generalsafetyrecommendation.html',title='General Safety')


########################################################################################################
#view for the physical condition questionnaire page
@app.route('/physicalcondition',methods=['GET','POST'])
def module1():
    form = SafetyModule1()

    if form.validate_on_submit():
        # get the data in the session object for the client side
        session['physicalcondition_risk'] = 'No'
        session['kid_name'] = form.kid_name.data
        session['unsteady_standing'] = form.unsteady_standing.data
        ##use the bmi in conjuction with the unsteady standing to find risk factor

        if session['unsteady_standing'] == "Yes":
            session['physicalcondition_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 12)
                ###########################################################
            else:
                session['risk_value'] = str(int(session['risk_value']) + 6)


        session['kitchen_reach'] = form.kitchen_reach.data

        #calcultate the risk factor for the kitchen reach
        ###################################################
        if session['kitchen_reach'] == "No":
            session['physicalcondition_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 3)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 2)

        ###################################################
        if form.stairs_present == "Yes":
            session['stairs_present'] = "Yes"
            session['stairs_handrails'] = form.stairs_handrails.data
        else:
            session['stairs_present'] = "No"
            session['stairs_handrails'] = "None"


        print("session stairs present is ", session["stairs_present"])
        print("handrails present is",session['stairs_handrails'])
        #calculate the risk for handrails here
        ###################################################
        if session['stairs_handrails'] == "No":
            session['physicalcondition_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 3)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 2)

        ###################################################
        #session['stairs_handrails'] = form.stairs_handrails.data
        session['walk_difficulty'] = form.walk_difficulty.data
        #calculate the risk for walking difficulty here
        ###################################################
        if session['walk_difficulty'] == "Yes":
            session['physicalcondition_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 12)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 6)

        ###################################################
        session['difficulty_chair'] = form.difficulty_chair.data

        #calculate the risk for handrails here
        ###################################################
        if session['difficulty_chair'] == "No":
            session['physicalcondition_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 12)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 6)

        ###################################################
        session['emergency_contact'] = form.emergency_contact.data

        ###################################################
        if session['emergency_contact'] == "No":
            session['physicalcondition_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 8)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 4)

        ###################################################
        print(session['risk_value'])
        return redirect(url_for('module2'))

    #render the template for the current view
    else:
        flash('All Fields are required.')
        return render_template('module1.html', form=form)
    return render_template('module1.html', form=form, title='Physical Condition')


###########################################################################################################
#view for the house safety questionnaire page
@app.route('/housesafety',methods=['GET','POST'])
def module2():
    form = SafetyModule2()

    if form.validate_on_submit() and request.method == 'POST':
        session['house_risk'] = 'No'

        # session['water_presence'] = form.water_presence.data
        print(request.form.getlist('wet_option'))
        if "Yes" in request.form.getlist('wet_option'):
            session['water_presence'] = "Yes"
        else:
            session['water_presence'] = "No"
        ###################################################
        #update the risk for having the water resence
        if session['water_presence'] == "Yes":
            session['house_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 2)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 1)

        ###################################################
        session['slip_products'] = form.slip_products.data
        ###################################################
        #update risk for having the slip products
        if session['slip_products'] == "Yes":
            session['house_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 3)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 1)

        ###################################################
        session['electrical_cords'] = form.electrical_cords.data
        ###################################################
        #update risk for having the electrical cords
        if session['electrical_cords'] == "Yes":
            session['house_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 2)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 1)

        ###################################################
        session['path_checked'] = form.path_checked.data
        ###################################################
        #update risks for having the path cracked
        if session['path_checked'] == "Yes":
            session['house_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 2)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 1)

        ###################################################
        session['adequate_light'] = form.adequate_light.data
        ###################################################
        #risk for adequate lighting
        if session['adequate_light'] == "No":
            session['house_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 2)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 1)

        ###################################################
        session['grab_bars'] = form.grab_bars.data
        ###################################################
        #risks for grab bars
        if session['grab_bars'] == "No":
            session['house_risk'] = 'Yes'
            if session['bmi'] == 'underweight' or session['bmi'] == "obese":
                session['risk_value'] = str(int(session['risk_value']) + 3)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 1)

        ###################################################
        session['smoke_detector'] = form.smoke_detector.data
        ###################################################
        #risk of smoking and smoke detectors
        if session['smoke_detector'] == "No":
            session['house_risk'] = 'Yes'
            if session['smoke'] == 'yes':
                session['risk_value'] = str(int(session['risk_value']) + 3)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 1)

        ###################################################
        session['fire_extinguisher'] = form.fire_extinguisher.data
        ###################################################
        #risks for fire extinguisher and smoke
        if session['fire_extinguisher'] == "No":
            session['house_risk'] = 'Yes'
            if session['smoke'] == 'yes':
                session['risk_value'] = str(int(session['risk_value']) + 3)

            else:
                session['risk_value'] = str(int(session['risk_value']) + 1)

        ###################################################
        if int(session['risk_value']) > 60:
            session['risk_factor'] = "High Risk"
        elif int(session['risk_value']) >=30 and int(session['risk_value']) <=60:
            session['risk_factor'] = "Medium Risk"
        else:
            session['risk_factor'] = "Low Risk"
        return redirect(url_for('recommendation_menu'))

    #render the template for the current view
    else:
        return render_template('module2.html', form=form)
    return render_template('module2.html', form=form)


########################################################################################################

#render template for safety questionnaire feedback
#@app.route('/safety_questionnaire_feedback')
#def safety_questionnaire_feedback():
#    return render_template('safety_questionnaire_feedback.html')

########################################################################################################
#page to query the database and check whether entries are pushing or not
@app.route('/safety_questionnaire_query')
# @login_required
def safety_questionnaire_query():
    questionnaire = safety_questionnaire_database.query.all()[-5:]#list only the last five records inserted in the table
    return render_template('safety_questionnaire_answers.html',questionnaire= questionnaire)

########################################################################################################
#template to delete all the data in the safety questionnaire table
@app.route('/delete_questionnaire_data',methods=['GET','POST'])
# @login_required
def delete_questionnaire():
    form = DeleteFromSafety()
    if form.validate_on_submit():
        try:
            db.session.query(safety_questionnaire_database).delete()
            db.session.commit()
        except:
            db.session.rollback()
    return render_template('delete_questionnaire_data.html', form = form)


########################################################################################################
#view that will be seen by when user logins to the system
@app.route('/welcome')
# @login_required
def welcome_user():
    return render_template('welcome_user.html')

########################################################################################################
#logout view for the admin
@app.route('/logout')
# @login_required
def logout():
    logout_user()
    flash("You are logged Out")
    return redirect(url_for('index'))

########################################################################################################
#login view for the system administrator
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Login Sucessfully')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next =url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)


########################################################################################################
#view for the admin to create another administrator
@app.route('/register',methods=['GET','POST'])
# @login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("thank you for registering")
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

########################################################################################################
#view for inserting the council d  ata by the system administrator into the CouncilDisasterData
@app.route('/uploadcouncildisaster', methods=['GET','POST'])
# @login_required
def uploadcouncildisaster():
    print(CouncilDisasterData.query.all()[-1:])
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file.save(os.path.join(basedir, csv_file.filename))
        with open(csv_file.filename,'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                council_data = CouncilDisasterData(council = row[0], postcode=row[1], calamity_1 = row[2], calamity_1_severity = row[3],  calamity_2 = row[4], calamity_2_severity = row[5], calamity_3 = row[6], calamity_3_severity = row[7], calamity_4 = row[8], calamity_4_severity = row[9])
                db.session.add(council_data)
                db.session.commit()
        return redirect(url_for('uploadcouncildisaster'))
    return render_template('uploadcouncildisaster.html')

#query all the council query data
########################################################################################################
@app.route('/councilquery')
# @login_required
def councilquery():
    councildata = CouncilDisasterData.query.all()[0:5]#list only the last five records inserted in the table
    return render_template('councilquery.html',councildata= councildata)

########################################################################################################
#view for the council select page for natural disasters
@app.route('/safetybycouncil',methods=['GET','POST'])
def safetybycouncil():
    form = DisasterForm()
    CouncilDisasterData.query.filter(CouncilDisasterData.council == 'ï»¿Melbourne').update({"council":"Melbourne"})
    db.session.commit()
    form.postcode.choices = [(c.postcode,c.postcode) for c in CouncilDisasterData.query.with_entities(CouncilDisasterData.postcode).all()]
    if form.validate_on_submit():
        postcode_input = form.postcode.data
        queried_data = CouncilDisasterData.query.filter_by(postcode = postcode_input).first()
        session['postcode'] = queried_data.postcode
        session['calamity_1'] = queried_data.calamity_1
        session['calamity_2'] = queried_data.calamity_2
        session['calamity_3'] = queried_data.calamity_3
        session['calamity_4'] = queried_data.calamity_4
        session['calamity_1_severity'] = queried_data.calamity_1_severity
        session['calamity_2_severity'] = queried_data.calamity_2_severity
        session['calamity_3_severity'] = queried_data.calamity_3_severity
        session['calamity_4_severity'] = queried_data.calamity_4_severity
        return redirect(url_for('disasterrecommendation'))
    return render_template('safetybycouncil.html',form=form)


@app.route('/disasterrecommendation')
def disasterrecommendation():
    return render_template('disasterrecommendation.html')


########################################################################################################
#view to find the health risks
@app.route('/healthrisk',methods=['GET','POST'])
def healthrisk():
    form = HealthRiskForm()
    if form.validate_on_submit():
        session['health_risk'] = "No"
        #print("validation okkay")
        age = form.age.data
        gender = form.gender.data

        if form.height_unit.data == "Feets":
            feetdata = form.height_feet.data
            inchesdata = form.height_inches.data
            height = feetdata + float(0.1*inchesdata)

        elif form.height_unit.data == "Centimeters":
            height = 0.032*form.height_centimeters.data


        if form.weight_unit.data == "Pounds":
            pounds = form.weight_pounds.data
            weight = 0.45*pounds
        elif form.weight_unit.data == "Kilograms":
            weight = form.weight_kilograms.data

        distance = form.distance.data
        children = form.children.data
        smoke = form.smoke.data
        height_meters = (height/(3.2808))
        bmi = weight/(height_meters*height_meters)
        #session to store the distance
        session['walking_distance'] = form.distance.data

        if int(session['walking_distance'] ) < 1250:
            session['walking_habbits'] = "bad"
            session['health_risk'] = "Yes"
        else:
            session['walking_habbits'] = "good"

        #store the bmi category in the session variable
        if bmi < 18:
            session['bmi'] = "underweight"
            session['health_risk'] = "Yes"
        elif bmi > 30:
            session['bmi']  = "obese"
            session['health_risk'] = "Yes"
        else:
            session['bmi'] = 'normal'

        #store the smoking habbit in the session variable as well
        print(type(smoke))
        print(smoke)
        if smoke == '1':
            session['smoke_data'] = "yes"
            session['health_risk'] = "Yes"
        else:
            session['smoke_data'] = "no"
        #end of this session for smoke


        model = pickle.load(open('decision_tree_model.pkl','rb'))
        predicted_value = (model.predict([[age,gender,bmi,distance,children,smoke]])[0])
        # session['age'] = form.age.data
        session['gender'] = form.gender.data
        if form.gender.data == "0":
            session['grandparent_gender'] = "grandmother"
        else:
            session['grandparent_gender'] = "grandfather"

        session['smoke'] = form.smoke.data
        # session['height_meters'] = height_meters
        if predicted_value == 1:
            session['risk'] = "Yes"
            session['risk_value'] = 30
        elif predicted_value == 0:
            session['risk'] = "No"
            session['risk_value'] = 0
        print("risk value is ",session['risk_value'])
        return redirect(url_for('module1'))
    else:
        return render_template('healthrisk.html', form = form)
    return render_template('healthrisk.html', form = form)


########################################################################################################
#view to give health risk recommendation
@app.route('/healthriskfeedback')
def healthriskfeedback():
    return render_template('healthriskfeedback.html')

########################################################################################################
#view to give health condition recommendation
@app.route('/physicalconditionfeedback')
def physicalconditionfeedback():
    return render_template('physicalconditionfeedback.html')

########################################################################################################
#view to give house safety recommendation
@app.route('/housesafetyfeedback')
def housesafetyfeedback():
    return render_template('housesafetyfeedback.html')

########################################################################################################
#view page for recommendation menu
@app.route('/recommendation_menu')
def recommendation_menu():
    return render_template('recommendation_menu.html')

########################################################################################################
########################################################################################################
#default page error hander
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))


########################################################################################################
#run the main file
if __name__ == '__main__':
    app.run(debug=True)
