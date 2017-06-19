#!/usr/bin/python
#coding=utf-8


from gi.repository import Gtk, GLib
import pygtk 

import random
import locale
import gettext
import os
import time 
import threading
import gobject
import json


class View():

	def __init__(self):
		# Cargamos el Gtk.Builder y nuestra interfaz creada en Glade
		self.builder = Gtk.Builder()
		self.builder.add_from_file("sprint1.glade")

		# Centramos y cambiamos el tamaño por defecto de las ventanas de nuestra aplicación
		self.window = self.builder.get_object("window")
		
		self.window_anadir = self.builder.get_object("window_anadir")
		
		self.window.set_default_size(800,500)
		self.window.set_position(Gtk.WindowPosition.CENTER)

		self.window_anadir.set_default_size(500,250)
		self.window_anadir.set_position(Gtk.WindowPosition.CENTER)
	
		# Cargamos la información de nuestro modelo en el treeview
		self.db_model=self.builder.get_object("liststore1")
		self.treeview = self.builder.get_object("treeview1")
		# Creamos nuestro Treeview y le asignamos el modelo
		self.create_treeview_view()

	# Conectamos las señales definidas en Glade con nuestras funciones 
	def register_handlers(self, handler):
		self.builder.connect_signals(handler)
	
	def run(self):
		self.window.show_all() #mostramos la ventana principal de nuestra aplicación
		Gtk.main()

	# TREEVIEW
	def create_treeview_view(self):
		json_data=open("./db_movies.json", "r")
		movies_data=json.load(json_data)

		for item in movies_data:
			self.db_model.append([item['titulo'], item['genero'], item['director'], item['ano'], item['pais']])
		json_data.close()


	# COMUNICACION CON VIEW
	def delete_window_anadir(self):
		self.window_anadir.hide()


	def show_window_anadir(self):
		self.window_anadir.show_all()
		self.window.hide()
		

	def show_dialog_eliminar(self):
		self.dlg_el=self.builder.get_object("dialog_eliminar")
		self.dlg_el.set_transient_for(self.window)
		self.dlg_el.run()
		self.dlg_el.hide()
		

	def show_dialog_anadir(self):
		self.dlg_an=self.builder.get_object("dialog_anadir")
		self.titulo_entrada=self.builder.get_object("entry1")
		self.genero_entrada=self.builder.get_object("entry2")
		self.director_entrada=self.builder.get_object("entry3")
		self.ano_entrada=self.builder.get_object("entry4")
		self.pais_entrada=self.builder.get_object("entry5")
		self.dlg_an.set_transient_for(self.window_anadir)
		self.dlg_an.run()
		self.dlg_an.hide()
		

	def cancel_window_anadir(self):
		self.window.show_all()		
		self.window_anadir.hide()
		

	def dialog_eliminar_acept(self):
		self.window.show_all()
		self.dlg_el.hide()
		

	def dialog_eliminar_cancel(self):
		self.window.show_all()
		self.dlg_el.hide()
	
	def hide_dialog_eliminar(self):
		self.dlg_el.hide()	

	def dialog_anadir_acept(self):
		self.window.show_all()
		self.dlg_an.hide()	

	def dialog_anadir_cancel(self):
		self.window_anadir.show_all()
		self.dlg_an.hide()
	


class Controller:
	def __init__(self, model, view):
		self.model = Model()
		self.view = View()
		self.view.register_handlers(self)

	def run(self):
		self.view.run()

	def get_movies_from_model(self):
		return self.model.get_movies_DB()


	# SEÑALES DE DELETE_EVENT
	def on_window_delete_event(self, widget, event):
		self.model.modelo_guardar(self.view)
		Gtk.main_quit()
				
	def on_window_anadir_delete_event(self, window_anadir, event): #view: delete_window_anadir 
		self.view.delete_window_anadir()

	# SEÑALES ABOUT_DIALOG
	def on_aboutdialog_activate(self, aboutdialog): #view: aboutdialog_run	
		aboutdialog.run()		
	
	def on_aboutdialog_close(self, aboutdialog, id): #view: aboutdialog_hide
		aboutdialog.hide()
		return True



	# SEÑALES PARA BOTONES
	def on_button3_clicked(self, widget): #view: show_window_anadir
		self.view.show_window_anadir()

	def on_button4_clicked(self, widget): #view: show_dialog_eliminar
		self.view.show_dialog_eliminar()


	def on_button1_clicked(self, widget): #view: show_dialog_anadir
		self.view.show_dialog_anadir()	
		

	def on_button2_clicked(self, widget): #view: cancel_window_anadir
		self.view.cancel_window_anadir()
	

	def on_button7_clicked(self, widget): #view: dialog_eliminar_acept
		self.model.modelo_eliminar(self.view)
		self.view.dialog_eliminar_acept()
	

	def on_button8_clicked(self, widget): #view: hide_dialog_eliminar
		self.view.hide_dialog_eliminar()		
			

	def on_button5_clicked(self, widget): #view: dialog_anadir_acept
		self.model.modelo_anadir(self.view)
		self.view.dialog_anadir_acept()


	def on_button6_clicked(self, widget): #view: dialog_anadir_cancel
		self.view.dialog_anadir_cancel()


	def on_edited_clicked(self, cell, path, new_text):
		self.model.modelo_editar(self.view,path,new_text)


class Model:

	def __init__(self):
		pass

	def get_movies_DB(self):
		return json.load(open('db_movies.json'))

	#ANADIR PELICULA 
	def modelo_anadir(self,view):
		titulo=Gtk.Entry.get_text(view.titulo_entrada)
		genero=Gtk.Entry.get_text(view.genero_entrada)
		director=Gtk.Entry.get_text(view.director_entrada)
		ano=Gtk.Entry.get_text(view.ano_entrada)
		pais=Gtk.Entry.get_text(view.pais_entrada)

		# -------COMPROBAR NO AÑADIR REPETIDOS
		#añadimos
		view.db_model.append([titulo, genero, director, ano, pais])

		Gtk.Entry.set_text(view.titulo_entrada,"")
		Gtk.Entry.set_text(view.genero_entrada,"")
		Gtk.Entry.set_text(view.director_entrada,"")
		Gtk.Entry.set_text(view.ano_entrada,"")
		Gtk.Entry.set_text(view.pais_entrada,"")

	# ELIMINAR PELICULA
	def modelo_eliminar(self,view):
		selection = view.treeview.get_selection()
		x1, rows = selection.get_selected_rows()
		iters = []
		for row in rows:
			iters.append(view.db_model.get_iter(row))
		for i in iters:
			if i is not None:
				view.db_model.remove (i)

	#EDITAR PELICULA 
	def modelo_editar(self,view,path,new_text):
		i = view.db_model.get_iter(path)
		aux=0
		for fila in view.db_model:
			if new_text==fila[0]:
				aux=1
		if new_text<>"" and aux==0:
			view.db_model.set_value(i, 0, new_text)

	# GUARDAR CAMBIOS 
	def modelo_guardar(self,view):
		json_data=open("./db_movies.json", "w+")
		json_data.write("[")
		aux=0
		for i in view.db_model:
			if aux>0:
				json_data.write(",")
			json.dump({"titulo":i[0], "genero":i[0],"director":i[0],"ano":i[0],"pais":i[0]}, json_data)
			aux=1
		json_data.write("]")
		json_data.close()

model=Model()
view=View()
controller=Controller(model, view)
view.register_handlers(controller)
view.run()
