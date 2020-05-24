#forms.py
#import the forms library
from flask_wtf import FlaskForm
from wtforms import (StringField,BooleanField,DateTimeField,
                    RadioField,SelectField,TextField,TextAreaField,
                    SubmitField, PasswordField, SelectMultipleField,IntegerField, FloatField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
#import the  validators that will be required to build the application
from wtforms.validators import DataRequired, EqualTo, NumberRange, Optional, Length
from wtforms import ValidationError

class SafetyModule1(FlaskForm):
    #create the forms details
    kid_name = StringField('Please enter your name.',validators=[DataRequired(), Length(max=20)], render_kw={'onchange': "name_verification()"})
    unsteady_standing = SelectField('What is the best statement that describes your granparent while they are standing?',
                    choices =[('Yes','Visibly Shaken'),('Yes','Hold to stroller'),('No','No diificulty while standing')],validators=[DataRequired()])

    kitchen_reach = RadioField('Do you notice your grandparents can reach things easily in the kitchen?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    stairs_present = SelectField('Are there stairs at your grandparents house?',
                        choices=[('No','No'),('Yes','Yes')], validators=[DataRequired()],render_kw={'onchange': "myFunction()"})

    stairs_handrails = RadioField('Do the stairs in your elderly house have handrails?',
                        choices=[('Yes','Yes'),('No','No')], validators=[Optional()])

    walk_difficulty = SelectField('How confident are your grandparents whil ethey are standing?',
                        choices=[('Yes','Not Confident'),('No','Confident')], validators=[DataRequired()])

    difficulty_chair = SelectField('How easy is it for your grandparents to get out of chair or couch?',
                    choices =[('Yes','Very easily on their own'),('Yes','Sometimes need help from people'), ('No','Can not manage easily')],validators=[DataRequired()])

    emergency_contact =  SelectField('Where do your grandparent keep their emergency contact details?',
                    choices =[('Yes','On mobile phone'),('Yes','In address book'), ('No','They have memorised')],validators=[DataRequired()])


    submit = SubmitField('Proceed to House Safety Assessment')


class SafetyModule2(FlaskForm):
    #create the forms details
    water_presence = SelectMultipleField('Do you notice which of these areas in your grandparent\'s house is always wet?',
                        choices=[('Yes','Bathroom'),('Yes','Kitchen'), ('Yes','Garden'), ('Yes','Others'), ('No','None of above')])

    slip_products = RadioField('Are there any rugs or mats in your grandparent\'s house',
                        choices=[('Yes','Yes'),('No','No')], validators=[DataRequired()])

    electrical_cords = SelectField('Do you notice electrical cords of the following appliances running across your grandparent\'s house?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    path_checked = RadioField('Do you notice the paths around your grandparent\'s house are cracked?',
                        choices=[('Yes','Yes'),('No','No')], validators=[DataRequired()])

    adequate_light = SelectField('Do you notice adequate lighting all over your grandparent\'s house?',
                    choices =[('Yes','Bright rooms with lots of outside light'),('Yes','Rooms have medium level of light'), ('No','Some rooms have low level of light')],validators=[DataRequired()])

    grab_bars = RadioField('Do you see grab bars in your grandparent\'s bathroom?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    smoke_detector = RadioField('Do your grandparent\'s house has smokde detector installed?',
                    choices =[('Yes','Yes it beeps three times'),('No','No, it doesn\'t make beep noise')],validators=[DataRequired()])

    fire_extinguisher = RadioField('Is there a fire extinguisher in your grandparent\'s kitchen?',
                    choices =[('Yes','Yes, fire extinguisher present.'),('No','No, fire extinguisher not present')],validators=[DataRequired()])

    submit = SubmitField('Proceed to Feedback')

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
    postcode = SelectField('Select Postcode',validators=[DataRequired()])
    submit = SubmitField('Submit')

#adding the login page at the start of the application itselves
class SiteLogIn(FlaskForm):
    password = PasswordField('Enter the Password', validators=[DataRequired()])
    submit = SubmitField('Go to website')

#, render_kw={'onchange': "genderFunction()"}

class HealthRiskForm(FlaskForm):
    age = IntegerField('',validators=[DataRequired(), NumberRange(min=1, max=100)],  render_kw={'onchange': "age_verification()"})
    gender = RadioField('Is this safety assessment for your grandmother or grandfather?',
                    choices =[('0','Grandmother'),('1','Grandfather')],validators=[DataRequired()])

    height_unit = SelectField('Select the unit to enter the height.',
                        choices=[('Feets','Feet'),('Centimeters','Centimeters')], validators=[DataRequired()], render_kw={'onchange': "height_function()"})

    height_feet = IntegerField('Enter the feets',validators=[Optional(), NumberRange(min=3, max=8)], render_kw={'onchange': "feet_verification()"})
    height_inches = IntegerField('Enter the inches',validators=[Optional(), NumberRange(min=1, max=12)], render_kw={'onchange': "inches_verification()"})
    height_centimeters = IntegerField('Enter the height in centimeters',validators=[Optional(), NumberRange(min=1, max=1000)], render_kw={'onchange': "centimeter_verification()"})

    #height = FloatField('What is your grandparent height?', validators=[DataRequired()])
    weight_unit = SelectField('Select the unit to enter the weight.',
                        choices=[('Pounds','Pounds'),('Kilograms','Kilograms')], validators=[DataRequired()], render_kw={'onchange': "weight_function()"})

    weight_pounds = IntegerField('Enter the weight in pounds',validators=[Optional()], render_kw={'onchange': "pound_verification()"})
    weight_kilograms = IntegerField('Enter the weight in kilograms',validators=[Optional()], render_kw={'onchange': "kilogram_verification()"})

    #weight = IntegerField('Please Enter your grandparents weight in kilograms.',validators=[DataRequired(), NumberRange(min=20, max=250)])
    distance = SelectField('Ask your grandmother/grandfather approximately how much do they walk every day in kilometers',
                        choices=[('600','Less than 1 KM everyday'),('1250','Approximately 1 KM everyday'),('2500','Approximately 2 KM everyday'), ('3750','Approximately 3 KM everyday'), ('5000','Approximately 4KM everyday'), ('7000','More than 5KM everyday'),('100','Do not walk at all'), ('300','Walk within the house')], validators=[DataRequired()])
    children = IntegerField('How many children does your grandparents have?',validators=[DataRequired(), NumberRange(min=1, max=10)], render_kw={'onchange': "child_verification()"})
    smoke = SelectField('Does your grandmother currently smoke or smoked in the last 2 years ?',
                    choices =[('1','Heavy Smoker'),('1','Social Smoker'), ('0','Non Smoker')],validators=[DataRequired()])
    submit = SubmitField('Proceed to Physical Condition Assessment')
