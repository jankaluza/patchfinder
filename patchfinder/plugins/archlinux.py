from patchfinder.plugin import Plugin
from patchfinder.patch import Patch
from collections import OrderedDict
import urllib
from lxml import etree

class ArchLinuxPlugin(Plugin):
	def __init__(self):
		self.name = "ArchLinux"

	def patches(self, component):
		if component.find("/") != -1:
			component = component.split('/')[1]
		ret = {}
		print "Downloading Arch Linux version info"
		url = "http://www.archlinux.org/packages/?sort=&arch=i686&q=%s&maintainer=&last_update=&flagged=&limit=200" % (component)
		f = urllib.urlopen(url)
		data = f.read()
		f.close()


		hrefs = etree.HTML(data).xpath("//*[contains(@href,'/%s/')]" % (component))
		if len(hrefs) == 0:
			return {}
		category = hrefs[0].attrib['href']
		url = "http://www.archlinux.org/%s" % (category)
		f = urllib.urlopen(url)
		data = f.read()
		f.close()

		hrefs = etree.HTML(data).xpath("//*[contains(@title,'View source files for')]")
		if len(hrefs) == 0:
			return {}

		version = 'Unknown'
		h2s = etree.HTML(data).xpath("//h2")
		for h2 in h2s:
			if h2.text.find(component) != -1:
				version = h2.text
		ret = {}
		ret[version] = OrderedDict()

		print "Downloading Arch Linux patches list"
		url = hrefs[0].attrib['href']
		f = urllib.urlopen(url)
		data = f.read()
		f.close()

		hrefs = etree.HTML(data).xpath("//*[contains(@href,'.patch')]")
		if len(hrefs) == 0:
			return {}
		
		url = ''
		name = ''
		for href in hrefs:
			if not href.text or href.text in ["log", "stats"]:
				continue

			if href.text == 'plain':
				url = "https://projects.archlinux.org/" + href.attrib['href']
				ret[version][name] = Patch(name, url)
			else:
				name = href.text

		return ret

