import os
import sys
from plugin import Plugin

from straight.plugin.loaders import ClassLoader

class PatchFinder(object):
	def __init__(self):
		self.plugins = ClassLoader().load("patchfinder.plugins")

	def get_patches(self, components):
		default = ""
		parsed = {}
		for component in components:
			if component.find("=") != -1:
				parsed[component.split('=')[0].lower()] = component.split('=')[1]
			else:
				default = component
		ret = {}
		for plugin in self.plugins:
			if not issubclass(plugin, Plugin):
				continue
			p = plugin()
			if p.name == "":
				continue
			component = default
			if parsed.has_key(p.name.lower()):
				component = parsed[p.name.lower()]
			ret[p.name] = p.patches(component)

		return ret

