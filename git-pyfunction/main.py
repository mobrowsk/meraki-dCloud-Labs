import functions_framework
from flask import jsonify
import merakiCalls
import os, sys
import json
import time
from datetime import datetime
import threading
import requests
import httpx
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

from markupsafe import escape
#test
#load environment variables
API_KEY = os.environ.get("MERAKI_DASHBOARD_API_KEY", "Could not retrieve API key")
PROJECT_KEY = os.environ.get("JIRA_PROJECT_KEY", "Could not retrive project key")  # Replace with your project key
# Jira Authentication
USERNAME = os.environ.get("JIRA_EMAIL", "default_email@example.com")
API_TOKEN = os.environ.get("JIRA_API_TOKEN", "Could not retrieve Jira API token")  # Replace with your Jira API token


test_parameter = 1      # Set test_paramenter to 1 if running testing environment and 0 if production environment
orgs_list = ['215332', '351024', '351028', '622622648483971160', '622622648483971212', '660903245316620327', '660903245316620328']

def alert_tracker(alert_org, alert_serial): 
    print("Checking if alerting device is still offline")

    device_status = merakiCalls.get_device_status(alert_org, alert_serial)
    print(device_status)
    device_status_data = {'device-status': device_status}

    return device_status
def search_string_in_data(data, search_strings):
    # Ensure that search_strings is a list even if a single string is passed
    if isinstance(search_strings, str):
        search_strings = [search_strings]
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                for search_string in search_strings:
                    if search_string_in_data(value, search_string):
                        return True
            elif isinstance(value, str):
                for search_string in search_strings:
                    if search_string in value:
                        return True
    elif isinstance(data, list):
        for item in data:
            for search_string in search_strings:
                if search_string_in_data(item, search_string):
                    return True
    return False

def upstreamOfflineDeviceCheck(alert_org):
        print("Upstream offline devices being found")
        #alert_entry, alert_org, alert_network, alert_serial = args
        # Send GET request to Meraki for all offline device statuses
        offline_devices = merakiCalls.get_offline_devices(str(alert_org))
        print(offline_devices)
        upstreamOfflineDevice = {}

        specific_string1 = ['N_622622648484016986', 'N_673288144291938036', 'N_673288144291921351', 'N_622622648484227786', 'N_622622648484015753', 'N_660903245316626413', 'N_660903245316626542' ]
        specific_string2 = "ISP_Disti"
        specific_string3 = "MX"
        specific_string4 = "MS"
        specific_string5 = "MR"

        if search_string_in_data(offline_devices, specific_string1):
            print(f"The specific string {specific_string1} was found in the JSON response.")
            try:
                for device in offline_devices:
                    for device in offline_devices:
                        if specific_string1 in device['model']:
                            #print(device['serial'])
                            upstreamOfflineDevice = device['serial']
            except:
                print("not in forloop")

        elif search_string_in_data(offline_devices,specific_string2):
            print(f"The specific string {specific_string2} was found in the JSON response.")
            try:
                for device in offline_devices:
                    for device in offline_devices:
                        if specific_string2 in device['model']:
                            #print(device['serial'])
                            upstreamOfflineDevice = device['serial']
            except:
                print("not in forloop")

        elif search_string_in_data(offline_devices,specific_string3):
            print(f"The specific string {specific_string3} was found in the JSON response.")
            try:
                for device in offline_devices:
                    for device in offline_devices:
                        if specific_string3 in device['model']:
                            #print(device['serial'])
                            upstreamOfflineDevice = device['serial']
            except:
                print("not in forloop")

        elif search_string_in_data(offline_devices,specific_string4):
            print(f"The specific string {specific_string4} was found in the JSON response.")
            try:
                for device in offline_devices:
                    for device in offline_devices:
                        if specific_string4 in device['model']:
                            #print(device['serial'])
                            upstreamOfflineDevice = device['serial']
            except:
                print("not in forloop")

        elif search_string_in_data(offline_devices,specific_string5):
            print(f"The specific string {specific_string5} was found in the JSON response.")
            try:
                for device in offline_devices:
                    if specific_string5 in device['model']:
                        #print(device['serial'])
                        upstreamOfflineDevice = device['serial']
            except:
                print("not in forloop")
        else:
            print("The specific string was not found in the JSON response.")
            #include an upstream device null entry 

        return upstreamOfflineDevice

def getOpenIssues():
    # Jira setup
    jira_url = "https://obrowskimarie.atlassian.net/rest/api/3/search"  # Replace with your Jira domain

    # Basic authentication
    auth = HTTPBasicAuth(USERNAME, API_TOKEN)
   
    # JQL query to get all issues from a project
    jql_query = f"project={PROJECT_KEY}&resolution=unresolved" #set second query param to only get open tickets

    # Headers
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    # Request parameters
    query = {
    'jql': jql_query,
    'maxResults': 10,  # Adjust this value as needed
    }
    # Make the request
    response = httpx.get(
    jira_url,
    headers=headers,
    params=query,
    auth=auth
    )

    # Check for successful response
    if response.status_code == 200:
        # Parse the JSON response
        issues = json.loads(response.text)
        device_serial = {}
        # Do something with the issues, e.g., print the summary of each issue
        for issue in issues['issues']:
            # Initialize an empty string for the deviceSerial
            device_serial[issue['key']] = ""

            # Check if 'description' exists and is not None
            description = issue['fields'].get('description')
            if description:
                # Iterate through the content to find the deviceSerial
                for item in description.get('content', []):
                    for text_item in item.get('content', []):
                        if 'text' in text_item and 'Device Serial:' in text_item['text']:
                            # Extract the deviceSerial after the 'deviceSerial: ' part
                            device_serial[issue['key']] = text_item['text'].split('Device Serial: ')[1]
                            break  # Break the loop once we found the deviceSerial

            # Print or return the deviceSerial value
            #print(issue['key'], device_serial[issue['key']])

    else:
        print("Failed to retrieve issues:", response.status_code) 
    return device_serial

