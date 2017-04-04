import requests


class Servers:
	def __init__(self):
		auth = ""
		headers = {
			"Authorization": "Basic {}".format(auth),
			"Content-Type": "application/json"
		}
		base_url = "https://jira.hayneedle.com/rest/api/2/issue/"
		self.requests = {
			url = base_url,
			headers = headers
		}

	
	def get_servers_in_use(self):
		server_array = []
		servers = models.Servers.select().order_by(models.Servers.date_spun.desc())
		for server in servers.execute():
			server_dict = {
				"name": server.server_name,
				"qa": server.story_qa,
				"dev": server.story_dev,
				"ticket": {
					"name": server.story_ticket_name,
					"number": server.story_ticket_number
				}
			}
			server_array.append(server_dict)
		return server_array

	
	def spin_up_server(self, server, jira, qa):
		jira_info = self.get_jira_ticket(jira)
		server = models.Servers.create(
			server_name = server,
			story_qa = qa,
			story_dev = jira_info[0],
			story_ticket_number = jira,
			story_ticket_name = jira_info[1]
		)
