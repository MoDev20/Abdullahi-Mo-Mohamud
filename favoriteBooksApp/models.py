from __future__ import unicode_literals
from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
	def userValidator(self, postData):
		errors = {}
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		emailMatch = User.objects.filter(email = postData['useremail'])
		print('*********')
		print(emailMatch)
		print('*********')
		if len(postData['fname']) < 2:
			errors['firstName'] = "First Name should be at least be 2 characters"
		if len(postData['lname']) < 2:
			errors['lastName'] = "Last Name should be at least be 2 characters"
		if len(postData['useremail']) < 2:
			errors['emailreq'] = "Valid Email is required for registration"
		elif not EMAIL_REGEX.match(postData['useremail']): errors['emailinvalid'] = "Invalid email address!"
		if len(emailMatch) > 0:
			errors['emailused'] = "Email is used already"
		if len(postData['pw']) < 8:
			errors['password'] = "Password must be at least be 8 characters"
		if (postData['pw']) != (postData['cpw']):
			errors['cpw'] = "Password and Confirmation must be a match"
		return errors
		
	def loginValidator(self, postData):
		errors ={}
		emailMatch = User.objects.filter(email = postData['useremail'])
		
		if len(emailMatch) == 0:
			errors["emailError"] = "No user with such email address; please register"
			print(emailMatch)
		else:
			loggedUser = emailMatch[0]
			if bcrypt.checkpw(postData['pw'].encode(), loggedUser.password.encode()):
				print("password match")
			else:
				errors["passwordError"] = "Invalid password"
				print("failed password")
		return errors

class BookManager(models.Manager):
	def bookValidator(self, postData):
		errors = {}
		if len(postData['title']) < 2:
			errors['quoter'] = "Qouted By should be at least 2 characters"
		if len(postData['desc']) < 10:
			errors['desc'] = "Message should be at least be 10 characters"
		return errors

class User(models.Model):
	firstName = models.CharField(max_length=255)
	lastName =  models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Book(models.Model):
	title = models.CharField(max_length=255)
	desc =  models.CharField(max_length=255)
	creator = models.ForeignKey(User, related_name = "book_created", on_delete = models.CASCADE)
	isPosted = models.BooleanField(default = False)
	like = models.ManyToManyField(User, related_name = "book_liked")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	