def createTicket(org_id:str, device_serial):

    # Jira setup
    base_url = "https://obrowskimarie.atlassian.net/"  # Replace with your Jira domain

    org_name = merakiCalls.get_organization(org_id)
    device_info = merakiCalls.get_device(device_serial)
    network_id = device_info['networkId']
    network_name = merakiCalls.get_network_name(network_id)
    device_name = device_info['name']
    device_model = device_info['model']


    # Basic authentication
    auth = HTTPBasicAuth(USERNAME, API_TOKEN)
    api_endpoint = f"/rest/api/3/issue"
    jira_url = f"{base_url}{api_endpoint}"  

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }
    ticket_summary = f"{org_name} {network_name} {device_model} outage"
    ticket_description = f"Organization: {org_name}\n" \
                f"Network: {network_name}\n" \
                f"Device Name: {device_name}\n" \
                f"Device Model: {device_model}\n" \
                f"Device Serial: {device_serial}\n" \
    
    payload = json.dumps({
        "fields": {
            # "assignee": {"id": "5b109f2e9729b51b54dc274d"},  # Uncomment if this field is allowed
            # Add other fields that are allowed on your screen
            "description" : {
                "content": [
                    {
                        "content" : [
                            {
                                "text" : ticket_description,
                                "type" : "text"
                            }
                        ],
                        "type": "paragraph"
                    }
                ],
                "type": "doc",
                "version": 1
            },
            "summary": ticket_summary,
            "issuetype": {"id": "10012"},  # Make sure this is correct
            "project": {"id": "10001"},  # Make sure this is correct
            # "parent": {"key": "SUP"},  # Uncomment if you are creating a sub-task and the parent key is correct
            # Add other fields that are allowed on your screen
        }
    })

    response = httpx.post(
    jira_url,
    data=payload,
    headers=headers,
    auth=auth
    )

    return print("Ticket created successfully"), 201

def jira_logic(*args):
    print("Jira logic being executed")
    alert_org, alert_network, alert_serial = args
    current_device_status = alert_tracker(alert_org, alert_serial)  # Step 1: Check if the alerting device is still offline after 1 hour
    print(f'currentd device stat is : {current_device_status}')
    # Check if the condition is met and stop running if it is
    if current_device_status == 'online':
        print(f"Condition met. Stopping execution at: {datetime.now()}")
        sys.exit() # If device is back online exit the script
    else:   
        #If aleriting device is still offline execute the following code
        upstreamOfflineDevice = upstreamOfflineDeviceCheck(alert_org)   # Step 2: Check for any upstream devices that are offline via Meraki Dashboard API
        deviceswithIssues = getOpenIssues() # Step 3: returns open tickets in the Jira Project
        print(upstreamOfflineDevice)
        print(deviceswithIssues)
        if upstreamOfflineDevice in deviceswithIssues: # Step 4: If the serial device of an upstream device is found to have an open ticket against it already no new ticket is created, else create a ticket for the most upstream device OR the alerting device.
            #Create no ticket!
            print("Ticket exists already")
        else:   
            #Create ticket for that serial.
            createTicket(alert_org, upstreamOfflineDevice)
            print("Create Ticket")
    return 200

@functions_framework.http
def handler(request):
    
    # Check if the request method is POST.
    if request.method != "POST":
        return 'Only POST requests are accepted', 405
    
    # Parse the incoming webhook data as JSON.
    try:
        webhook_data = request.get_json()
    except Exception as e:
        return f'Invalid JSON or no JSON provided: {e}', 400
    
    # If you want to do any processing with the webhook data, do it here.
    # Accessing the values for alert tracker
    organization_id = webhook_data.get('organizationId', [])
    network_id = webhook_data.get('networkId', [])
    device_serial = webhook_data.get('deviceSerial', [])
    
    print("OrgId:", organization_id)
    print("DeviceSerial", device_serial)
    # For demonstration purposes, we'll just print the data to the function's logs.
    print('Received webhook data:', webhook_data)
    args = (str(organization_id), str(network_id), str(device_serial))
    '''
    Timer Object to run a delayed function
    Run function to create Jira ticket after 1 hour of device outage
    '''
    # Specify the delay in seconds
    delay = 10  # Test = 10 seconds, Production = 3600 (set this automatically later)

    # Create a Timer object that will call the delayed_function after the delay
    timer = threading.Timer(delay, jira_logic, args=(*args,))
    # Start the timer
    timer.start()  

    # Return a JSON response with the received data.
    return jsonify(webhook_data), 200

