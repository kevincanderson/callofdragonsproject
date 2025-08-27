import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess

class EmulatorWorker(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, emulator_queue, ldconsole_path):
        super().__init__()
        self.emulator_queue = emulator_queue
        self.ldconsole_path = ldconsole_path
        self._is_running = True

    def run_ldconsole(self, args):
        cmd = [self.ldconsole_path] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return f"Error: {result.stderr}"
            return result.stdout
        except Exception as e:
            return f"Exception: {str(e)}"

    def run(self):
        import time
        for emulator_name in self.emulator_queue:
            if not self._is_running:
                break
            output = self.run_ldconsole(['launch', '--name', emulator_name])
            self.log_signal.emit(f"{emulator_name}: {output}")
            self.log_signal.emit(f"Waiting 15 seconds for emulator to load...")
            time.sleep(15)
            # Check if emulator is running
            while True:
                status = self.run_ldconsole(['isrunning', '--name', emulator_name])
                self.log_signal.emit(f"Checking if {emulator_name} is running: {status.strip()}")
                if 'running' in status.lower():
                    break
                self.log_signal.emit(f"{emulator_name} not running yet, waiting 15 seconds...")
                time.sleep(15)
            # Step 2: Launch Game
            game_output = self.run_ldconsole(['runapp', '--name', emulator_name, '--packagename', 'com.farlightgames.samo.gp'])
            if "Error:" in game_output or "Exception:" in game_output:
                self.log_signal.emit(f"{emulator_name} (Game Launch Error): {game_output}")
            else:
                self.log_signal.emit(f"{emulator_name} (Game Launch Output): {game_output}")
            # Step 3: Wait 60 seconds before first game running check
            self.log_signal.emit(f"{emulator_name}: Waiting 60 seconds before checking if game is running...")
            time.sleep(60)
            game_loaded = False
            for i in range(6):  # 6 x 5s = 30s
                adb_output = self.run_ldconsole(['adb', '--name', emulator_name, '--command', 'shell ps | grep com.farlightgames.samo.gp'])
                if 'com.farlightgames.samo.gp' in adb_output:
                    self.log_signal.emit(f"{emulator_name}: Game is running!")
                    game_loaded = True
                    break
                else:
                    self.log_signal.emit(f"{emulator_name}: Game not running yet, waiting 5 seconds...")
                    time.sleep(5)
            if not game_loaded:
                self.log_signal.emit(f"{emulator_name}: Game did not start within 90 seconds.")
            # Step 4: Let game run for 30 seconds
            if game_loaded:
                self.log_signal.emit(f"{emulator_name}: Letting game run for 30 seconds...")
                time.sleep(30)
            # Step 5: Close the game
            close_game = self.run_ldconsole(['killapp', '--name', emulator_name, '--packagename', 'com.farlightgames.samo.gp'])
            self.log_signal.emit(f"{emulator_name} (Game Closed): {close_game}")
            # Step 6: Close Emulator
            output = self.run_ldconsole(['quit', '--name', emulator_name])
            self.log_signal.emit(f"{emulator_name} (Emulator Closed): {output}")

