
from pathlib import Path
from threading import Thread

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Scale
import time


# Get the current file's directory
OUTPUT_PATH = Path(__file__).parent

# Define the relative path to the assets folder
ASSETS_RELATIVE_PATH = Path("assets/frame0")

# Combine the output path with the relative assets path
ASSETS_PATH = OUTPUT_PATH / ASSETS_RELATIVE_PATH

# ...

# Function to get the full path for assets
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



# Define lap time variables
lap_start_time = 0
last_lap_start_time = 0
running = False  # Flag to indicate if the timer is running


def start_stop_timer():
    global running
    if running:
        running = False
    else:
        running = True
        start_new_lap()
        start_new_last_lap()
        update_timers()


def update_timers():
    if running:
        update_current_lap_timer()
        update_last_lap_timer()
        window.after(100, update_timers)


def start_new_lap():
    global lap_start_time
    lap_start_time = time.time()


def start_new_last_lap():
    global last_lap_start_time
    last_lap_start_time = time.time()


def update_current_lap_timer():
    current_lap_time = time.time() - lap_start_time
    formatted_time = format_time(current_lap_time)
    canvas.itemconfig(current_lap_text, text=formatted_time)


def update_last_lap_timer():
    last_lap_time = time.time() - last_lap_start_time
    formatted_time = format_time(last_lap_time)
    canvas.itemconfig(last_lap_text, text=formatted_time)


def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02}:{int(seconds):02}:{milliseconds:02}"





window = Tk()

window.geometry("800x480")
window.configure(bg = "#262626")
window.title("UWFE Dashboard")


canvas = Canvas(
    window,
    bg = "#262626",
    height = 480,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)


canvas.place(x = 0, y = 0)

charge_bar = canvas.create_rectangle(
    1.0,
    2.0,
    801.0,
    58.00000000000006,
    fill="#FF0000",
    outline="")


# Corrected Button creation
start_stop_button = Button(
    window,
    text="Start/Stop",
    font=("Lato Regular", 15),
    bg="#4CAF50",
    fg="black",
    command=start_stop_timer
)

# Position the button
start_stop_button.place(x=370, y=266)

soc_label = canvas.create_text(
    270.0,
    91.0,
    anchor="nw",
    text="SOC:",
    fill="#FFFFFF",
    font=("Lato Regular", 30 * -1)
)

soc_text = canvas.create_text(
    336.0,
    53.0,
    anchor="nw",
    text="100%",
    fill="#FFFFFF",
    font=("Lato Bold", 80 * -1)
)

def calculate_charge_color(charge):
    # Calculate a gradient from blue to red based on charge percentage
    r = int(255 * (1 - charge / 100))
    g = 0
    b = int(255 * (charge / 100))
    # Convert to hexadecimal color code
    color = "#{:02X}{:02X}{:02X}".format(r, g, b)
    return color

def update_battery_charge(value):
    # Convert value to an integer
    value = int(value)

    # Update the text
    canvas.itemconfig(soc_text, text=f"{value}%")

    # Calculate the color based on the charge percentage
    charge_color = calculate_charge_color(value)

    # Update the charge bar color
    canvas.itemconfig(charge_bar, fill=charge_color)

    # Update the bar at the top
    canvas.coords(charge_bar, 1.0, 2.0, 1.0 + (value / 100) * 800, 58.0)


battery_charge_slider = Scale(
    window,
    from_=0,
    to=100,
    orient="horizontal",
    length=200,  # Adjust the length as needed
    sliderlength=20,
    showvalue=0,
    command=update_battery_charge
)
battery_charge_slider.place(x=370, y=300)  # Adjust the position as needed

# Initial configuration of the battery charge
update_battery_charge(battery_charge_slider.get())


temp_bg1 = canvas.create_rectangle(
    0.0,
    58.0,
    196.0,
    150.0,
    fill="#7125BD",
    outline="")

temp_bg2 = canvas.create_rectangle(
    0.0,
    323.0,
    196.0,
    415.0,
    fill="#0C15EA",
    outline="")

