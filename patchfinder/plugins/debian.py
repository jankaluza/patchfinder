from patchfinder.plugin import Plugin
from patchfinder.patch import Patch
from collections import OrderedDict
import urllib
from lxml import etree
import sys

class DebianPlugin(Plugin):
	def __init__(self):
		self.name = "Debian"

	def patches(self, component):
		if component.find("/") != -1:
			component = component.split('/')[1]
		ret = {}
		print >> sys.stderr, "Downloading Debian version list"
		url = "http://patch-tracker.debian.org/package/%s" % (component)
		f = urllib.urlopen(url)
		data = f.read()
		f.close()

		hrefs = etree.HTML(data).xpath("//*[contains(@href,'%s')]" % (url))

		if len(hrefs) > 4:
			return {}

		for href in hrefs:
			url = href.attrib['href']
			version = url.split('/')[-1]
			if not ret.has_key(version):
				ret[version] = OrderedDict()

			print >> sys.stderr, "Downloading patches list for version", version
			f = urllib.urlopen(url)
			data = f.read()
			f.close()

			indexes = {}
			table = etree.HTML(data).xpath("//*[contains(@class,'patchlisting')]")
			if len(table) == 0:
				del ret[version]
				ret[version + " - error parsing data fetched from " + url] = OrderedDict()
				print >> sys.stderr, "Error parsing data fetched from", url
				continue
			elif len(table) == 1:
				continue
			elif len(table) == 2:
				table = table[1]
			for tr in table:
				i = 0
				name = ""
				url = ""
				for td in tr:
					if len(indexes) != 4:
						indexes[td.text] = i
					elif not indexes.has_key("patch"):
						continue
					elif indexes['patch'] == i:
						name = td.text
					elif indexes['raw'] == i:
						url = td[0].attrib['href']
					i += 1
				if name != '':
					ret[version][name] = Patch(name, url)

		return ret

