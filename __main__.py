import os
import threading

def run_command(command):
    os.system(command)

if __name__ == '__main__':
    # Get the absolute path of the current script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the filenames of the Python scripts
    script1 = "main.py"
    script2 = "make_array/_serial_v2.py"

    # Create a thread for each script and start them
    threads = []
    for script in [script1, script2]:
        # Construct the full path to the script file
        script_path = os.path.join(script_dir, script)

        # Create the command to run the script
        command = f"python {script_path}"

        # Start the thread for the command
        thread = threading.Thread(target=run_command, args=(command,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
