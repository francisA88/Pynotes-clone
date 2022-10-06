from django.db import models

import hashlib
from random import randint

def generate_temp_key():
	chars = ("".join(map(str, range(10)))) + ''.join([chr(i) for i in range(97,97+26)]) + ''.join([chr(j) for j in range(65, 65+26)])
	key = ''.join([
		chars[randint(0,len(chars)-1)] for i in range(15) 
		])
	return key

class Note(models.Model):
	content = models.CharField(max_length=1500, default='')
	title = models.CharField(max_length=30, default='No Title')
	password = models.CharField(max_length=70, default='')
	note_num = models.IntegerField(default=0)
	openly_modifiable = models.BooleanField(default=False)
	can_be_deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def save(self, **kws):
		self.title = self.title.title()
		self.note_num = len(self.__class__.objects.all()) + 1
		hashed_pwd = hashlib.sha256(self.password.encode())
		hashed_pwd = hashed_pwd.hexdigest()
		self.password = hashed_pwd
		super().save(**kws)
		#Create a TempKey class for this note
		TempKey.objects.create(str_key=generate_temp_key(), note=self)
		##########


class TempKey(models.Model):
	used = models.IntegerField(default= 0)
	str_key = models.CharField(default=generate_temp_key(), max_length=15)
	note = models.ForeignKey(Note, on_delete=models.CASCADE)
