from emulator.controller import EmulatorController
from tasks.task_manager import TaskManager

class CallOfDragonsBot:
    def __init__(self):
        self.emulator_controller = EmulatorController()
        self.task_manager = TaskManager()

    def start(self):
        self.emulator_controller.start_emulator()
        print("Emulator started.")
        self.run_tasks()

    def run_tasks(self):
        self.task_manager.execute_tasks()

    def stop(self):
        self.task_manager.clear_tasks()
        self.emulator_controller.stop_emulator()
        print("Emulator stopped.")

if __name__ == "__main__":
    bot = CallOfDragonsBot()
    try:
        bot.start()
    except KeyboardInterrupt:
        bot.stop()