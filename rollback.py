import datetime
import models
import re
import requests


def get_time_since_rollback():
	last_rollback = models.Rollbacks.select().order_by(models.Rollbacks.rollback_id.desc()).limit(1).execute()
	for rollback in last_rollback:
		date_created = rollback.date_created
	time_difference = datetime.datetime.now() - date_created
	color = "green" if time_difference.days > 0 else "red"
	message = {
		"color": color,
		"message": "It has been {} days since an HN5/SEO rollback".format(time_difference.days),
		"notify": True,
		"message_format": "text"
	}
	return message


def parse_message(message):
	res_message = {
		"color": "gray",
		"message": "Whoops that is not a recognized rollback command. Ask Matt how to use this. He'll know",
		"notify": False,
		"message_format": "text"
	}
	if message.find(":blame") > -1:
		last_rollback = models.Rollbacks.select().order_by(models.Rollbacks.rollback_id.desc()).limit(1).execute()
		for rollback in last_rollback:
			last_rollback = rollback
		res_message = {
			"color": "red",
			"message": "The last roll back on {} to HNE-{} was caused by {}".format(
				last_rollback.date_created.strftime("%B %-d"),
				last_rollback.rollback_story_number,
				last_rollback.rollback_blame
			),
			"notify": False,
			"message_format": "text"
		}
	if message.find(":now") > -1:
		ticket_number = re.search('HNE-([0-9]{3,4})', message)
		if ticket_number:
			rollback_story_number = ticket_number.group(0)
			jira_info = get_jira_ticket(rollback_story_number)
			models.Rollbacks.create(
				rollback_story_number = int(rollback_story_number.replace("HNE-", "")),
				rollback_story_name = jira_info[1],
				rollback_blame = jira_info[0]
			)
			res_message = {
				"color": "purple",
				"message": "Well that sucks. Another rollback in the books. Thanks a lot {}".format(jira_info[0]),
				"notify": True,
				"message_format": "text"
			}
		else:
			res_message = {
				"color": "gray",
				"message": "Whoops, when using :now you need to supply a ticket number",
				"notify": False,
				"message_format": "text"
			}
	if message.find(":undo") > -1:
		last_rollback_query = models.Rollbacks.select().order_by(models.Rollbacks.rollback_id.desc()).execute()
		i = 0
		for rollback in last_rollback_query:
			if i < rollback.rollback_id:
				i = rollback.rollback_id
				last_rollback = models.Rollbacks.get(rollback_id = i)
				last_rollback.delete_instance()
			else:
				break
		res_message = {
			"color": "gray",
			"message": "Nice job deleting that rollback. I'm sure it was intentional. You wouldn't make mistakes",
			"notify": False,
			"message_format": "text"
		}
	return res_message


def get_jira_ticket(ticket_number):
	auth = "bW1jZWx3ZWU6SW50aGViZWdpbm5pbmd3YXN0aGVXb3JkSm9objE6MQ=="
	headers = {
		"Authorization": "Basic {}".format(auth),
		"Content-Type": "application/json"
	}
	url = "https://jira.hayneedle.com/rest/api/2/issue/{}".format(ticket_number)
	response = requests.get(url=url, headers=headers)
	blame = response.json()['fields']['customfield_11202']['displayName']
	ticket_name = response.json()['fields']['summary']
	return [blame, ticket_name]
