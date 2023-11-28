from datetime import datetime

def GenerateLayout(GUI, bodies):
    months = list(range(1,13))
    days = list(range(1,32))
    Hours = list(range(0, 24))
    Mins = list(range(0, 60))
    secs = list(range(0, 60))
    yearMin = int(datetime.now().strftime("%Y"))- 3
    yearMax = yearMin + 7
    year = list(range(yearMin, yearMax))

    # Configures the layout of the screen
    layout = [  
                # Displays Angle and tracking data
                [GUI.Text('Azimuth: 0', key='Horz_Dis') ,GUI.Text('Elivation: 0', key='Vert_Dis') ,GUI.Text('Tracking Active: False', key='Track_Dis')],
                # Formats planet input
                [GUI.Text('Select Planet:'), GUI.Combo(bodies, key="Planet")],
                [
                    #Formats Angle inputs
                    GUI.Checkbox("Check Use Angle Entry", key="Ang_active", enable_events=True), GUI.Text('Enter Azimuth:'), GUI.InputText(key='Horizontial', size=(8,1)),
                    GUI.Text('Enter Elivation:'), GUI.InputText(key='Vertical', size=(8,1))
                ],
                # GUI layout for for GPS
                [GUI.Checkbox("Clarkson's GPS", key="CU_GPS_active", enable_events=True)],
                [
                    GUI.Text("Enter GPS"), GUI.Text("LAT"), GUI.InputText(key='LAT', size=(6,1)), GUI.Text("LON"), 
                    GUI.InputText(key='LON', size=(6,1)), GUI.Text("ALT"), GUI.InputText(key='ALT', size=(6,1))
                ],
                # Ckeck box for current time 
                [GUI.Checkbox("Use current date and time:", key="Current_time", enable_events=True)],
                
                # GUI layout for date and time 
                [
                    GUI.Text("Enter Date"), 
                    GUI.Text("Month"), GUI.Combo(months, key='Month'),
                    GUI.Text("Day"), GUI.Combo(days, key='Day'),
                    GUI.Text("Year"), GUI.Combo(year, key='Year'),
                    GUI.Text("Hour"), GUI.Combo(Hours, key='Hour'),
                    GUI.Text("Min"), GUI.Combo( Mins, key='Min'),
                    GUI.Text("Sec"), GUI.Combo(secs, key='Sec'),
                ],
                # Button to enter the input, start and end tracking
                [GUI.Button('Enter'),GUI.Button('Start Tracking'), GUI.Button('Cancel Tracking')],
                #Terminates the program
                [GUI.Button("Terminate Program")]
            ]
    return layout


def CreateWindow(GUI, name, layout, margin):
    window = GUI.Window(name, layout, margins=(margin[0], margin[1])) # Window creation
    return window

