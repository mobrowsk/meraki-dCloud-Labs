import meraki
import requests
import json
import os
from dotenv import load_dotenv


# Defining your API key as a variable in source code is discouraged.
# This API key is for a read-only docs-specific environment.
# In your own code, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

API_KEY = os.environ.get("MERAKI_DASHBOARD_API_KEY", "Could not retrieve API key")

load_dotenv()


# Set your Meraki API key here
MERAKI_API_KEY = os.environ['MERAKI_DASHBOARD_API_KEY']
#os.environ.get("MERAKI_DASHBOARD_API_KEY", "Could not retrieve API key")

# Base URL for Meraki Dashboard API
MERAKI_BASE_URL = 'https://api.meraki.com/api/v1'

# The headers to use with each API request
HEADERS = {
    'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
    'Content-Type': 'application/json'
}

org_mapping = {'215332': 'Pod 1', '351024': 'Pod 2', '351028' : 'Pod 3', '622622648483971160': 'Pod 4', '622622648483971212': 'Pod 5', '660903245316620327': 'Pod 6','660903245316620328': 'Pod 7'}

specific_string1 = ['N_622622648484016986', 'N_673288144291938036', 'N_673288144291921351', 'N_622622648484227786', 'N_622622648484015753', 'N_660903245316626413', 'N_660903245316626542' ]
specific_string2 = "ISP_Disti"
specific_string3 = "MX"
specific_string4 = "MS"
specific_string5 = "MR"

class Meraki:
    def __init__(self) -> None:
        pass
    
    def get_meraki_device_availabilities(self, organization_ids):
        """
        Retrieves Meraki devices for each organization ID in the list and outputs to a file.
        
        :param organization_ids: A list of organization IDs.
        """
        devices_per_org = {}
        #influx_dict = {}
        for org_id in organization_ids:
            # Build the URL to get devices for an organization
            url = f"{MERAKI_BASE_URL}/organizations/{org_id}/devices/availabilities"
            
            # Make the GET request to retrieve the devices
            response = requests.get(url, headers=HEADERS)
            '''
                response = self.dashboard.organizations.getOrganizationDevicesStatuses(
                org_id, total_pages='all'
                )'''

            # Check if the request was successful
            if response.status_code == 200:
                # Add the list of devices to the dictionary
                devices_per_org[org_id] = response.json()
                for device in devices_per_org[org_id]:
                    device['organizationId'] = org_id
                    if device['status'] == 'online':
                        device['status_numerical'] = 1
                    else:
                        device['status_numerical'] = 0
                    if org_id in org_mapping:
                        device['org_name'] = org_mapping[org_id]
                    else:
                        device['org_name'] == "Org not found"

                
            else:
                print(f"Failed to retrieve devices for organization {org_id}")
                devices_per_org = []

                '''            
        # Write the dictionary to a JSON file
            with open('devices.json', 'w') as json_file:

                json.dump(devices_per_org, json_file, indent=4)
                '''
        return devices_per_org
        

dashboard = meraki.DashboardAPI(
    output_log=False,
    # log_file_prefix=os.path.basename(__file__)[:-3],
    # log_path='',
    print_console=False
)        

