import meraki
import json
from dotenv import load_dotenv
import os

# Defining your API key as a variable in source code is discouraged.
# This API key is for a read-only docs-specific environment.
# In your own code, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

API_KEY = os.environ.get("MERAKI_DASHBOARD_API_KEY", "Could not retrieve API key")

dashboard = meraki.DashboardAPI(
    output_log=False,
    # log_file_prefix=os.path.basename(__file__)[:-3],
    # log_path='',
    print_console=False
)

def get_orgs():

    response = dashboard.organizations.getOrganizations()

    return response

def get_organization(org_id):

    response = dashboard.organizations.getOrganization(
    org_id
    )

    org_name = response['name']
    return org_name

def get_networks(organization_id:str):

    response = dashboard.organizations.getOrganizationNetworks(
    organization_id, total_pages='all'
)
    return response  

def get_network_name(network_id):

    response = dashboard.networks.getNetwork(
        network_id
    )

    network_name = response['name']
    return network_name

def get_device(serial):

    response = dashboard.devices.getDevice(
        serial
    )
    device_info = response

    return device_info
def get_device_status(organization_id:str, serial:str):

    response = dashboard.organizations.getOrganizationDevicesStatuses(
    organization_id
    )
    try:
        for device in response:
            if serial in device['serial']:
                status = device['status']
                print("Device found!")
                
    except:
        print("not in forloop")

    return status

def get_offline_devices(organization_id:str):

    response = dashboard.organizations.getOrganizationDevicesStatuses(
    organization_id, 
    statuses = 'offline'
)
    return response

def get_meraki_devices(organization_ids):
    """
    Retrieves Meraki devices for each organization ID in the list and outputs to a file.
    
    :param organization_ids: A list of organization IDs.
    """
    devices_per_org = {}
    
    for org_id in organization_ids:
        response = dashboard.organizations.getOrganizationDevices(
            org_id, total_pages='all'
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            # Add the list of devices to the dictionary
            devices_per_org[org_id] = response.json()
        else:
            print(f"Failed to retrieve devices for organization {org_id}")
            devices_per_org[org_id] = []
    
    # Write the dictionary to a JSON file
    with open('devices.json', 'w') as json_file:
        json.dump(devices_per_org, json_file, indent=4)

