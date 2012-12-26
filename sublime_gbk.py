#coding: utf8

import sublime, sublime_plugin
import os, re
import urllib

TEMP_PATH = os.path.join(os.getcwd(), 'tmp')
SEPERATOR = '                '

def gbk2utf8(view):
	try:
		reg_all = sublime.Region(0, view.size())
		gbk = view.substr(reg_all).encode('gbk')
	except:
		gbk = file(view.file_name()).read()
		text = gbk.decode('gbk')
		
		file_name = view.file_name().encode('utf-8')

		tmp_file_name = os.path.basename(file_name)
		tmp_file = os.path.join(TEMP_PATH, tmp_file_name)

		f = file(tmp_file, 'w')
		f.write(text.encode('utf8'))
		f.close()

		window = sublime.active_window()
		
		v = window.find_open_file(tmp_file)

		if(not v):
			v = window.open_file(tmp_file)

		v.settings().set('file_src', file_name)

		window.focus_view(view)
		window.run_command('close')
		window.focus_view(v)

		sublime.set_timeout(lambda: sublime.status_message('gbk encoding detected, open with utf8.'), 100)

def saveWithEncoding(view, file_name = None, encoding = 'gbk'):
	if(not file_name):
		file_name = view.file_name()
	reg_all = sublime.Region(0, view.size())
	text = view.substr(reg_all).encode(encoding)
	gbk = file(file_name, 'w')
	gbk.write(text)
	gbk.close()

	sublime.set_timeout(lambda: sublime.status_message('Saved %s (%s)' % (file_name, encoding.upper())), 100)

class EventListener(sublime_plugin.EventListener):
	def on_load(self, view):
		gbk2utf8(view)
	def on_post_save(self, view):
		if(view.file_name().startswith(TEMP_PATH)):
			file_name = view.settings().get('file_src', None)
			saveWithEncoding(view, file_name)

class SaveWithGbkCommand(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
	def run(self, edit):
		file_name = self.view.file_name()

		if(not file_name):
			return

		if(not file_name.startswith(TEMP_PATH)):
			saveWithEncoding(self.view)
			sublime.active_window().run_command('close')
			sublime.active_window().open_file(self.view.file_name())
		else:
			sublime.active_window().run_command('save')

class SaveWithUtf8Command(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
	def run(self, edit):
		file_name = self.view.file_name()

		if(not file_name):
			return

		if(file_name.startswith(TEMP_PATH)):
			file_name = view.settings().get('file_src', None)
			saveWithEncoding(self.view, file_name, 'utf-8')
			sublime.active_window().run_command('close')
			sublime.active_window().open_file(file_name)
		else:
			sublime.active_window().run_command('save')