temp_bg3 = canvas.create_rectangle(
    0.0,
    234.0,
    196.0,
    326.0,
    fill="#BA007B",
    outline="")

temp_bg4 = canvas.create_rectangle(
    0.0,
    147.0,
    196.0,
    239.0,
    fill="#FF0101",
    outline="")

battery_temp_label = canvas.create_text(
    4.0,
    62.0,
    anchor="nw",
    text="Battery Temp:",
    fill="#FFFFFF",
    font=("Lato Regular", 15 * -1)
)

motor_temp_label = canvas.create_text(
    4.0,
    150.0,
    anchor="nw",
    text="Motor Temp:",
    fill="#FFFFFF",
    font=("Lato Regular", 15 * -1)
)

inverter_temp_label = canvas.create_text(
    4.0,
    239.0,
    anchor="nw",
    text="Inverter Temp:",
    fill="#FFFFFF",
    font=("Lato Regular", 15 * -1)
)

water_temp_label = canvas.create_text(
    4.0,
    327.0,
    anchor="nw",
    text="Water Temp:",
    fill="#FFFFFF",
    font=("Lato Regular", 15 * -1)
)

battery_temp_text = canvas.create_text(
    6.0,
    76.0,
    anchor="nw",
    text="67.3°C",
    fill="#FFFFFF",
    font=("Lato Bold", 60 * -1)
)

motor_temp_text = canvas.create_text(
    7.0,
    163.0,
    anchor="nw",
    text="85.8°C",
    fill="#FFFFFF",
    font=("Lato Bold", 60 * -1)
)

inverter_temp_text = canvas.create_text(
    4.0,
    253.0,
    anchor="nw",
    text="79.9°C",
    fill="#FFFFFF",
    font=("Lato Bold", 60 * -1)
)

water_temp_text = canvas.create_text(
    4.0,
    340.0,
    anchor="nw",
    text="31.6°C",
    fill="#FFFFFF",
    font=("Lato Bold", 60 * -1)
)

deployment_label = canvas.create_text(
    235.0,
    139.0,
    anchor="nw",
    text="Deployment \n Last Lap:",
    fill="#FFFFFF",
    font=("Lato Bold", 20 * -1)
)

deployment_text = canvas.create_text(
    384.0,
    134.0,
    anchor="nw",
    text="4.8%",
    fill="#FFFFFF",
    font=("Lato Regular", 50 * -1)
)

speed_label = canvas.create_text(
    237.0,
    202.0,
    anchor="nw",
    text="Speed:",
    fill="#FFFFFF",
    font=("Lato Bold", 20 * -1)
)

