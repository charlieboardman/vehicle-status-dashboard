from flask import Flask, render_template, request
from csv import reader, writer
from shutil import move
from tempfile import NamedTemporaryFile
from datetime import datetime
from calendar import month_abbr
from time import strftime

def read_dashboard():

    status_dashboard = []
    
    with open('dashboard.csv','r') as f:
        csv_reader = reader(f)
        for row in csv_reader:
            name, status = row
            status_dashboard.append({'name': name, 'status':status})
        
    
    return status_dashboard

def update_dashboard(button_value,update_time):
    update_info = button_value.split(',')
    
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')
    
    with open('dashboard.csv','r') as csvfile, tempfile:
        csv_reader = reader(csvfile)
        csv_writer = writer(tempfile)
        
        for row in csv_reader:
            if row[0] == update_info[0]: #Check for the vehicle we wish to update
                row = update_info #Replace the row with the new status
            csv_writer.writerow(row)
            
    move(tempfile.name, 'dashboard.csv')
    
    last_updated = update_time
    
    with open('history.csv','a') as f:
        f.write(f"{last_updated},{update_info[0]},{update_info[1]}")
        f.write("\n")
        
    with open('last_update.txt','w') as f:
        f.write(f"{last_updated},{update_info[0]},{update_info[1]}")

app = Flask(__name__)

@app.route("/")
def display_status_table():
    dashboard = read_dashboard()
    with open('last_update.txt', 'r') as f:
        last = f.read().replace(',' , ', ')
        last_updated_msg = f"Last update: {last}"
    return render_template("index.html", dashboard=dashboard, last_update=last_updated_msg)
    
@app.route("/update", methods =['GET', 'POST'])
def update_page():
    if request.method == 'POST':
        button_value = request.form.get('update_button')
        
        #Get the date and time the last update happened
        update_time = datetime.now().strftime('%a,%d %b %Y,%I:%M %p')
        
        update_dashboard(button_value,update_time)
        print(button_value)
    
    dashboard = read_dashboard()
    return render_template("update.html", dashboard=dashboard)
