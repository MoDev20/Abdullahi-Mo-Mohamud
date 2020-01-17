from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import date

def register(request):
	return render(request, 'index.html') 

def createuser(request):
	print(request.POST)
	errors = User.objects.userValidator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		hashedpassword = bcrypt.hashpw(request.POST ['pw'].encode(), bcrypt.gensalt()).decode()
		newuser = User.objects.create(firstName = request.POST['fname'], lastName = request.POST ['lname'], email = request.POST['useremail'], password = hashedpassword )
		print (newuser.id)
		request.session['loggedInID'] = newuser.id
	return redirect('/book')

def book(request):
	if 'loggedInID' not in request.session:
		return redirect('/')
	loggedInUser = User.objects.get(id=request.session['loggedInID'])
	context = {
		'loggedUser': loggedInUser,
		'allbooks': Book.objects.all()
	}
	return render (request, 'book.html', context)	

def login(request):
	validationErrors = User.objects.loginValidator(request.POST)
	if len(validationErrors) > 0:
		for key, value in validationErrors.items():
			messages.error(request, value)
		return redirect('/')
	loggedInUser = User.objects.get(email = request.POST['useremail'])
	print("*******")
	print(loggedInUser)
	print("********")
	request.session['loggedInID'] = loggedInUser.id
	return redirect('/book')

def add(request):
	print(request.POST)
	loggedInUser = User.objects.get(id=request.session['loggedInID'])
	newBook = Book.objects.create(title = request.POST['title'], desc = request.POST['desc'], creator = loggedInUser)
	return redirect('/book')

def delete(request, bookId):
	book = Book.objects.get (id = bookId)
	book.delete()
	return redirect('/book')

def edit(request, bookId):
	print(request.POST)
	loggedInUser = User.objects.get(id=request.session['loggedInID'])
	book = Book.objects.get (id = bookId)
	context = {
	'loggedUser' : loggedInUser,

	}
	return redirect('edit.html', context)

def update(request, bookId):
	print(request.POST)
	book = Book.objects.get(id = bookId)
	book.title = request.POST['title']
	book.desc = request.POST['desc']
	book.save()
	return redirect('/book')

def display(request, bookId):
	if 'loggedInID' not in request.session:
		return redirect('/')
	loggedInUser = User.objects.get(id=request.session['loggedInID'])
	context = {
		'loggedUser' : loggedInUser,
		'book': Book.objects.get(id=bookId)
	}
	return render(request, 'showbook.html', context)

def addfavor(request, bookId):
	if 'loggedInID' not in request.session:
		return redirect('/')
	print(request.POST)
	loggedInUser = User.objects.get(id=request.session['loggedInID'])
	book = Book.objects.get(id=bookId)
	book.like.add(loggedInUser)
	return redirect('/book')
	
def removefavor(request, bookId):
	if 'loggedInID' not in request.session:
		return redirect('/')
	print(request.POST)
	loggedInUser = User.objects.get(id=request.session['loggedInID'])
	book = Book.objects.get(id=bookId)
	book.like.remove(loggedInUser)
	return redirect('/book')

def logout(request):
	request.session.clear()
	return redirect('/')