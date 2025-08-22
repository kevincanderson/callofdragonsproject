from ppadb.client import Client as AdbClient
from datetime import datetime
import time

class EmulatorController:
    def __init__(self, host="127.0.0.1", port=5037, serial=None):
        self.client = AdbClient(host=host, port=port)
        self.device = None
        self.emulator_running = False
        self.serial = serial  # Add serial as an optional parameter

    def start_emulator(self):
        # Connect to LDPlayer via ADB (assumes LDPlayer is already running)
        devices = self.client.devices()
        if not devices:
            print("No LDPlayer instance found. Make sure LDPlayer is running and ADB is enabled.")
            self.emulator_running = False
            return
        if self.serial:
            # Try to find the device with the specified serial
            for dev in devices:
                if dev.serial == self.serial:
                    self.device = dev
                    break
            if not self.device:
                print(f"No emulator with serial {self.serial} found.")
                self.emulator_running = False
                return
        else:
            # Default: use the first device
            self.device = devices[0]
        self.emulator_running = True
        print(f"Connected to {self.device.serial}")

    def stop_emulator(self):
        # Optionally implement stopping LDPlayer via command line if needed
        self.device = None
        self.emulator_running = False
        print("Emulator stopped (disconnect only).")

    def send_command(self, command):
        if self.emulator_running and self.device:
            output = self.device.shell(command)
            print(f"Command sent to emulator: {command}\nOutput: {output}")
        else:
            print("Emulator is not running. Please start it first.")

    def tap(self, x, y):
        if self.emulator_running and self.device:
            self.device.shell(f"input tap {x} {y}")
            print(f"Tapped at ({x}, {y})")
        else:
            print("Emulator is not running. Please start it first.")

    def screenshot(self, path="screen.png"):
        if self.emulator_running and self.device:
            image = self.device.screencap()
            with open(path, "wb") as f:
                f.write(image)
            print(f"Screenshot saved to {path}")
        else:
            print("Emulator is not running. Please start it first.")

    def launch_app(self, package_name):
        if self.emulator_running and self.device:
            self.device.shell(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
            print(f"Launched app: {package_name}")
        else:
            print("Emulator is not running. Please start it first.")

def log(msg): 
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# List of emulators and their tap coordinate sets
emulators = [
    {
        "serial": "emulator-5560",  # LDPlayer example serial ORE
        "taps": {
            "world": (30, 451),
            "search1": (26, 405),
            "resource": (423, 448),
            "reduce-level": (358, 346),
            "increase-level": (493, 346),
            "search2": (423, 383),
            "node": (319, 236),
            "gather": (478, 322),
            "legion": (504, 137),
            "send": (532, 438),
        }
    },
    # {
    #     "serial": "emulator-5562",  # LDPlayer example serial GOLD
    #     "taps": {
    #         "world": (60, 672),
    #         "search1": (56, 570),
    #         "resource": (430, 650),
    #         "reduce-level": (294, 454),
    #         "increase-level": (567, 455),
    #         "search2": (427, 528),
    #         "node": (636, 353),
    #         "gather": (924, 525),
    #         "legion": (1016, 153),
    #         "send": (1064, 633),
    #     }
    # },
    # {
    #     "serial": "emulator-5554",  # Another LDPlayer instance WOOD
    #     "taps": {
    #         "world": (30, 458),
    #         "search1": (28, 406),
    #         "resource": (428, 446),
    #         "reduce-level": (360, 346),
    #         "increase-level": (491, 347),
    #         "search2": (419, 381),
    #         "node": (319, 236),
    #         "gather": (476, 322),
    #         "legion": (504, 153),
    #         "send": (532, 438),
    #     }
    # },
    #     {
    #     "serial": "emulator-5558",  # Another LDPlayer instance WOOD
    #     "taps": {
    #         "world": (30, 458),
    #         "search1": (28, 406),
    #         "resource": (428, 446),
    #         "reduce-level": (360, 346),
    #         "increase-level": (491, 347),
    #         "search2": (419, 381),
    #         "node": (319, 236),
    #         "gather": (476, 322),
    #         "legion": (504, 153),
    #         "send": (532, 438),
    #     }
    # },
    # Add more LDPlayer instances as needed
]

first_run = True

while True:
    if first_run:
        log("Sleeping 4 hours before first run...")
        time.sleep(4)
        first_run = False

    for emu in emulators:
        log(f"Processing {emu['serial']}")
        controller = EmulatorController(serial=emu["serial"])
        controller.start_emulator()
        if controller.emulator_running:
            log("Launching Call of Dragons...")
            controller.launch_app("com.farlightgames.samo.gp")
            time.sleep(90)
            # log(f"Tapping main {emu['taps']['world']}")
            # controller.tap(*emu['taps']['world'])
            # time.sleep(2)
            # for repeat in range(5):
            #     log(f"Tapping search {emu['taps']['search1']}")
            #     controller.tap(*emu['taps']['search1'])
            #     time.sleep(2)
            #     log(f"Sequence repeat {repeat+1}")
            #     controller.tap(*emu['taps']['resource'])
            #     time.sleep(2)
            #     for i in range(7):
            #         log(f"Tapping reduce-level {emu['taps']['reduce-level']} [{i+1}/7]")
            #         controller.tap(*emu['taps']['reduce-level'])
            #         time.sleep(0.5)
            #     time.sleep(2)
            #     for i in range(4):
            #         log(f"Tapping increase-level {emu['taps']['increase-level']} [{i+1}/5]")
            #         controller.tap(*emu['taps']['increase-level'])
            #         time.sleep(0.5)
            #     time.sleep(2)
            #     log(f"Tapping search {emu['taps']['search2']}")
            #     controller.tap(*emu['taps']['search2'])
            #     time.sleep(2)
            #     log(f"Tapping node {emu['taps']['node']}")
            #     controller.tap(*emu['taps']['node'])
            #     time.sleep(2)
            #     log(f"Tapping gather {emu['taps']['gather']}")
            #     controller.tap(*emu['taps']['gather'])
            #     time.sleep(2)
            #     log(f"Tapping legion {emu['taps']['legion']}")
            #     controller.tap(*emu['taps']['legion'])
            #     time.sleep(2)
            #     log(f"Tapping send {emu['taps']['send']}")
            #     controller.tap(*emu['taps']['send'])
            #     time.sleep(60)


            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("01.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("02.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("03.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("04.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("05.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("06.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("07.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("08.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("09.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("10.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("11.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("12.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("13.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("14.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("15.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("16.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("17.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("18.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("19.png")
            time.sleep(5)
            log("Taking screenshots...")
            controller.screenshot("20.png")
            

            # world 60,664
            # search 60,570
            #march 1 927,120 
            #march 2 985, 120 
            #march 3 1040,120 
            #march 4 1100,120 
            #march 5 1160,120 


            time.sleep(10)
            log("Closing Call of Dragons.")
            controller.send_command("am force-stop com.farlightgames.samo.gp")
        controller.stop_emulator()

    log("Waiting 4 hours before restarting all emulators...")
    time.sleep(4 * 60 * 60)