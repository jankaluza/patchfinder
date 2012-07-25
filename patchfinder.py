#!/usr/bin/python
import sys
from patchfinder import PatchFinder
import os
import urwid
import urllib
import tempfile

pf = PatchFinder()
patches = pf.get_patches(sys.argv[1:])

class PatchWidget(urwid.TreeWidget):
	unexpanded_icon = urwid.AttrMap(urwid.TreeWidget.unexpanded_icon,
		'dirmark')
	expanded_icon = urwid.AttrMap(urwid.TreeWidget.expanded_icon,
		'dirmark')

	def __init__(self, node, name, url = ""):
		self.name = name
		self.url = url
		self.__super.__init__(node)
		# insert an extra AttrWrap for our own use
		self._w = urwid.AttrWrap(self._w, None)
		self.flagged = False
		self.update_w()
		self.expanded = node.get_depth() < 2

	def selectable(self):
		return True

	def keypress(self, size, key):
		"""allow subclasses to intercept keystrokes"""
		if key == 'left':
			key = '-'
		key = self.__super.keypress(size, key)
		if key:
			key = self.unhandled_keys(size, key)
		return key

	def unhandled_keys(self, size, key):
		if key == 'enter' or key == ' ':
			if self.url != '':
				f = urllib.urlopen(self.url)
				data = f.read()
				f.close()

				fd, name = tempfile.mkstemp()
				print name
				f = os.fdopen(fd, "w")
				f.write(data)
				f.flush()
				os.system("less %s" % (name))
				f.close()
				os.remove(name)
				self.update_w()
		else:
			return key

	def update_w(self):
		if self.flagged:
			self._w.attr = 'flagged'
			self._w.focus_attr = 'flagged focus'
		else:
			self._w.attr = 'body'
			self._w.focus_attr = 'focus'

	def get_display_text(self):
		text = self.name
		if self.url != '':
			text += " " * (80 - len(self.name)) + self.url
		return text

  
class PatchNode(urwid.TreeNode):
	def __init__(self, patch, parent=None):
		self.patch = patch
		key = patch.name
		urwid.TreeNode.__init__(self, key, key=key, parent=parent, depth=3)

	def load_widget(self):
		return PatchWidget(self, self.patch.name, self.patch.url)


class VersionNode(urwid.ParentNode):
	def __init__(self, name, childs, parent = None):
		self._childs = childs
		self.key = name
		urwid.ParentNode.__init__(self, self.key, key=self.key, parent=parent, depth=2)

	def load_child_keys(self):
		return self._childs.keys()

	def load_child_node(self, key):
		childdata = self._childs[key]
		return PatchNode(childdata, parent=self)

	def load_widget(self):
		name = self.key
		if len(self._childs) == 0:
			name += " - no patches"
		return PatchWidget(self, name)

class DistroNode(urwid.ParentNode):
	def __init__(self, name, childs, parent = None):
		self._childs = childs
		self.key = name
		urwid.ParentNode.__init__(self, self.key, key=self.key, parent=parent, depth=1)

	def load_child_keys(self):
		return self._childs

	def load_child_node(self, key):
		return VersionNode(key, patches[self.key][key], parent=self)

	def load_widget(self):
		name = self.key
		if len(self._childs) == 0:
			name += " - no package with this name"
		return PatchWidget(self, name)

class PatchesNode(urwid.ParentNode):
	def __init__(self, name, childs):
		self._childs = childs
		self.key = name
		urwid.ParentNode.__init__(self, self.key, key=self.key, parent=None, depth=0)

	def load_child_keys(self):
		return self._childs

	def load_child_node(self, key):
		return DistroNode(key, patches[key].keys(), parent=self)

	def load_widget(self):
		return PatchWidget(self, self.key)

class PatchBrowser:
	palette = [
		('body', 'black', 'light gray'),
		('flagged', 'black', 'dark green', ('bold','underline')),
		('focus', 'light gray', 'dark blue', 'standout'),
		('flagged focus', 'yellow', 'dark cyan', 
				('bold','standout','underline')),
		('head', 'yellow', 'black', 'standout'),
		('foot', 'light gray', 'black'),
		('key', 'light cyan', 'black','underline'),
		('title', 'white', 'black', 'bold'),
		('dirmark', 'black', 'dark cyan', 'bold'),
		('flag', 'dark gray', 'light gray'),
		('error', 'dark red', 'light gray'),
		]
	
	footer_text = [
		('title', "PatchFinder"), "    ",
		('key', "UP"), ",", ('key', "DOWN"), ",",
		('key', "PAGE UP"), ",", ('key', "PAGE DOWN"),
		"  ",
		('key', "SPACE"), "  ",
		('key', "+"), ",",
		('key', "-"), "  ",
		('key', "LEFT"), "  ",
		('key', "HOME"), "  ", 
		('key', "END"), "  ",
		('key', "Q"),
		]
	
	
	def __init__(self):
		distro = PatchesNode("Patches", patches.keys())
		self.header = urwid.Text("")
		self.listbox = urwid.TreeListBox(urwid.TreeWalker(distro))
		self.listbox.offset_rows = 1
		self.footer = urwid.AttrWrap(urwid.Text(self.footer_text),
			'foot')
		self.view = urwid.Frame(
			urwid.AttrWrap(self.listbox, 'body'), 
			header=urwid.AttrWrap(self.header, 'head'), 
			footer=self.footer)

	def main(self):
		self.loop = urwid.MainLoop(self.view, self.palette,
			unhandled_input=self.unhandled_input)
		self.loop.run()
	
	def unhandled_input(self, k):
		if k in ('q','Q'):
			raise urwid.ExitMainLoop()


def main():
	PatchBrowser().main()

if __name__=="__main__": 
	main()
        
