#!/usr/bin/python

"""
Implement the `extract_ip` function to extract the IP JSON entries from the Docker
output file provided.  Docker knowledge is not a requirement to write this function,
treat it as a simple text file of output


Expected output is a list of 2 dictionaries:
1. A dictionary of unique public IPs
2. A dictionary of unique private IPs

To simplify, assume that private IPs start with: "10.", "192.", "172.". The rest
of the IPs are public.

e.g.
[
    {'CONTAINER_ROUTER_LOCAL_IP':'192.168.0.32', 'CONTAINER_ROUTER_PEER_IP':'192.168.0.1'},
    {'CONTAINER_ROUTER_HOST_ROUTE':'3.232.22.11'}
]
"""

import re

## Creating a regex for IP detection
ip_regex = '''^.+?(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?).+$'''

def extract_ip(file_name):
    ## Reading the file
    with open(file_name, 'r') as file_reader:
        contents = file_reader.readlines()
    
    ## Initializing an list for IPs
    list_of_ips = []
    
    ## Going over each line in the file
    for line in contents:
        try:
            lookup_ip_in_line = re.findall(ip_regex, line)                          ## Try to find IP in line
            if(lookup_ip_in_line != []):
                if(len(lookup_ip_in_line) == 1):                                    ## If only 1 IP in the line is found
                    ip = ''
                    for ip_octet in lookup_ip_in_line[0]:
                        ip = ip +"."+ ip_octet
                    list_of_ips.append(ip[1:])
                else:                                                               ## If more than 1 IP in the line is found
                    for ip in lookup_ip_in_line:
                        ip = ''
                        for ip_octet in ip:
                            ip = ip + "." + ip_octet
                        list_of_ips.append(ip[1:])
        except:
            print("Something went wrong with the regex search.")        
    
    ## Initializing 2 lists
    private_ip_list = []
    public_ip_list = []
    for ip in list_of_ips:
        try:
            first_octet = ip.split(".")[0]
            ## Check if it's a private IP
            if(first_octet == '10' or first_octet == '172' or first_octet == '192'):
                private_ip_list.append(ip)
            else:
                public_ip_list.append(ip)
        except:
            print("Sorry the IPs are in incorrect format.")

    del list_of_ips
    return private_ip_list, public_ip_list


if __name__ == "__main__":
    ## Extract private and public IP lists
    private_ip_list, public_ip_list = extract_ip('docker_inspect.json')

    count = 0
    ## Print the lists in suitable format.
    print("Private IPs found ---------------------------")
    for ip in private_ip_list:
        count += 1
        print(ip)
    print("\nPublic IPs found ---------------------------")
    for ip in public_ip_list:
        count += 1
        print(ip)
    
    print("\nA total of {} IPs were found in the file.".format(count))