class LDPlayerController(QWidget):
    def log(self, message):
        print(message)
    def init_ui(self):
        self.setWindowTitle('CoD BoT')
        self.setMinimumWidth(600)

        from PyQt5.QtWidgets import QVBoxLayout, QLabel, QSizePolicy, QTextEdit
        main_layout = QVBoxLayout()

        # Logo placeholder (square)
        logo_label = QLabel('LOGO')
        logo_label.setStyleSheet("font-size: 32px; font-weight: bold; min-width: 180px; min-height: 180px; max-width: 180px; max-height: 180px; background: #eee; border: 1px solid #ccc; text-align: center;")
        logo_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        main_layout.addWidget(logo_label)

        # Buttons vertical layout
        button_style = "font-size: 24px; min-height: 60px; min-width: 400px;"

        self.start_btn = QPushButton('Start')
        self.start_btn.setStyleSheet(button_style)
        self.start_btn.clicked.connect(self.start_app)
        main_layout.addWidget(self.start_btn)

        self.pause_btn = QPushButton('Pause')
        self.pause_btn.setStyleSheet(button_style)
        self.pause_btn.clicked.connect(self.pause_app)
        self.pause_btn.setEnabled(False)
        main_layout.addWidget(self.pause_btn)

        self.end_btn = QPushButton('End')
        self.end_btn.setStyleSheet(button_style)
        self.end_btn.clicked.connect(self.end_app)
        self.end_btn.setEnabled(False)
        main_layout.addWidget(self.end_btn)

        self.setLayout(main_layout)
    log_signal = pyqtSignal(str)

    def __init__(self, emulator_queue, ldconsole_path):
        super().__init__()
        self.emulator_queue = emulator_queue
        self.ldconsole_path = ldconsole_path
        self._is_running = True

    def run_ldconsole(self, args):
        cmd = [self.ldconsole_path] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return f"Error: {result.stderr}"
            return result.stdout
        except Exception as e:
            return f"Exception: {str(e)}"

    def run(self):
        import time
        for emulator_name in self.emulator_queue:
            if not self._is_running:
                break
            output = self.run_ldconsole(['launch', '--name', emulator_name])
            self.log_signal.emit(f"{emulator_name}: {output}")
            self.log_signal.emit(f"Waiting 15 seconds for emulator to load...")
            time.sleep(15)
            # Check if emulator is running
            while True:
                status = self.run_ldconsole(['isrunning', '--name', emulator_name])
                self.log_signal.emit(f"Checking if {emulator_name} is running: {status.strip()}")
                if 'running' in status.lower():
                    break
                self.log_signal.emit(f"{emulator_name} not running yet, waiting 15 seconds...")
                time.sleep(15)
            # Step 2: Launch Game
            game_output = self.run_ldconsole(['runapp', '--name', emulator_name, '--packagename', 'com.farlightgames.samo.gp'])
            if "Error:" in game_output or "Exception:" in game_output:
                self.log_signal.emit(f"{emulator_name} (Game Launch Error): {game_output}")
            else:
                self.log_signal.emit(f"{emulator_name} (Game Launch Output): {game_output}")
            # Step 3: Wait 60 seconds before first game running check
            self.log_signal.emit(f"{emulator_name}: Waiting 60 seconds before checking if game is running...")
            time.sleep(60)
            game_loaded = False
            for i in range(6):  # 6 x 5s = 30s
                adb_output = self.run_ldconsole(['adb', '--name', emulator_name, '--command', 'shell ps | grep com.farlightgames.samo.gp'])
                if 'com.farlightgames.samo.gp' in adb_output:
                    self.log_signal.emit(f"{emulator_name}: Game is running!")
                    game_loaded = True
                    break
                else:
                    self.log_signal.emit(f"{emulator_name}: Game not running yet, waiting 5 seconds...")
                    time.sleep(5)
            if not game_loaded:
                self.log_signal.emit(f"{emulator_name}: Game did not start within 90 seconds.")
            # Step 4: Let game run for 30 seconds
            if game_loaded:
                self.log_signal.emit(f"{emulator_name}: Letting game run for 30 seconds...")
                time.sleep(30)
            # Step 5: Close the game
            close_game = self.run_ldconsole(['killapp', '--name', emulator_name, '--packagename', 'com.farlightgames.samo.gp'])
            self.log_signal.emit(f"{emulator_name} (Game Closed): {close_game}")
            # Step 6: Close Emulator
            output = self.run_ldconsole(['quit', '--name', emulator_name])
            self.log_signal.emit(f"{emulator_name} (Emulator Closed): {output}")
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.is_paused = False
        self.ldconsole_path = r'C:\LDPlayer\LDPlayer9\ldconsole.exe'  # Update this path if needed
        # List of emulator names to launch (update as needed)
        self.emulator_queue = ['my.cod.farms.01', 'my.cod.farms.02']
        self.init_ui()
    def run_ldconsole(self, args):
        cmd = [self.ldconsole_path] + args
        def start_app(self):
            if not self.is_running:
                self.is_running = True
                self.is_paused = False
                self.start_btn.setEnabled(False)
                self.pause_btn.setEnabled(True)
                self.end_btn.setEnabled(True)
                self.worker = EmulatorWorker(self.emulator_queue, self.ldconsole_path)
                self.worker.log_signal.connect(self.log)
                self.worker.start()

    def start_app(self):
        import time
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.end_btn.setEnabled(True)
            for emulator_name in self.emulator_queue:
                output = self.run_ldconsole(['launch', '--name', emulator_name])
                self.log(f"{emulator_name}: {output}")
                self.log(f"Waiting 20 seconds for emulator to load...")
                time.sleep(20)
                # Check if emulator is running
                while True:
                    status = self.run_ldconsole(['isrunning', '--name', emulator_name])
                    self.log(f"Checking if {emulator_name} is running: {status.strip()}")
                    if 'running' in status.lower():
                        break
                    self.log(f"{emulator_name} not running yet, waiting 15 seconds...")
                    time.sleep(15)
                # Step 2: Launch Game
                game_output = self.run_ldconsole(['runapp', '--name', emulator_name, '--packagename', 'com.farlightgames.samo.gp'])
                if "Error:" in game_output or "Exception:" in game_output:
                    self.log(f"{emulator_name} (Game Launch Error): {game_output}")
                else:
                    self.log(f"{emulator_name} (Game Launch Output): {game_output}")
                # Step 3: Wait 60 seconds before first game running check
                self.log(f"{emulator_name}: Waiting 60 seconds before checking if game is running...")
                time.sleep(60)
                game_loaded = False
                for i in range(6):  # 6 x 5s = 30s
                    adb_output = self.run_ldconsole(['adb', '--name', emulator_name, '--command', 'shell ps | grep com.farlightgames.samo.gp'])
                    if 'com.farlightgames.samo.gp' in adb_output:
                        self.log(f"{emulator_name}: Game is running!")
                        game_loaded = True
                        break
                    else:
                        self.log(f"{emulator_name}: Game not running yet, waiting 5 seconds...")
                        time.sleep(5)
                if not game_loaded:
                    self.log(f"{emulator_name}: Game did not start within 90 seconds.")
                # Step 4: Take 10 screen captures, 10 seconds apart
                if game_loaded:
                    for capture_num in range(1, 11):
                        screenshot_path = f"screenshot_{emulator_name}_{capture_num}.png"
                        adb_screencap_cmd = f"shell screencap -p /sdcard/{screenshot_path}"
                        pull_cmd = f"pull /sdcard/{screenshot_path} ./"
                        # Take screenshot
                        screencap_output = self.run_ldconsole(['adb', '--name', emulator_name, '--command', adb_screencap_cmd])
                        self.log(f"{emulator_name}: Screenshot {capture_num} taken: {screencap_output}")
                        # Pull screenshot to local
                        pull_output = self.run_ldconsole(['adb', '--name', emulator_name, '--command', pull_cmd])
                        self.log(f"{emulator_name}: Screenshot {capture_num} pulled: {pull_output}")
                        time.sleep(10)
                # Step 5: Close the game
                close_game = self.run_ldconsole(['killapp', '--name', emulator_name, '--packagename', 'com.farlightgames.samo.gp'])
                self.log(f"{emulator_name} (Game Closed): {close_game}")
                # Step 6: Close Emulator
                output = self.run_ldconsole(['quit', '--name', emulator_name])
                self.log(f"{emulator_name} (Emulator Closed): {output}")

    def pause_app(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.pause_btn.setText('Resume')
            self.log('App Paused!')
        elif self.is_running and self.is_paused:
            self.is_paused = False
            self.pause_btn.setText('Pause')
            self.log('App Resumed!')

    def end_app(self):
        if self.is_running:
            self.is_running = False
            self.is_paused = False
            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.pause_btn.setText('Pause')
            self.end_btn.setEnabled(False)
            for emulator_name in self.emulator_queue:
                # Step 4: Close Game (force stop, replace with actual package name if needed)
                close_game = self.run_ldconsole(['killapp', '--name', emulator_name, '--packagename', 'com.farlightgames.samo.gp'])
                self.log(f"{emulator_name} (Game Closed): {close_game}")
                # Step 5: Close Emulator
                output = self.run_ldconsole(['quit', '--name', emulator_name])
                self.log(f"{emulator_name} (Emulator Closed): {output}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LDPlayerController()
    window.show()
    sys.exit(app.exec_())
