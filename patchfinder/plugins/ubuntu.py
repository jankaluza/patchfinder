from patchfinder.plugin import Plugin
from patchfinder.patch import Patch
from collections import OrderedDict
import urllib
from lxml import etree

class UbuntuPlugin(Plugin):
	def __init__(self):
		self.name = 'Ubuntu'

	def patches(self, component):
		if component.find("/") != -1:
			component = component.split('/')[1]
		print "Downloading Ubuntu patches list"
		url = "https://patches.ubuntu.com/%s/%s/" % (component[0], component)
		f = urllib.urlopen(url)
		data = f.read()
		f.close()

		ret = {}
		ret["unknown"] = OrderedDict()

		hrefs = etree.HTML(data).xpath("//*[contains(@href,'.patch')]")
		for href in hrefs:
			name = href.attrib['href']
			ret["unknown"][name] = Patch(name, url + name)
		return ret

