import cantools
import csv
import math
import sys
import threading
import time
from tkinter import Tk, Canvas, Button, Scale

from util import default_dbc_path, default_dtc_path
from connect.connect import QueueDataSubscriber

class DashboardApp:

    def __init__(self, master, queue_data):
        self.master = master
        self.queue_data = queue_data
        master.geometry("800x480")
        master.configure(bg="#262626")
        master.title("UWFE Dashboard (ULTRALIGHT)")

        self.canvas = Canvas(
            master,
            bg="#262626",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.soc_label = self.canvas.create_text(
            270.0,
            91.0,
            anchor="nw",
            text="SOC:",
            fill="#FFFFFF",
            font=("Lato Regular", 30 * -1)
        )

        self.soc_text = self.canvas.create_text(
            336.0,
            53.0,
            anchor="nw",
            text="100%",
            fill="#FFFFFF",
            font=("Lato Bold", 80 * -1)
        )

        self.charge_bar = self.canvas.create_rectangle(
            1.0,
            2.0,
            801.0,
            58.00000000000006,
            fill="#FF0000",
            outline="")

        self.battery_charge_slider = Scale(
            master,
            from_=0,
            to=100,
            orient="horizontal",
            length=200,
            sliderlength=20,
            showvalue=0,
            command=self.update_battery_charge
        )

        self.battery_charge_slider.place(x=370, y=300)

        CAN_data = self.queue_data.fetch()

        battery_val = CAN_data["battery"]

        self.update_battery_charge(battery_val)

        self.mode_button = Button(
            master,
            text="Mode",
            font=("Lato Regular", 15),
            bg="#4CAF50",
            fg="black",
            command=self.change_mode
        )

        self.mode_label = self.canvas.create_text(
            610.0,
            131.0,
            anchor="nw",
            text="Mode:",
            fill="#FFFFFF",
            font=("Lato Regular", 15 * -1)
        )

        self.mode_text = self.canvas.create_text(
            620.0,
            144.0,
            anchor="nw",
            text="RACE",
            fill="#FFFFFF",
            font=("Lato Bold", 40 * -1)
        )

        self.mode_button.place(x=370, y=320)

        master.resizable(False, False)

    def calculate_charge_colour(self, charge):
        r = int(255 * (1 - charge / 100))
        g = 0
        b = int(255 * (charge / 100))
        colour = "#{:02X}{:02X}{:02X}".format(r, g, b)
        return colour

    def update_battery_charge(self, value):
        value = int(value)
        self.canvas.itemconfig(self.soc_text, text=f"{value}%")
        charge_colour = self.calculate_charge_colour(value)
        self.canvas.itemconfig(self.charge_bar, fill=charge_colour)
        self.canvas.coords(self.charge_bar, 1.0, 2.0, 1.0 + (value / 100) * 800, 58.0)

    def change_mode(self):
        current_mode = self.canvas.itemcget(self.mode_text, "text")
        new_mode = "SLOW" if current_mode == "RACE" else "RACE"
        self.canvas.itemconfig(self.mode_text, text=new_mode)

class QueueData:
    """ Facilitates data transfer between the GUI and the Queue. """

    def __init__(self):
        self._lock = threading.Lock()
        self._data = {
            "dtc_message_payload": [],
            "speed": 0,
            "temperature": 0,
            "voltage": 0,
            "battery": 0
        }

    def fetch(self):
        with self._lock:
            return self._data

    def push(self, key, value):
        if key not in self._data:
            raise RuntimeError("Queue data schema violated")

        with self._lock:
            self._data[key] = value


class QueueThread(threading.Thread):
    """ Collects data from zmq message queue in the background. """

    em_enable_fail_codes = [16, 17]
    em_enable_fail_reasons = ["bpsState false", "low brake pressure", "throttle non-zero",
                              "brake not pressed", "not hv enabled", "motors failed to start"]

    def __init__(self, queue_data, dbc=default_dbc_path(), dtc=default_dtc_path()):
        threading.Thread.__init__(self)
        self.queue_data = queue_data
        self.dashboard_subscriber = DashboardSubscriber()
        self.db = cantools.database.load_file(dbc)

        self.dtc_messages = []
        with open(dtc) as dtc_file:
            csv_reader = csv.reader(dtc_file)
            next(csv_reader)                        # Read header
            for row in csv_reader:
                self.dtc_messages.append(row[6])    # Add each DTC message to list

    # Convert motor RPM to km/h
    def get_speed_kph_from_rpm(self, new_speed_rpm, current_speed_kph):
        radius = 9              # Inches (wheel radius)
        in_to_km = 0.001524     # Inches to km conversion
        sprocket_ratio = 52/15  # Motor sprocket to wheel sprocket ratio
        new_speed_kph = (new_speed_rpm * in_to_km * sprocket_ratio * 2 * math.pi * radius)
        return (0.5 * (current_speed_kph + new_speed_kph))

    def run(self):
        speed = 0
        while True:
            can_packet = self.dashboard_subscriber.recv()

            # BMU_stateBatteryHV
            if can_packet["frame_id"] == self.db.get_message_by_name("BMU_stateBusHV").frame_id:
                voltage = can_packet["signals"]["VoltageCellMin"]
                self.queue_data.push("voltage", round(voltage, 1))

            # BMU_batteryStatusHV
            elif can_packet["frame_id"] == self.db.get_message_by_name("BMU_batteryStatusHV").frame_id:
                battery = can_packet["signals"]["StateBatteryChargeHV"]
                self.queue_data.push("battery", round(battery, 1))
                temp = can_packet["signals"]["TempCellMax"]
                self.queue_data.push("temperature", round(temp, 1))
 
            # SpeedFeedbackRight, SpeedFeedbackLeft
            elif can_packet["frame_id"] in [self.db.get_message_by_name("SpeedFeedbackRight").frame_id,
                                            self.db.get_message_by_name("SpeedFeedbackLeft").frame_id]:
                current_speed = 0
                if can_packet["frame_id"] == self.db.get_message_by_name("SpeedFeedbackRight").frame_id:
                    current_speed = can_packet["signals"]["SpeedMotorRight"]
                else:
                    current_speed = can_packet["signals"]["SpeedMotorLeft"]
                speed = self.get_speed_kph_from_rpm(current_speed, speed)
                self.queue_data.push("speed", round(speed, 1))

            # PDU_DTC, DCU_DTC, VCU_F7_DTC, BMU_DTC
            elif can_packet["frame_id"] in [self.db.get_message_by_name("PDU_DTC").frame_id,
                                            self.db.get_message_by_name("DCU_DTC").frame_id,
                                            self.db.get_message_by_name("VCU_F7_DTC").frame_id,
                                            self.db.get_message_by_name("BMU_DTC").frame_id]:
                code, severity, data = can_packet["signals"]["DTC_CODE"], can_packet["signals"]["DTC_Severity"], can_packet["signals"]["DTC_Data"]
                try:
                    message = self.dtc_messages[int(code)-1]
                except IndexError:
                    message = "Unknown DTC Code: {})".format(code)

                # Substitute #data in message with actual error reason
                if code in QueueThread.em_enable_fail_codes:
                    message = message[:message.find(" (Reasons")]
                    message = message.replace("#data", QueueThread.em_enable_fail_reasons[data])
                elif "#data" in message:
                    message = message.replace("#data", data)

                payload = [{
                    "severity": severity,
                    "message": message
                }]
                self.queue_data.push("dtc_message_payload", payload)

class DashboardSubscriber(QueueDataSubscriber):
    """ Subscribes dashboard to data using zmq """

    def __init__(self):
        super(DashboardSubscriber, self).__init__()
        self.subscribe_to_packet_type("")

def main():

    # Start thread in background to collect data
    data = QueueData()
    queue_thread = QueueThread(data)
    queue_thread.daemon = True
    queue_thread.start()
    dashboard = Tk()
    app = DashboardApp(dashboard, data)
    dashboard.mainloop()


if __name__ == "__main__":
    main()
