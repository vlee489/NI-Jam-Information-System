from wtforms import Form, BooleanField, StringField, PasswordField, IntegerField, TextAreaField, RadioField, SelectField, validators, HiddenField
from database import get_volunteers_to_select, get_workshops_to_select, get_individual_time_slots_to_select, get_workshop_rooms, get_workshop_from_workshop_id


class CreateWorkshopForm(Form):
    workshop_title = StringField("Workshop title", [validators.DataRequired()])
    workshop_description = TextAreaField("Workshop description", [validators.DataRequired()])
    workshop_limit = IntegerField("Workshop max attendees", [validators.DataRequired()])
    workshop_level = RadioField("Workshop level", choices=[("Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")])
    workshop_id = HiddenField("Workshop ID", default="")


class AddWorkshopToJam(Form):
    workshop = SelectField("Workshop", choices=get_workshops_to_select())
    volunteer = SelectField("Coordinator", choices=get_volunteers_to_select())
    slot = SelectField("Time slot", choices=get_individual_time_slots_to_select())
    room = SelectField("Room", choices=get_workshop_rooms())
    pilot = SelectField("Pilot", choices=[("False", "False"), ("True", "True")])

    def __init__(self, *args, **kwargs):
        super(AddWorkshopToJam, self).__init__(*args, **kwargs)
        self.workshop.choices = [(workshop.workshop_id, workshop.workshop_title) for workshop in get_workshops_to_select()]
        self.volunteer.choices = [(-1, "None")] + get_volunteers_to_select()
        self.room.choices = get_workshop_rooms()


class GetOrderIDForm(Form):
    order_id = IntegerField("Order ID", [validators.DataRequired()])
    day_password = StringField("Jam password", [validators.DataRequired()])


class LoginForm(Form):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])


class RegisterUserForm(Form):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    first_name = StringField("First name", [validators.DataRequired()])
    surname = StringField("Surname", [validators.DataRequired()])
    access_code = StringField("Access code", [validators.DataRequired()])
    email = StringField("Email address - Note must be same used for Slack", [validators.DataRequired()])

    # Added ready to add to Login form itself on page.


class VolunteerAttendance(Form):
    attending_jam = SelectField("Attending Main Jam", choices=[("False", "False"), ("True", "True")])
    attending_setup = SelectField("Attending Setup", choices=[("False", "False"), ("True", "True")])
    attending_packdown = SelectField("Attending Packdown", choices=[("False", "False"), ("True", "True")])
    attending_food = SelectField("Attending Food After", choices=[("False", "False"), ("True", "True")])
    notes = TextAreaField("Notes")
