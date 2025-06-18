import schedule
import time
from netmiko import ConnectHandler
import getpass
import sys

VLAN_LIST = [
    '811', '813', '814', '815', '816', '817', '820', '821', '822', '823', 
    '824', '825', '826', '827', '828', '829', '830', '831', '832', '833', 
    '834', '835'
    ]
#INT_LIST = ['1/0/10']

def issue_command_to_switch(switch_ip, username, password, enable_password):

    device = {
        "device_type": "cisco_ios",
        "ip": switch_ip,
        "username": username,
        "password": password,
        "secret": enable_password,
    }

    """
    # Enter privileged EXEC mode
    enable
    # Enter global configuration mode
    configure terminal
    # Enter interface configuration mode for the interface you want to change
    int gi1/25
    # Change the VLAN for this interface
    switchport access vlan 192
    # Exit interface configuration mode
    exit
    # Exit global configuration mode
    exit
    """
    # Function to issue a command to the Cisco switch
    print("Going to execute command 1")
    cmd_to_exec = "switchport access vlan" + " " + VLAN_LIST[0]

    #interface_cmd = "interface GigabitEthernet" + " " + INT_LIST[0]
    interface_cmd = "interface GigabitEthernet" + " " + "1/0/10"
    #print("Interface command: " + interface_cmd)
    new_vlan = VLAN_LIST.pop(0)
    #new_int = INT_LIST.pop(0)

    ######################
    # To make sure it runs again on the same list
    ######################
    VLAN_LIST.append(new_vlan)
    #INT_LIST.append(new_int)
    print("VLAN list now: ")
    print(VLAN_LIST)
    #print("Int LIST now: ")
    #print(INT_LIST)

    # int gi0/3
    connection = None  # initialize connection variable

    # get commands to write
    commands = []
    commands.append(interface_cmd)
    commands.append(cmd_to_exec)
    print("****Command List****\n")
    print(commands)

    # now execute it
    try:
        print("****Initiating connection to the switch.****")
        connection = ConnectHandler(**device)
        connection.enable()
    except Exception as e:
        print(
            f"Caught an exception while trying to connect to the switch: {e}")
        return

    try:
        print("****Executing commands.****")
        output = connection.send_config_set(commands)
        print(output)
        print("****Done executing.****")
    except Exception as e:
        print(f"Caught an exception while trying to execute commands on the switch: {e}")

    try:
        print("****Disconnecting from the switch.****")
        connection.disconnect()
    except Exception as e:
        print(f"Caught an exception while trying to disconnect from the switch: {e}")
    
    ##########
        # Does this need to terminate?
    ##########
    """    
    if len(VLAN_LIST) == 0:
        print("VLAN list is empty! Terminating script")
        sys.exit(0)
    """
def main():
    
    switch_ip = input("Enter switch IP: ")
    username = getpass.getpass("Enter the username: ")
    password = getpass.getpass("Enter the password: ")
    enable_password = getpass.getpass("Enter the enable password: ")

    # get the VLAN list and its corresponding interface list
    """
    try:
        num_of_vlans = input("Enter the number of VLANS you wish to go through.\n")
        num_of_vlans = int(num_of_vlans)

    except Exception as e:
        print("Please enter a valid number.")

    for i in range(int(num_of_vlans)):
        vlan_num = input("Enter VLAN number: \n")
        VLAN_LIST.append(vlan_num)
        int_num = input("Enter corresponding interface: \n")
        INT_LIST.append(int_num)
    """
    print("Your current VLAN and interface list is: ")
    for i in range(len(VLAN_LIST)):
        #print("VLAN: " + VLAN_LIST[i] + " ----- Interface: " + INT_LIST[i])
        print("VLAN: " + VLAN_LIST[i] + " ----- Interface: " + "1/0/10")


    # Schedule the function to run every hour
    #schedule.every(6).hours.do(issue_command_to_switch, switch_ip=switch_ip, username=username, password=password, enable_password=enable_password)
    schedule.every(1).minutes.do(issue_command_to_switch, switch_ip=switch_ip, username=username, password=password, enable_password=enable_password)
    while True:
    # Run pending tasks
        schedule.run_pending()
        # Sleep for a while
        time.sleep(1)

if __name__ == "__main__":
    main()
    main()
