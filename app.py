# ...existing code...
import subprocess
import time

LDPLAYER_PATH = r'C:\LDPlayer\LDPlayer9\ldconsole.exe'
EMULATOR_NAME = 'my.cod.farms.01'
GAME_PACKAGE = 'com.farlightgames.samo.gp'

class EmulatorController:
    def __init__(self, emulator_name, adb_path='adb'):
        self.emulator_name = emulator_name
        self.adb_path = adb_path
        self.screenshot_count = 0

    def tap(self, x, y):
        cmd = [self.adb_path, 'shell', 'input', 'tap', str(x), str(y)]
        subprocess.run(cmd)
        time.sleep(2)
        screenshot_name = f'screenshot_{self.screenshot_count}.png'
        self.screenshot(screenshot_name)

    def screenshot(self, save_path=None):
        if save_path is None:
            save_path = f'screenshot_{self.screenshot_count}.png'
        screencap_cmd = [self.adb_path, 'shell', 'screencap', '-p', '/sdcard/screen.png']
        pull_cmd = [self.adb_path, 'pull', '/sdcard/screen.png', save_path]
        subprocess.run(screencap_cmd)
        subprocess.run(pull_cmd)
        self.screenshot_count += 1

def run_ldconsole(args):
    cmd = [LDPLAYER_PATH] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result

if __name__ == '__main__':
    print(f"Launching emulator: {EMULATOR_NAME}")
    run_ldconsole(['launch', '--name', EMULATOR_NAME])
    print("Waiting 30 seconds for emulator to load...")
    time.sleep(30)
    print(f"Launching game: {GAME_PACKAGE}")
    run_ldconsole(['runapp', '--name', EMULATOR_NAME, '--packagename', GAME_PACKAGE])
    
    # EmulatorController class for tap and screenshot automation
    import time
    import subprocess

    class EmulatorController:
        def __init__(self, emulator_name, adb_path='adb'):
            self.emulator_name = emulator_name
            self.adb_path = adb_path
            self.screenshot_count = 0

        def tap(self, x, y):
            cmd = [self.adb_path, 'shell', 'input', 'tap', str(x), str(y)]
            subprocess.run(cmd)
            time.sleep(2)
            screenshot_name = f'screenshot_{self.screenshot_count}.png'
            self.screenshot(screenshot_name)

        def screenshot(self, save_path=None):
            if save_path is None:
                save_path = f'screenshot_{self.screenshot_count}.png'
            screencap_cmd = [self.adb_path, 'shell', 'screencap', '-p', '/sdcard/screen.png']
            pull_cmd = [self.adb_path, 'pull', '/sdcard/screen.png', save_path]
            subprocess.run(screencap_cmd)
            subprocess.run(pull_cmd)
            self.screenshot_count += 1

        controller = EmulatorController(EMULATOR_NAME)
        print("Enter tap coordinates as 'x y' (or type 'quit' to exit):")
        while True:
            user_input = input('Tap coordinates: ')
            if user_input.strip().lower() == 'quit':
                print('Exiting automation loop.')
                break
            try:
                x_str, y_str = user_input.strip().split()
                x, y = int(x_str), int(y_str)
                controller.tap(x, y)
            except ValueError:
                print("Invalid input. Please enter coordinates as two integers, e.g. '100 200', or type 'quit' to exit.")
