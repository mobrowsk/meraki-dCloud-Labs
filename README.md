# dCloud Meraki Labs: Jira Ticketing Automation and Meraki Lab Outage Dashboard
This project does 3 main things:
  1. Creates an automated support process between offline/disconnected Meraki Lab devices and dCloud Team.
  2. Creates a dashboard to record outages and trends in device outages.
  3. Create Webex Bot to notify lab admins/users of offline devices.​

This diagram provides a representation of how these elements complement one another:

<img width="1474" alt="image" src="https://github.com/mobrowsk/meraki-lab-functions/assets/165918441/bde0b40a-15a7-4d94-8c07-01b2b0b5ecb0">


## Table of Contents

- [Meraki Alert to JIRA Ticket](#meraki-alert-to-jira-ticket)
  - [Usage 1](#usage-1)
  - [Features 1](#features-1)
  - [Requirements 1](#requirements-1)
  - [Configuration 1](#configuration-1)
  - [Endpoints 1](#endpoints-1)
  - [Deployment 1](#deployment-1)
  - [Function Description-1](#function-description-1)
- [Reporting Dashboard with InfluxDB and Grafana](#reporting-dashboard-with-influxdb-and-grafana)
  - [Usage 2](#usage-2)
  - [Features 2](#features-2)
  - [Requirements 2](#requirements-2)
  - [Deployment 2](#deployment-2)
  - [Function Description 2](#function-description-s)
- [Webex Bot for JIRA Ticket notifications](#webex-bot-for-jira-ticket-notifications)
  - [Usage 3](#usage-3)
  - [Features 3](#features-3)
  - [Requirements 3](#requirements-3)
  - [Function Description 3](#functions-description-3)
- [Contributing](#contributing)
- [License](#license)

## Meraki Alert to JIRA Ticket

This Python application is designed to integrate Cisco Meraki alerts with Atlassian JIRA. When a Meraki device goes offline, the script will trigger after a specified delay, check the device's status, search for upstream offline devices, and create a JIRA ticket if necessary.

### Usage

This application is designed to handle POST requests with JSON payloads corresponding to Meraki alert data. Ensure you have it set up to receive and process webhooks sent by the Meraki dashboard.

### Features

- Loads environment variables for API keys and project keys.
- Checks if the alerting Meraki device is still offline.
- Searches for upstream offline devices.
- Retrieves open issues from JIRA.
- Creates a ticket in JIRA for the offline device if no open issue is found.
- Uses threading to delay JIRA ticket creation.
- Responds to Meraki webhook alerts.

### Requirements

- Python 3.x
- Pipenv or virtualenv (optional, but recommended)

### Configuration

Before running the application, you must configure the necessary environment variables. Create a `.env` file in the project root and provide the following keys:

- `MERAKI_DASHBOARD_API_KEY`: Specify your Meraki Dashboard API key here.
- `JIRA_PROJECT_KEY`: Enter the key for the JIRA project you are integrating with.
- `JIRA_EMAIL`: Your email address associated with the JIRA account.
- `JIRA_API_TOKEN`: The API token generated from your JIRA account for authentication.

### Endpoints

The application features the following endpoint:

- `/handler`: The primary route that captures webhook POST requests from Meraki. It initiates the process of monitoring the device status and, after a predefined delay, possibly creates a JIRA ticket based on the alert information received.

### Deployment

For deployment, this application is suitable for serverless platforms (in this case GCP Cloud Functions) or any hosting service with support for Python and Flask applications. Make sure the service can receive and forward POST requests from Meraki to the application.

### Function Descriptions

Below is a brief overview of the key functions within the application and their respective roles:

- `alert_tracker(alert_org, alert_serial)`: Checks the current status of a device by its serial number within a specified organization to determine if it's still offline.

- `search_string_in_data(data, search_strings)`: Searches for specific strings within a data structure, which can be either a dictionary or a list.

- `upstreamOfflineDeviceCheck(alert_org)`: Identifies any upstream devices that are offline in the provided organization.

- `getOpenIssues()`: Fetches unresolved issues from the configured JIRA project using JQL (JIRA Query Language).

- `createTicket(org_id, device_serial)`: Creates a new JIRA ticket with the details of the offline device, including organization, network, and device information.

- `jira_logic(*args)`: Orchestrates the logic to check device status, search for upstream offline devices, check for existing JIRA issues, and potentially create a new JIRA ticket.

- `handler(request)`: Serves as the main entry point for the application, processing incoming POST requests from Meraki webhooks. It parses the request data, starts a delayed execution of the JIRA logic, and returns a JSON response.

Each function is designed to handle specific parts of the integration workflow, from initial alert processing to potential ticket creation in JIRA.

## Reporting Dashboard with InfluxDB and Grafana

This Python application is designed to sync device availability data from Cisco Meraki organizations to an InfluxDB database. It regularly fetches the status of devices from multiple Meraki organizations and writes the information to InfluxDB.

### Usage
Run `main.py` to start the application. It will perform the following actions in a loop:

- Invoke `update_deviceAvailabilities()` to fetch Meraki device data and write to InfluxDB.
- Wait for a specified interval (default 300 seconds) before repeating the process.

### Features

- Fetches device availability data from specified Meraki organizations.
- Writes device status and metadata to InfluxDB.
- Operates at a regular interval set by the user.
### Requirments

- Python 3.x
- Access to a Cisco Meraki Dashboard with API enabled.
- An InfluxDB instance.

### Configuration

Set the following environment variables in your `.env` file:

- `MERAKI_DASHBOARD_API_KEY`: Your Meraki Dashboard API key.
- `INFLUXDB_URL`: The URL of your InfluxDB instance.
- `INFLUXDB_TOKEN`: Your InfluxDB authentication token.
- `INFLUXDB_ORG`: Your InfluxDB organization name.
- `INFLUXDB_BUCKET`: The bucket name in your InfluxDB where data will be stored.

### Deployment

This application can be deployed on any system capable of running Python scripts, as long as it has network access to both the Meraki API and the InfluxDB instance.

### Connecting InfluxDB to Grafana
In order to create a dashboard, data from InfluxDB must be sent to Grafana. To do this, navigate to
Grafana and hover over the settings icon on and click ‘Data sources’.

Click ‘Add data source’ and search for InfluxDB. You will now need to input the details of the
InfluxDB bucket. Set the query language to Flux, the URL to http://localhost:8086 (or
http://127.0.0.1:8086, depending on what URL you are using), set Access to ‘Server (default)’,
enable Basic auth, enter your organisation ID, the name of the default bucket and the API token for
the bucket you generated.

Click ‘Save & test’. You should a green tick appear with a message saying the bucket has been found.

To import the dashboard, hover over the four squares icon and click ‘Browse’. Click ‘Import’ and upload the
included JSON file.

### Function Description

- `update_deviceAvailabilities()`: Fetches device availability data for a predefined list of organization IDs and writes this data to InfluxDB using the `InfluxDB` class from `testInflux.py`.

- `InfluxDB.writeDevicestoDB(meraki_response)`: Takes the response from the Meraki API and writes formatted data points to InfluxDB.

- `Meraki.get_meraki_device_availabilities(organization_ids)`: Retrieves the availability status of devices across multiple organizations as specified by the `organization_ids` list.

## Webex Bot for JIRA Ticket notifications
This application is designed to integrate JIRA with Cisco Webex by receiving webhook notifications from JIRA and sending alerts to a specified Webex Teams room. It is ideal for teams looking to enhance real-time collaboration by getting updates directly in their communication platform.

### Usage
 - When configured, the application listens for POST requests from JIRA. If the event relates to one of the pre-defined projects and contains specified custom fields, it sends a detailed message to the configured Webex Teams room.
### Features
 - Real-Time Notifications: Sends instant updates from JIRA to Webex Teams.
 - Custom Field Support: Handles custom JIRA fields for detailed notifications.
 - Security: Utilizes environment variables for secure storage of sensitive data like API tokens and room IDs.
### Requirments
 - flask
 - python-dotenv
 - requests library
 - functions-framework==3.*
### Function Description
 - send_message_to_webex(message): Sends a formatted message to the specified Webex Teams room.
 - webhook(request): Handles incoming POST requests from JIRA, processes the data and formats the data, and triggers the Webex notification function.

## Contributing

Contributions to this project are welcome! To contribute, please fork the repository, make your changes, and submit a pull request with a clear description of your improvements.

## License

The code in this project is open source, licensed under the MIT License. For the full license text, refer to the `LICENSE` file in this repository.
