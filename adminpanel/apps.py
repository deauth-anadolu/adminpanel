from django.apps import AppConfig
import subprocess
import threading
import os
import signal
from django.core.signals import request_finished
from django.db.backends.signals import connection_created
from django.db import connections

class MyAppConfig(AppConfig):
    name = 'adminpanel'

    def ready(self):
        def run_IDS():
            script_path = '/home/hsrv/Desktop/proje/IDS/main.py'
            # result = subprocess.run(['python3', script_path], capture_output=True, text=True, shell=True)
            # Command to open XTerm and run the script
            command = ['xterm', '-hold', '-e', f'python3 {script_path}']
            self.process = subprocess.Popen(command)
            
            if self.process.returncode != 0:
                # Handle the error appropriately
                print(f"Error running IDS: {self.process.stderr}")
            else:
                print(f"IDS Output: {self.process.stdout}")
        
            # Register signal handlers
            request_finished.connect(self.stop_subprocess)

        # Run IDS in a separate thread
        thread = threading.Thread(target=run_IDS)
        thread.start()


    def stop_subprocess(self, **kwargs):
        if self.process:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process = None
    