from flask import Flask, render_template, request
from csv import reader, writer
from shutil import move
from tempfile import NamedTemporaryFile

def read_dashboard():

  status_dashboard = []

  with open('dashboard.csv','r') as f:
    csv_reader = reader(f)
    for row in csv_reader:
      name, status = row
      status_dashboard.append({'name': name, 'status':status})
    
  return status_dashboard

def update_dashboard(button_value):
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

app = Flask(__name__)

@app.route("/")
def display_status_table():
    dashboard = read_dashboard()
    return render_template("index.html", dashboard=dashboard)
    
@app.route("/update", methods =['GET', 'POST'])
def update_page():
  if request.method == 'POST':
    button_value = request.form.get('update_button')
    update_dashboard(button_value) #Need to define this
    print(button_value)
    
  dashboard = read_dashboard()
  return render_template("update.html", dashboard=dashboard)
