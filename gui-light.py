
from threading import Thread

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Scale
import time

window = Tk()

window.geometry("800x480")
window.configure(bg = "#262626")
window.title("UWFE Dashboard (LIGHT)")


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

window.resizable(False, False)
window.mainloop()
