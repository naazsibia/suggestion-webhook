import os
# Use the package we installed
from dotenv import load_dotenv
from slack_bolt import App
from slack import WebClient
from slack.errors import SlackApiError


load_dotenv()
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.action("submit")
def handle_some_action(ack, body, logger):
    ack()
    # print(body)
    user = body['user']['username']
    print(user)
    print(body['view']['state']['values'])
    logger.info(body)
    try:
        response = client.chat_postMessage(
        channel="C026XU9MHQU",
        type= "section",
        text="##Hello from your app! :tada:\nSo what's up?"
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        print(e.response["error"])  # str like 'invalid_auth', 'channel_not_found'

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "What's your name?",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "radio_buttons",
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "yes",
                                "emoji": True
                            },
                            "value": "yes"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "no",
                                "emoji": True
                            },
                            "value": "no"
                        }
                    ],
                    "action_id": "radio_buttons-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Would you like your name to be displayed with your suggestion?",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "radio_buttons",
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Lab Administration",
                                "emoji": True
                            },
                            "value": "Lab Administration"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Microproject",
                                "emoji": True
                            },
                            "value": "Microproject"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Ongoing Research Project",
                                "emoji": True
                            },
                            "value": "Ongoing Research Project"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "New Research Idea",
                                "emoji": True
                            },
                            "value": "New Research Idea",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Other",
                                "emoji": True
                            },
                            "value": "Other"
                        }
                    ],
                    "action_id": "radio_buttons-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "What is your suggestion for?",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "What is your suggestion?",
                    "emoji": True
                }
            },
            {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Submit",
						"emoji": True
					},
					"value": "submit",
					"action_id": "submit"
				}
			]
		}
        ]
      }
    )
  
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))