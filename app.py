import os
# Use the package we installed
from dotenv import load_dotenv
from slack_bolt import App
from slack import WebClient
from slack.errors import SlackApiError
import logging
logging.basicConfig(level=logging.DEBUG)
load_dotenv()
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
form = [
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "block_id": "name_visible",
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
                    "block_id": "category",
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
                    "block_id": "suggestion",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "What is your suggestion?",
                        "emoji": True
                    }
                }
            ]
submit_button = {
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
@app.view("view_1")
def handle_command_suggestion(ack, body, logger):
    handle_suggestion_action(ack, body, logger)

@app.command("/suggest")
def handle_suggestion(ack, body, logger):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view = {
            "type": "modal",
            "callback_id": "view_1",
            # body of the view
            "title": {"type": "plain_text", "text": "Make a Suggestion"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": form
        }
        

    )

@app.action("submit")
def handle_suggestion_action(ack, body, logger):
    ack()
    # print(body)
    user = body['user']['username']
    print("Handler")
    # logger.info(body)
    response = body['view']['state']['values']
    name_visible = response['name_visible']['radio_buttons-action']['selected_option']['value']
    category = response['category']['radio_buttons-action']['selected_option']['value']
    suggestion = response['suggestion']['plain_text_input-action']['value']
    name = "Anonymous"
    if name_visible == "yes": name = user
    try:
        response = client.chat_postMessage(
        channel="C027LB05V53",
        blocks=[{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "New Suggestion 💡"
			}
		},
        {
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Suggestion Category 📚*: {}".format(category)
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Suggestion ✅*: {}".format(suggestion)
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*From*: {}".format(name)
			}
		},
		{
			"type": "divider"
		}]
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        print(e.response["error"])  # str like 'invalid_auth', 'channel_not_found'
    finally:
        with open('log.txt', 'a+') as f:
            f.write('{}, {}, {}\n'.format(user, category, suggestion))
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
        "blocks": form + [submit_button]
      }
    )
  
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))