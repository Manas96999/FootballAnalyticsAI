import subprocess
import time
import sys
import os

def print_banner():
    """Prints a stylish banner to the terminal."""
    banner = r"""
    \033[1;32m
    ██████╗ ██████╗  ██████╗ ████████╗██████╗  ██████╗ ██╗      █████╗ ██╗     ██╗██╗   ██╗
    ██╔══██╗██╔══██╗██╔════╝ ╚══██╔══╝██╔══██╗██╔═══██╗██║     ██╔══██╗██║     ██║╚██╗ ██╔╝
    ██████╔╝██████╔╝██║         ██║   ██████╔╝██║   ██║██║     ███████║██║     ██║ ╚████╔╝ 
    ██╔═══╝ ██╔══██╗██║         ██║   ██╔══██╗██║   ██║██║     ██╔══██║██║     ██║  ╚██╔╝  
    ██║     ██║  ██║╚██████╗    ██║   ██║  ██║╚██████╔╝███████╗██║  ██║███████╗██║   ██║   
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝   
    \033[0m
    \033[1;34m=================================================================================\033[0m
    \033[1;32m      Football Analytics AI: Live Demo Mode Initiated\033[0m
    \033[1;34m=================================================================================\033[0m
    """
    print(banner)

def run_in_background(command):
    """Runs a command in a new background process."""
    if sys.platform == "win32":
        return subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        return subprocess.Popen(command, preexec_fn=os.setsid)

def main():
    """Main function to start the demo."""
    print_banner()

    # --- Commands to run ---
    flask_app_cmd = [sys.executable, "main.py"]
    simulator_cmd = [sys.executable, "FootballAnalyticsAI/core/simulate_match.py"]

    server_process = None
    simulator_process = None

    try:
        # 1. Start the Flask Web Server
        print("\n\033[1;36m[STEP 1/3] Starting the Flask web server...\033[0m")
        server_process = run_in_background(flask_app_cmd)
        print(f"  -> \033[0;32mSuccess! Flask server running in background (PID: {server_process.pid})\033[0m")

        # 2. Provide Link and Countdown
        print("\n\033[1;36m[STEP 2/3] Starting the match simulator in...\033[0m")
        print(f"  -> Please open your browser to: \033[4;32mhttp://127.0.0.1:5000\033[0m")
        for i in range(3, 0, -1):
            print(f"\r     {i}...", end="", flush=True)
            time.sleep(1)
        print("\r     \033[0;32mGo!\033[0m")

        # 3. Start the Match Simulator
        print("\n\033[1;36m[STEP 3/3] Running the data simulation engine...\033[0m")
        simulator_process = run_in_background(simulator_cmd)
        print(f"  -> \033[0;32mSuccess! Simulator running in background (PID: {simulator_process.pid})\033[0m")

        print("\n\033[1;33mDemo is now running. Press CTRL+C to stop both processes and exit.\033[0m")
        
        # Keep the main script alive to listen for KeyboardInterrupt
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n\033[1;31mInterruption detected! Shutting down processes gracefully...\033[0m")

    finally:
        # --- Cleanup: Terminate background processes ---
        if server_process:
            print(f"  -> Terminating Flask server (PID: {server_process.pid})...")
            if sys.platform == "win32":
                server_process.send_signal(subprocess.signal.CTRL_BREAK_EVENT)
            else:
                 os.killpg(os.getpgid(server_process.pid), subprocess.signal.SIGTERM)
            server_process.wait()
            print("     \033[0;32mServer stopped.\033[0m")

        if simulator_process:
            print(f"  -> Terminating Simulator (PID: {simulator_process.pid})...")
            if sys.platform == "win32":
                simulator_process.send_signal(subprocess.signal.CTRL_BREAK_EVENT)
            else:
                os.killpg(os.getpgid(simulator_process.pid), subprocess.signal.SIGTERM)
            simulator_process.wait()
            print("     \033[0;32mSimulator stopped.\033[0m")
            
        print("\n\033[1;32mAll processes terminated. Demo finished.\033[0m\n")


if __name__ == "__main__":
    main()