speed_text = canvas.create_text(
    393.0,
    179.0,
    anchor="nw",
    text="34",
    fill="#FFFFFF",
    font=("Lato Regular", 50 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    410.0,
    473.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    178.0,
    496.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    642.0,
    455.0,
    image=image_image_3
)

border_rectangle1 = canvas.create_rectangle(
    603.0,
    58.0,
    799.0,
    128.0,
    fill="#6B6B6B",
    outline="#FFFFFF")

border_rectangle2 = canvas.create_rectangle(
    603.0,
    126.0,
    799.0,
    196.0,
    fill="#6B6B6B",
    outline="#FFFFFF")

border_rectangle3 = canvas.create_rectangle(
    603.0,
    193.0,
    799.0,
    263.0,
    fill="#6B6B6B",
    outline="#FFFFFF")

border_rectangle4 = canvas.create_rectangle(
    603.0,
    261.0,
    799.0,
    331.0,
    fill="#6B6B6B",
    outline="#FFFFFF")

vbatt_label = canvas.create_text(
    610.0,
    63.0,
    anchor="nw",
    text="V-Batt:",
    fill="#FFFFFF",
    font=("Lato Regular", 15 * -1)
)


mode_label = canvas.create_text(
    610.0,
    131.0,
    anchor="nw",
    text="Mode:",
    fill="#FFFFFF",
    font=("Lato Regular", 15 * -1)
)

lap_label = canvas.create_text(
    610.0,
    197.0,
    anchor="nw",
    text="Current Lap:",
    fill="#FFFFFF",
    font=("Lato Regular", 15 * -1)
)

lap_label2 = canvas.create_text(
    610.0,
    265.0,
    anchor="nw",
    text="Last Lap",
    fill="#FFFFFF",
    font=("Lato Regular", 15 * -1)
)

vbatt_text = canvas.create_text(
    651.0,
    77.0,
    anchor="nw",
    text="300V",
    fill="#FFFFFF",
    font=("Lato Bold", 40 * -1)
)

def changeMode():
    if(canvas.itemcget(mode_text, "text") == "RACE"):
        canvas.itemconfig(mode_text, text="SLOW")
    elif(canvas.itemcget(mode_text, "text") == "SLOW"):
        canvas.itemconfig(mode_text, text="RACE")

mode_button = Button(
    window,
    text="Mode",
    font=("Lato Regular", 15),
    bg="#4CAF50",
    fg="black",
    command=changeMode
)

# Position the button
mode_button.place(x=370, y=320)
    

mode_text = canvas.create_text(
    620.0,
    144.0,
    anchor="nw",
    text="RACE",
    fill="#FFFFFF",
    font=("Lato Bold", 40 * -1)
)

current_lap_text = canvas.create_text(
    621.0,
    212.0,
    anchor="nw",
    text="00:00:00",
    fill="#FFFFFF",
    font=("Lato Bold", 40 * -1)
)

last_lap_text = canvas.create_text(
    621.0,
    278.0,
    anchor="nw",
    text="00:00:00",
    fill="#FFFFFF",
    font=("Lato Bold", 40 * -1)
)

canvas.create_rectangle(
    8.0,
    429.0,
    95.0,
    482.0,
    fill="#1A1A1A",
    outline="")

canvas.create_rectangle(
    757.0,
    429.0,
    844.0,
    482.0,
    fill="#1A1A1A",
    outline="")

# Define temperature variables
battery_temp = 67.3
motor_temp = 85.8
inverter_temp = 79.9
water_temp = 31.6

# Function to simulate temperature increase
def increase_temps():
    global battery_temp, motor_temp, inverter_temp, water_temp
    while running:
        # Increase temperatures
        battery_temp += 0.1
        motor_temp += 0.2
        inverter_temp += 0.15
        water_temp += 0.05
        # Update temperature text on canvas
        update_temp_text()
        # Sleep for a short duration to control the rate of increase
        time.sleep(0.1)

# Function to simulate temperature decrease
def decrease_temps():
    global battery_temp, motor_temp, inverter_temp, water_temp
    while not running:
        # Decrease temperatures
        battery_temp -= 0.1
        motor_temp -= 0.2
        inverter_temp -= 0.15
        water_temp -= 0.05
        # Update temperature text on canvas
        update_temp_text()
        # Sleep for a short duration to control the rate of decrease
        time.sleep(0.1)

# Function to update temperature text on canvas
def update_temp_text():
    # Format temperatures and update text on canvas
    canvas.itemconfig(battery_temp_text, text=f"{battery_temp:.1f}°C")
    canvas.itemconfig(motor_temp_text, text=f"{motor_temp:.1f}°C")
    canvas.itemconfig(inverter_temp_text, text=f"{inverter_temp:.1f}°C")
    canvas.itemconfig(water_temp_text, text=f"{water_temp:.1f}°C")

# Function to start temperature simulation
def start_temp_simulation():
    # Create threads for temperature increase and decrease
    increase_thread = Thread(target=increase_temps)
    decrease_thread = Thread(target=decrease_temps)
    # Start the threads
    increase_thread.start()
    decrease_thread.start()

# Add a button to start temperature simulation
start_temp_button = Button(
    window,
    text="Start Temperature Simulation",
    font=("Lato Regular", 15),
    bg="#4CAF50",
    fg="black",
    command=start_temp_simulation
)

# Position the button
start_temp_button.place(x=370, y=350)



window.resizable(False, False)
update_timers()
window.mainloop()
