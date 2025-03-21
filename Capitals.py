import subprocess
import platform

# Global Variables: Get OS and  parameter up front.
DETECTED_OS = platform.system().lower() # e.g., 'windows', 'linux', etc
PING_PARAM = "-n" if DETECTED_OS == "windows" else "-c"

if DETECTED_OS == "windows":
    TIMEOUT = "100" # Milliseconds
else:
    TIMEOUT = "0.5"

#               print(f"\n[Global Setup] Detected OS: {DETECTED_OS}, using ping parameter: {PING_PARAM}\n")

def build_ping_command(host):
    if DETECTED_OS == "windows":
        command = ["ping", PING_PARAM, "1", "-w", TIMEOUT, host]
    else:
        command = ["ping", PING_PARAM, "1", "-W", TIMEOUT, host]

    return " ".join(command)

def ping_host(host):
    """
    Ping a given host and return True if the host is up, otherwise return False.
    Debug prints show each step in the process. 
    """
    # print(f"\n--- Pinging {host} ---")    

    # (Global OS and parameter already set, See global variablesDETECTED_OS and PING_PARAM)
    # print(f"Using global parameter: {PING_PARAM}\n")
    
    # Build the ping command as a list.
    # For example, on linux: ["ping", "-c", "1", "8.8.8.8"]
     # print("Building the ping command...")
    # command = ["ping", param, "1", host]

    # command = ["ping", PING_PARAM, "1", host]
    ## print(f"Ping command: {command}")
    #command_str = " ".join(command)
    #print(f"Command string {command_str}\n")    

    try: 
        # Execute the ping command without raising an exception on nonzero exit code.
        # print(f"Pinging {host} ...")
        # print("Executing the ping command...")
        
        # result = subprocess.run(command, capture_output=True, text=True, check=False)
        #print("Return code:", result.returncode)
        command_str = build_ping_command(host)
        # Use .split() to convert the command string back into a list
        result = subprocess.run(command_str.split(), capture_output=True, text=True, check=False)
        # print("Return code:", result.returncode)


        # print("Ping command executed, Return code:", result.returncode)

        # Capture and process the output. 
        # print("Capturing and processing the output...")
        output = result.stdout.lower()
        #               print("Ping result output:")
        #               print(result.stdout)

        # Decide what we are looking for based on OS. 
        if DETECTED_OS == "windows":
            success_indicator = "reply from"
        else:
            success_indicator = "bytes from"
        
        # Double check to verify the success indicator is present and the commom error phrases are not.
        if (success_indicator in output and
            "destination host unreachable" not in output and
            "request timed out" not in output):
            # print(f"Success indicator('{success_indicator}') found in output for {host} without error messages.")
            #               print(f"--- Result for {host} (SUCCESS) ---")
            return True
        else:
            # print(f"Either missing success indicator ('{success_indicator}') or found error message in output for {host}.") 
            #               print(f"--- Result for {host} (FAILURE) ---")
            return False
            
    except Exception as e:
        print(f"An exception occurred while pinging {host}:  {e}")
        print((e).stdout)
        print(f"--- Result for {host} with failure ---\n")
        return False

def ping_sweep(base_ip, start, end):

    """
    Sweep the IP range from the base_ip.start to base_ip.end.
    For Example if base_ip = "192.168.1", start=1, end = 254, 
    it will ping 192.168.1.1 through 192.168.254.

    Returns a list of IPs that are up.
    Includes debug prints to show each step.
    """
    #               print(f"\n=== ping_sweep: Starting sweep for {base_ip}.{start} to {base_ip}.{end} ===")
    up_hosts = []
    for i in range(start, end +1):
        # Construct the IP address. 
        ip = f"{base_ip}.{i}"
        command_str = build_ping_command(ip)
        # print(f"\n--- Processing IP {ip} --- :")

        # Ping the IP address. 
        # print(f"Pinging {ip}...")
        #               print(f"Pinging {ip}: \nCommand string {command_str} ")
        # print(f"ping_sweep: Pinging {ip}...")
        if ping_host(ip):
            print(f"\033[1;32m{ip} is up!\033[0m")
            # print(f"{ip} is up!") # ping_sweep: -->
            up_hosts.append(ip)
        else:
            print(f"\033[1;31m{ip} is down!\033[0m")
            # print(f"{ip} is down!") # ping_sweep: -->

    print(f"\n=== Sweep complete. Found {len(up_hosts)} hosts up. ===")
    return up_hosts    # Changed: Returns list of hosts that are up.

if __name__ == "__main__":
    # Main Block: Setup and call ping sweep.
    print("=== Starting Ping Sweep Utility ===")

    # Example usage: Sweep from 192.168.1.1 to 192.168.1.254
    base = "192.168.1"
    start_range = 1
    end_range = 255 #255

    print(f"Sweeping Ip range {base}.{start_range} through {base}.{end_range}... ")
    up_list = ping_sweep(base, start_range, end_range)

    print("\n=== Ping sweep Complete ===")
    if up_list:
        print("The Following hosts are up:")
        for ip in up_list:
            print(f"  {ip}")
    else: 
        print("No hosts were found up in the specified range.")
        
