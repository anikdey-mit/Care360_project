#forms.py
#import the forms library
from flask_wtf import FlaskForm
from wtforms import (StringField,BooleanField,DateTimeField,
                    RadioField,SelectField,TextField,TextAreaField,
                    SubmitField, PasswordField, SelectMultipleField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
#import the  validators that will be required to build the application
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

class SafetyQuestionnaireForm(FlaskForm):
    #create the forms details
    kid_name = StringField('Please enter your name.',validators=[DataRequired()])

    unsteady_standing = RadioField('Do you notice your grandparents stumble or shake while they are standing?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    water_presence = SelectField('Do you think which of these areas in your grandparent\'s house is always wet?',
                        choices=[('Stairs','Stairs'),('Bathroom','Bathroom'),('Kitchen','Kitchen'), ('Garden','Garden'), ('Others','Others'), ('None of above','None of above')], validators=[DataRequired()])

    kitchen_reach = RadioField('Do you think your grandparents can reach things easily in the kitchen?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    slip_products = RadioField('Do you see slippery products like mats, rugs in your grandparent\'s house?',
                        choices=[('Yes','Yes'),('No','No')], validators=[DataRequired()])

    electrical_cords = SelectField('Do you see electrical cords of the following appliances running across your grandparent\'s house?',
                    choices =[('Lamp','Lamp'),('Extension Cables','Extension Cables'), ('Charging wires','Charging wires'),
                    ('Vaccum Cleaner','Vaccum Cleaner'), ('None of above','None of above')],validators=[DataRequired()])

    stairs_handrails = RadioField('Do you think there are handrails for stairs in your grandparent\'s house?',
                        choices=[('Yes','Yes'),('No','No')], validators=[DataRequired()])

    path_checked = RadioField('Do you think the paths around your grandparent\'s house are cracked?',
                        choices=[('Yes','Yes'),('No','No')], validators=[DataRequired()])

    adequate_light = RadioField('Do you notice adequate lighting all over your grandparent\'s house?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    walk_difficulty = RadioField('Do you see your grandparent\'s struggle while walking?',
                        choices=[('Yes','Yes'),('No','No')], validators=[DataRequired()])

    grab_bars = RadioField('Do you see grab bars in your grandparent\'s bathroom?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    difficulty_chair = RadioField('Do you see your grandparents having difficulty getting out of a chair or couch?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    stairs_condition = RadioField('Do you think the stairs at your grandparent\'s house are slippery?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    smoke_detector = RadioField('Are smoke detectors installed and working properly in your grandparent\'s house?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    fire_extinguisher = RadioField('Is there a fire extinguisher in your grandparent\'s kitchen?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    emergency_contact =  RadioField('Ask your grandparent\'s if they have some emergency contact details with them?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])


    submit = SubmitField('Submit Safety Assesment Questonnaire')

#form for deleting the data from the safety questionnaire table
class DeleteFromSafety(FlaskForm):
    submit = SubmitField('Clear all the data in the table')


#create a login form for the system administrator to login and perform CRUD operation son the database
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

#add the registration form for the user
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists!')

class DisasterForm(FlaskForm):
    council_name = SelectField('Select Council Area',validators=[DataRequired()])
    submit = SubmitField('Submit')
