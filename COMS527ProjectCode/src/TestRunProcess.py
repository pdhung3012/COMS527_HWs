import subprocess, threading
import os,signal
import datetime
class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.timeExecution=0.0
        self.isTimeOut=False

    def run(self, timeout):
        def target():
            # print('Thread started')
            self.timeExecution =0.0
            self.isTimeOut = False
            start_time = datetime.datetime.now()
            self.process = subprocess.Popen(self.cmd, shell=True, preexec_fn=os.setsid)
            self.process.communicate()
            # print('Thread finished')

            end_time = datetime.datetime.now()
            time_diff = (end_time - start_time)
            execution_time = time_diff.total_seconds() * 1000
            self.timeExecution=execution_time

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            # print('Terminating process')
            os.killpg(self.process.pid, signal.SIGTERM)
            self.isTimeOut = True
            thread.join()
        print(self.process.returncode)

command = Command("echo 'Process started'; sleep 2; echo 'Process finished'")
command.run(timeout=3)
print('Time for run {} {}'.format(command.isTimeOut,command.timeExecution))
command.run(timeout=1)
print('Time for run {} {}'.format(command.isTimeOut,command.timeExecution))
