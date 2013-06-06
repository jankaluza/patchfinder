patchfinder
===========

Tool to search the repositories of various distribution for patches applied to particular component.

Examples
--------

* Search for patches against logrotate

	./patchfinder logrotate

* HTML output

	./patchfinder --html logrotate

* Search for packages with different names accross various distributions

	./patchfinder apache2 archlinux=apache gentoo=www-servers/apache
