from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie

from .search import search 
from .models import *

import json
import hashlib

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def is_pwd_protected(note):
	return not note.password == get_hash_string_SHA256('')

def get_hash_string_SHA256(string):
	hashed = hashlib.sha256(string.encode())
	result = hashed.hexdigest()
	return result


def home(request):
	return render(request,'index.html', {})

def view_note(request, temp_key, note_num):
	#:URL: notes/<str:temp_key>/<int:note_num>
	#return redirect('/')
	try:
		note = Note.objects.get(note_num=note_num)
	except Note.DoesNotExist:
		return HttpResponse(status=404)
	tk = TempKey.objects.get(note=note)
	if tk.used >= 2 or tk.str_key != temp_key:
		#Generate new str_key after being accessed once
		tk.str_key = generate_temp_key()
		tk.used = 0
		tk.save()
		return redirect(f'/notes/create')
	hour = note.date_created.hour +1
	hour = hour if hour > 9 else f'0{hour}'
	minute = note.date_created.minute
	minute = minute if minute > 9 else f'0{minute}'
	context = {
		'title': note.title,
		'content': note.content,
		'date': f'{months[note.date_created.month-1].title()} {note.date_created.day}, {note.date_created.year}',
		'time': f'{hour}:{minute}'
	}
	tk.used = tk.used + 1
	tk.save()
	return render(request, 'note.html', context)

def view_note_check(request, note_num):
	#/notes/{{num}}/view
	try:
		note = Note.objects.get(note_num=note_num)
	except Note.DoesNotExist:
		return HttpResponse(status=404)
	if is_pwd_protected(note):
		#Make a redirect to a password entry page
		return redirect(f'/notes/{note_num}/password')
	context = {
		'title': note.title,
		'content': note.content,
	}
	tk = TempKey.objects.get(note=note)
	return redirect(f'/notes/{tk.str_key}/{note.note_num}')
	#return render(request, 'note.html', context)

@ensure_csrf_cookie
def create_note(request):
	context = {}
	return render(request, 'createnote.html', context)

def delete_note(request):
	note_num = request.POST['note_num']
	try:
		note = Note.objects.get(note_num=note_num)
	except Note.DoesNotExist:
		return HttpResponse('failed')
	finally:
		note.delete()
		return HttpResponse('success')


def save_note(request):
	data = json.loads(request.body)
	title = data['title']
	content = data['content']
	password = data['password']
	if content.replace(' ','') and title.replace(' ',''):
		'''Go ahead and create and save'''
		try:
			new_note = Note(
				title=title.title(),
				content=content,
				password=password)
			new_note.save()
		except Exception as err:
			return HttpResponse(status='500')
		return HttpResponse(status='201')
	return HttpResponse("Empty body and/or title", status='401')

	
def get_search_results(request, search_key):
	titles = list(map(lambda n:n.title, Note.objects.all()))
	results = search(search_key, titles)
	# print("titles: ", titles)
	# print("Results: ",results)
	l = []
	def append_data(note):
		tk = TempKey.objects.get(note=note)
		d = {
			'title': note.title,
			'note_num': note.note_num,
			'str_key': tk.str_key,
		}
		l.append(d)

	for title in results:
		notes = Note.objects.filter(title=title)
		if len(notes) > 1:
			for note in notes:
				append_data(note)
		else:
			append_data(notes[0])

	response_data = {
		'notes': l
	}
	return JsonResponse(response_data)

@ensure_csrf_cookie
def password_entry(request, note_num):
	title = Note.objects.get(note_num=note_num).title
	context = {
		'title_short': title[:15],
		'num': note_num
	}
	return render(request, 'password.html', context)

def validate_password(request, note_num):
	value = request.body.decode()
	#note_id = request.POST['id']
	note = Note.objects.get(note_num = note_num)
	if get_hash_string_SHA256(value) == note.password:
		tempkey = TempKey.objects.get(note=note)
		return HttpResponse(f'key:{tempkey.str_key}')

	return HttpResponse(status=401)

def api_fetch(request, note_num):
	response = {
		'status': 'ok',
		'content': '',
		'title': ''
		}
	try:
		note = Note.objects.get(note_num=note_num)
		response['content'] = note.content
		response['title'] = note.title
		if not note.password == get_hash_string_SHA256(''):
			response['status'] = 'protected'
			return JsonResponse(response)
	except Note.DoesNotExist:
		response['status'] = 'does not exist'

	return JsonResponse(response)