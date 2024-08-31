import paramiko
import getpass

def connect_to_cisco_router(hostname, username, port=22):
    """
    Connects to a Cisco router using SSH.
    
    Args:
    hostname (str): The IP address or hostname of the router.
    username (str): The username for authentication.
    port (int): The SSH port number (default is 22).
    
    Returns:
    paramiko.SSHClient: An SSH client connected to the router.
    """
    try:
        # Prompt for password securely
        password = getpass.getpass(f"Enter password for {username}@{hostname}: ")
        
        # Initialize the SSH client
        ssh_client = paramiko.SSHClient()
        
        # Automatically add the server's host key
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the router
        ssh_client.connect(hostname=hostname, username=username, password=password, port=port)
        
        print(f"Successfully connected to {hostname}")
        return ssh_client
    
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as ssh_exception:
        print(f"Unable to establish SSH connection: {ssh_exception}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

# Example usage:
# ssh_client = connect_to_cisco_router('192.168.1.1', 'admin')
# if ssh_client:
#     # Perform operations with the connected client
#     ssh_client.close()  # Close the connection when done

def get_bgp_table(ssh_client):
    """
    Retrieves the BGP table from a Cisco router using the 'show ip bgp' command
    and formats the output into a list of dictionaries.

    Args:
    ssh_client (paramiko.SSHClient): An established SSH connection to the router.

    Returns:
    list: A list of dictionaries, each representing a BGP route entry.
    """
    try:
        # Execute the 'show ip bgp' command
        stdin, stdout, stderr = ssh_client.exec_command('show ip bgp')
        output = stdout.read().decode('utf-8')

        # Process the output
        lines = output.split('\n')
        bgp_table = []
        
        # Skip header lines
        for line in lines[1:]:
            if line.strip() and not line.startswith('*>'):
                continue
            
            parts = line.split()
            if len(parts) >= 5:
                entry = {
                    'status': parts[0],
                    'network': parts[1],
                    'next_hop': parts[2],
                    'metric': parts[3],
                    'local_pref': parts[4],
                    'path': ' '.join(parts[5:])
                }
                bgp_table.append(entry)

        return bgp_table

    except Exception as e:
        print(f"An error occurred while retrieving BGP table: {e}")
        return None

# Example usage:
# ssh_client = connect_to_cisco_router('192.168.1.1', 'admin')
# if ssh_client:
#     bgp_table = get_bgp_table(ssh_client)
#     if bgp_table:
#         for entry in bgp_table:
#             print(entry)
#     ssh_client.close()  # Close the connection when done

