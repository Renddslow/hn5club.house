class Character:
	def __init__(self, username):
		self.user = username
		self.character = models.Characters.get(username = self.user)
		self.attack_multiplier = 1

	
	def create_character(self, args):
		args['character_username'] = self.user
		models.Characters.create(**args)
	
	
	def attack(self):
		attack_points = self.character.ap
		power = self.attack_multiplier * attack_points
		return power


	def level_up(self):
		current_level = self.character.level
		self.character.level = current_level + 1
		self.character.save()
