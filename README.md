# Northern Ireland Raspberry Jam Information System
NIJIS is a system built for the Northern Ireland Raspberry Jam to manage a number of aspects of our events. These include
- Workshop management/booking.
- Volunteer attendance to each Jam.
- Volunteer on the day management.
- Attendee management (for front desk).
- Fire list (who is in the building).

The current list of features, along with what is still be worked on can be found in the [Proposed spec](NIJIS-spec.md)   .

The system is based off Python 3, along with Flask, a MySQL DB, SQLAlchemy and the Eventbrite API library.    

## Installation   
To install, run the following command from inside the `ni_jam_information_system` folder.    
```
python3 setup.py install
```    

Then setup your MySQL database, using the model found in the database folder. Once setup, rename secrets/config_example.py to secrets/config.py and populate it.   

To start the project 
```bash
python3 main.py
```   

If running a full scale setup, it should be run by Gunicorn with a proxy in front (like Nginx).

# Screenshots
## Public schedule page
![](images/Public-schedule.jpg)
   
## Attendee workshop signup page
![](images/Attendee-workshops.jpg)
   
## Front desk attendee management page
![](images/Front-desk.jpg)
   
## Volunteer workshop signup page
![](images/Volunteer-signup.jpg)
   
## Workshop management page
![](images/Workshop-management.jpg)
