from patchfinder.plugin import Plugin
from patchfinder.patch import Patch
from collections import OrderedDict
import urllib
from lxml import etree

class OpenSUSEPlugin(Plugin):
	def __init__(self):
		self.name = "openSUSE"

	def patches(self, component):
		if component.find("/") != -1:
			component = component.split('/')[1]
		ret = {}
		print "Downloading openSUSE patches list for", component
		url = "https://build.opensuse.org/package/files?package=%s&project=openSUSE:Factory" % (component)
		f = urllib.urlopen(url)
		data = f.read()
		f.close()

		ret = {}
		ret["Unknown"] = OrderedDict()

		hrefs = etree.HTML(data).xpath("//*[contains(@href,'.patch')]")
		
		for href in hrefs:
			name = href.text
			if not name:
				continue
			url = "https://api.opensuse.org/public/source/openSUSE:Factory/%s/%s" % (component, name)
			ret["Unknown"][name] = Patch(name, url)

		return ret

