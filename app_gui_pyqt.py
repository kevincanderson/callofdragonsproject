import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox
import subprocess

class LDPlayerController(QWidget):
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.is_paused = False
        self.ldconsole_path = r'C:\LDPlayer\LDPlayer9\ldconsole.exe'  # Update this path if needed
        # List of emulator names to launch (update as needed)
        self.emulator_queue = ['LDPlayer1', 'LDPlayer2']
        self.init_ui()
    def run_ldconsole(self, args):
        cmd = [self.ldconsole_path] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return f"Error: {result.stderr}"
            return result.stdout
        except Exception as e:
            return f"Exception: {str(e)}"

    def init_ui(self):
        self.setWindowTitle('CoD BoT')
        self.setMinimumWidth(600)

        from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy
        main_layout = QHBoxLayout()

        # Logo placeholder (square)
        logo_label = QLabel('LOGO')
        logo_label.setStyleSheet("font-size: 32px; font-weight: bold; min-width: 180px; min-height: 180px; max-width: 180px; max-height: 180px; background: #eee; border: 1px solid #ccc; text-align: center;")
        logo_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        main_layout.addWidget(logo_label)

        # Buttons vertical layout
        button_layout = QVBoxLayout()
        button_style = "font-size: 24px; min-height: 60px; min-width: 400px;"

        self.start_btn = QPushButton('Start')
        self.start_btn.setStyleSheet(button_style)
        self.start_btn.clicked.connect(self.start_app)
        button_layout.addWidget(self.start_btn)

        self.pause_btn = QPushButton('Pause')
        self.pause_btn.setStyleSheet(button_style)
        self.pause_btn.clicked.connect(self.pause_app)
        self.pause_btn.setEnabled(False)
        button_layout.addWidget(self.pause_btn)

        self.end_btn = QPushButton('End')
        self.end_btn.setStyleSheet(button_style)
        self.end_btn.clicked.connect(self.end_app)
        self.end_btn.setEnabled(False)
        button_layout.addWidget(self.end_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def start_app(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.end_btn.setEnabled(True)
            # Launch all emulators in the queue
            launch_results = []
            for emulator_name in self.emulator_queue:
                output = self.run_ldconsole(['launch', '--name', emulator_name])
                launch_results.append(f"{emulator_name}: {output}")
            QMessageBox.information(self, 'Info', 'Emulators launched:\n' + '\n'.join(launch_results))

    def pause_app(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.pause_btn.setText('Resume')
            QMessageBox.information(self, 'Info', 'App Paused!')
        elif self.is_running and self.is_paused:
            self.is_paused = False
            self.pause_btn.setText('Pause')
            QMessageBox.information(self, 'Info', 'App Resumed!')

    def end_app(self):
        if self.is_running:
            self.is_running = False
            self.is_paused = False
            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.pause_btn.setText('Pause')
            self.end_btn.setEnabled(False)
            # Stop LDPlayer emulator
            output = self.run_ldconsole(['quit', '--name', self.emulator_name])
            QMessageBox.information(self, 'Info', f'App Ended!\n{output}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LDPlayerController()
    window.show()
    sys.exit(app.exec_())
