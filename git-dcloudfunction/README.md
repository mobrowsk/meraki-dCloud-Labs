To get the bot up and running, it needs to be ran from the terminal, while an ngrok instance is running. By default, I have it running using this sequence of events.

Run this command from the admin command prompt:
  
	ngrok http 5000

Copy the forwarding URL and paste it into the JIRA Webhook's URL with "/webhook" at the end:

	<forwarding url>/webhook

Run the python file from the terminal:

	python '.\MerakiTicketingBot - Final.py'

It now listens for JIRA changes and pushes the updates to the requisite webex spaces.
