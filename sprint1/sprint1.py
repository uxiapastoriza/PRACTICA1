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

class Model:
	def get_movies_DB(self):
		return json.load(open('db_movies.json'))

	#ANADIR PELICULA
	def modelo_anadir(self,view):
		texto=Gtk.Entry.get_text(view.texto_entrada)
		aux=0
		for fila in view.store:
			if texto==fila[0]:
				aux=1
		if texto and aux==0:
			view.store.append([texto])
		Gtk.Entry.set_text(view.texto_entrada,"")

	# ELIMINAR PELICULA
	def modelo_eliminar(self,view):
		sel = view.tree.get_selection()
		x1, rows = sel.get_selected_rows()
		iters = []
		for row in rows:
			iters.append(view.store.get_iter(row))
		for i in iters:
			if i is not None:
				view.store.remove (i)

	#EDITAR PELICULA 
	def modelo_editar(self,view,path,new_text):
		i = view.store.get_iter(path)
		aux=0
		for fila in view.store:
			if new_text==fila[0]:
				aux=1
		if new_text<>"" and aux==0:
			view.store.set_value(i, 0, new_text)

	# GUARDAR CAMBIOS 
	def modelo_guardar(self,view):
		json_data=open("./db_movies.json", "w+")
		json_data.write("[")
		aux=0
		for i in view.store:
			if aux>0:
				json_data.write(",")
			json.dump({"titulo":i[0], "genero":i[0],"director":i[0],"ano":i[0],"pais":i[0],}, json_data)
			aux=1
		json_data.write("]")
		json_data.close()

class Controller:
	def __init__(self):
		self.model = Model()

	def get_movies_from_model(self):
		return self.model.get_movies_DB()

class View():

	def __init__(self):
		# Cargamos el Gtk.Builder y nuestra interfaz creada en Glade
		self.builder = Gtk.Builder()
		self.builder.add_from_file("sprint1.glade")

		# Conectamos las señales definidas en Glade con nuestras funciones 
		self.builder.connect_signals(self)

		# Instanciamos un controlador para acceder al modelo
		self.controller = Controller()
	
		# Centramos y cambiamos el tamaño por defecto de las ventanas de nuestra aplicación
		self.window = self.builder.get_object("window")
		
		self.window_anadir = self.builder.get_object("window_anadir")
		
		self.window.set_default_size(800,500)
		self.window.set_position(Gtk.WindowPosition.CENTER)

		self.window_anadir.set_default_size(500,250)
		self.window_anadir.set_position(Gtk.WindowPosition.CENTER)
	
		# Creamos nuestro Treeview y le asignamos el modelo
		self.create_treeview_view()
	
		# Por último, mostramos la ventana principal de nuestra aplicación
		self.window.show_all()


	# TREEVIEW
	def create_treeview_view(self):
		# Cargamos la información de nuestro modelo en el treeview
		self.db_model=self.builder.get_object("liststore1")
		self.treeview = self.builder.get_object("treeview1")
		movies_data = self.controller.get_movies_from_model()
		
		for item in movies_data:
			self.db_model.append([item['titulo'], item['genero'], item['director'], item['ano'], item['pais']])
	

	# SEÑALES DE DELETE_EVENT
	def on_window_delete_event(self, widget, event):
		Gtk.main_quit()

	def on_window_anadir_delete_event(self, window_anadir, event):
		self.window.show_all()
		window_anadir.hide()
		return True

	# SEÑALES PARA BOTONES
	def on_button3_clicked(self, widget):
		self.window_anadir.show_all()
		self.window.hide()
		return True

	def on_button4_clicked(self, widget):
		self.dlg_el=self.builder.get_object("dialog_eliminar")
		self.dlg_el.set_transient_for(self.window)
		self.dlg_el.run()
		self.dlg_el.hide()
		return True;

	def on_button1_clicked(self, widget):
		self.dlg_an=self.builder.get_object("dialog_anadir")
		self.dlg_an.set_transient_for(self.window_anadir)
		self.dlg_an.run()
		self.dlg_an.hide()
		return True

	def on_button2_clicked(self, widget):
		self.window.show_all()
		self.window_anadir.hide()
		return True

	def on_button7_clicked(self, widget):
		self.window.show_all()
		self.dlg_el.hide()
		return True	

	def on_button8_clicked(self, widget):
		self.window.show_all()
		self.dlg_el.hide()
		return True	

	def on_button5_clicked(self, widget):
		self.window.show_all()
		self.dlg_an.hide()
		return True

	def on_button6_clicked(self, widget):
		self.window_anadir.show_all()
		self.dlg_an.hide()
		return True

	
	# SEÑALES ABOUT_DIALOG
	def on_aboutdialog_activate(self, aboutdialog):
		aboutdialog.run()

	def on_aboutdialog_close(self, aboutdialog, id):
		aboutdialog.hide()
		return True


	def main(self):
		Gtk.main()

if __name__ == "__main__":
	inst = View()
	inst.main()
