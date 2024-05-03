import functions_framework
from flask import Flask, request
import json
import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv

# Declaring the token variables, taken from the environment variables
teams_token = os.getenv("TEAMS_BOT_TOKEN")
roomId = os.getenv("WEBEX_ROOM_ID")

def send_message_to_webex(message):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {teams_token}", # Webex Bot Token
        "Content-Type": "application/json"
    }
    payload = {
        "roomId": roomId,  # ID of the room you want to send the message to
        "markdown": message
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)

@functions_framework.http
def webhook(request):

        # Check if the request method is POST.
    if request.method != "POST":
        return 'Only POST requests are accepted', 405
    
    data = json.loads(request.data)
    print("Received data:", data)  # Process your data here
    project_name = data['issue']['fields']['project']['name'] # Name of the project that is being watched
    custom_field_value = data.get('issue', {}).get('fields', {}).get('customfield_10059') # Checking to see if the json data contains specific custom fields
    
    # Define a list of project names you want to listen to - 
    listened_projects = ['My Kanban Project', 'Support']

    if project_name in listened_projects:    
        # Parse the JSON data for issue information and extraction of required fields
        webhook_event = data['webhookEvent']
        issue_key = data['issue']['key']
        issue_summary = data['issue']['fields']['summary']
        
        if custom_field_value:
            organization_name = data['issue']['fields']['customfield_10059']
            network_name = data['issue']['fields']['customfield_10060']
            device_model = data['issue']['fields']['customfield_10044']

        issue_url = data['issue']['self']  # This is the API URL, I need the front-end URL

        # Replace the API URL with the front-end URL if necessary
        # Assuming 'self' field gives something like 'https://your-domain.atlassian.net/rest/api/2/issue/ISSUE-KEY'
        # I need to transform it to 'https://your-domain.atlassian.net/browse/ISSUE-KEY'
        domain = issue_url.split('/rest')[0]
        issue_browse_url = f"{domain}/browse/{issue_key}"

        assignee_info = data['issue']['fields'].get('assignee')  # This could be None if no assignee is set

        #Assignee name declaration
        assignee_name = 'Unassigned'

        # If an assignee is set, get the assignee's display name
        if assignee_info and 'displayName' in assignee_info:
            assignee_name = assignee_info['displayName']
        else:
            assignee_name = "Unassigned"

        # Message creation
        # A bunch of other pieces of information can be input here.    
        
        if custom_field_value:
            message = f"### Update from JIRA: {project_name}\n [{issue_key} - {issue_summary}]({issue_browse_url}) \n Webhook Event: {webhook_event} \n Organization Name: {organization_name} \n Network Name: {network_name} \n Device Model: {device_model} \n Assignee: {assignee_name}"
        else:
            message = f"### Update from JIRA: {project_name}\n [{issue_key} - {issue_summary}]({issue_browse_url}) \n Webhook Event: {webhook_event}. \n Assignee: {assignee_name}" # If the custom entries aren't found


        #send_message_to_webex(data, issue_key, issue_summary, issue_browse_url, assignee_name)
        send_message_to_webex(message)
    else:
        print(f"Ignoring issue from project: {project_name}")

    return "Success", 200