#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Wojciech 'KosciaK' Pietrzok
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ----------------------------------------------------------------------
#
# Icons used:
# famfamfam's "Silk" icon set - http://www.famfamfam.com/lab/icons/silk/
#

__author__ = "...."
__version__ = "...."

import sys
import os
import time
import locale
import urllib
import json,mimetypes,codecs
from optparse import OptionParser

def quote_sharp(s):
  return urllib.quote(s).replace('#','%23')

reload(sys)
sys.setdefaultencoding("utf-8")

locale.setlocale(locale.LC_ALL, '')
LANG, ENCODING = locale.getlocale()

DATE_FORMAT = '%Y-%m-%d&nbsp;%H:%M:%S'

TABLE_HEADERS = {'en_GB': ('Name', 'Size', 'Last Modified'),
				 'pl_PL': ('Nazwa', 'Rozmiar', 'Czas modyfikacji')}

SCRIPT_WWW = 'http://code.google.com/p/kosciak-misc/wiki/DropboxIndex'

FILES_URL = 'http://dl.dropboxusercontent.com/u/73985358'

JSON_STYLE=dict(encoding='utf-8',indent=4)
#JSON_STYLE=dict(indent=4)

ICONS = (
	'%s/icons/back.png' % FILES_URL,
	'%s/icons/folder.png' % FILES_URL,
	'%s/icons/file.png' % FILES_URL,
	'%s/icons/image.png' % FILES_URL,
	'%s/icons/video.png' % FILES_URL,
	'%s/icons/music.png' % FILES_URL,
	'%s/icons/archive.png' % FILES_URL,
	'%s/icons/package.png' % FILES_URL,
	'%s/icons/pdf.png' % FILES_URL,
	'%s/icons/txt.png' % FILES_URL,
	'%s/icons/markup.png' % FILES_URL,
	'%s/icons/code.png' % FILES_URL,
	'%s/icons/font.png' % FILES_URL,
	'%s/icons/document.png' % FILES_URL,
	'%s/icons/spreadsheet.png' % FILES_URL,
	'%s/icons/presentation.png' % FILES_URL,
	'%s/icons/application.png' % FILES_URL,
	'%s/icons/plugin.png' % FILES_URL,
	'%s/icons/iso.png' % FILES_URL,
	)

FILE_TYPES = {
	('gif', 'jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff', 'raw', 'img', 'ico', ): 'image',
	('avi', 'ram', 'mpg', 'mpeg', 'mov', 'asf', 'wmv', 'asx', 'ogm', 'vob', '3gp', ): 'video',
	('mp3', 'ogg', 'mpc', 'wav', 'wave', 'flac', 'shn', 'ape', 'mid', 'midi', 'wma', 'rm', 'aac', 'mka', ): 'music',
	('tar', 'bz2', 'gz', 'arj', 'rar', 'zip', '7z', ): 'archive',
	('deb', 'rpm', 'pkg', 'jar', 'war', 'ear', ): 'package',
	('pdf', ): 'pdf',
	('txt', ): 'txt',
	('html', 'htm', 'xml', 'css', 'rss', 'yaml', 'php', 'php3', 'php4', 'php5', ): 'markup',
	('js', 'py', 'pl', 'java', 'c', 'h', 'cpp', 'hpp', 'sql', 'gcode'): 'code',
	('ttf', 'otf', 'fnt', ): 'font',
	('doc', 'rtf', 'odt', 'abw', 'docx', 'sxw', ): 'document',
	('xls', 'ods', 'csv', 'sdc', 'xlsx', ): 'spreadsheet',
	('ppt', 'odp', 'pptx', ): 'presentation',
	('exe', 'msi', 'bin', 'dmg', ): 'application',
	('xpi', ): 'plugin',
	('iso', 'nrg', ): 'iso',
	}

HTML_STYLE = '''
	<style>
		body { font-family: Verdana, sans-serif; font-size: 12px;}
		a { text-decoration: none; color: #00A; }
		a:hover { text-decoration: underline; }
		#dropbox-index-header { padding: 0; margin: 0.5em auto 0.5em 1em; }
		table#dropbox-index-list { text-align: center; border-collapse: collapse; }
		#dropbox-index-list thead { border-bottom: 1px solid #555; }
		#dropbox-index-list th:hover { cursor: pointer; cursor: hand; background-color: #EEE; }
		#direction { border: 0; vertical-align: bottom; margin: 0 0.5em;}
		#dropbox-index-list tbody { border-bottom: 1px solid #555;}
		#dropbox-index-list tr, th { line-height: 1.7em; min-height: 25px; }
		#dropbox-index-list tbody tr:hover { background-color: #EEE; }
		.name { text-align: left; width: 35em; }
		.name a, thead .name { padding-left: 22px; }
		.name a { display: block; }
		.size { text-align: right; width: 7em; padding-right: 1em;}
		.date { text-align: right; width: 15em; padding-right: 1em;}
		.thname { text-align: left; width: 35em; }
		.thsize { text-align: right; width: 7em; padding-right: 1em;}
		.thdate { text-align: right; width: 15em; padding-right: 1em;}
		#dropbox-index-dir-info { margin: 1em auto 0.5em 2em; }
		#dropbox-index-footer { margin: 1em auto 0.5em 2em; font-size: smaller;}
		/* Icons */
		.dir, .back, .file { background-repeat: no-repeat; background-position: 2px 4px;}
		.back { background-image: url('%s'); }
		.dir { background-image: url('%s'); }
		.file { background-image: url('%s'); }
		.image { background-image: url('%s'); }
		.video { background-image: url('%s'); }
		.music { background-image: url('%s'); }
		.archive { background-image: url('%s'); }
		.package { background-image: url('%s'); }
		.pdf { background-image: url('%s'); }
		.txt { background-image: url('%s'); }
		.markup { background-image: url('%s'); }
		.code { background-image: url('%s'); }
		.font { background-image: url('%s'); }
		.document { background-image: url('%s'); }
		.spreadsheet { background-image: url('%s'); }
		.presentation { background-image: url('%s'); }
		.application { background-image: url('%s'); }
		.plugin { background-image: url('%s'); }
		.iso { background-image: url('%s'); }
	</style>''' % ICONS

#
HTML_JAVASCRIPT = '''
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
	<script>
	function sort() {
		column = $(this).attr("class").split(' ')[0];
		$("b").remove();
		if ($(this).hasClass("desc")) {
			$("#dropbox-index-list thead tr th").each(function(i) { $(this).removeClass("asc").removeClass("desc") });
			$(this).addClass("asc");
			reverse = -1;
		} else {
			$("#dropbox-index-list thead tr th").each(function(i) { $(this).removeClass("asc").removeClass("desc") });
			$(this).addClass("desc");
			reverse = 1;
		}
		if (column == "thname") {
			$(this).append('<b id="direction">'+((reverse == 1) ? '\xe2\x96\xbc' : '\xe2\x96\xb2')+'</b>');
		} else {
			$(this).prepend('<b id="direction">'+((reverse == 1) ? '\xe2\x96\xbc' : '\xe2\x96\xb2')+'</b>');
		}
		rows = $("#dropbox-index-list tbody tr").detach()
		rows.sort(function(a, b) {
			result = $(a).data('type') - $(b).data('type')
			if (result != 0) { return result }

			return (($(a).data(column) < $(b).data(column)) - ($(a).data(column) > $(b).data(column))) * reverse

		});
		$("#dropbox-index-list tbody").append(rows);
	}

	function prepare() {
		$("#dropbox-index-list tbody tr").each(function(i) {
			if ($(this).children(".name").hasClass("back")) {
				$(this).data('type', 1);
			} else if ($(this).children(".name").hasClass("dir")) {
				$(this).data('type', 2);
			} else {
				$(this).data('type', 3);
			}
			$(this).data('thname', $(this).children(".name").text().toLowerCase());
			$(this).data('thsize', parseInt($(this).children(".size").attr("sort")));
			$(this).data('thdate', parseInt($(this).children(".date").attr("sort")));
		});

		$("#dropbox-index-list thead tr th").each(function(i) {
			$(this).bind('click', sort);
		});
	}

	$(document).ready(function(){
		prepare();
	});
</script>''' #% (FILES_URL)#, FILES_URL)

FAVICON = '<link rel="shortcut icon" href="%s/icons/favicon.png"/>' % FILES_URL

HTML_START = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset="%(ENCODING)s"/>
	<title>%(PATH)s</title>
	%(FAVICON)s
	%(HTML_STYLE)s
	%(HTML_JAVASCRIPT)s
</head>
<body>
'''
HTML_HEADER = '<h1 id="dropbox-index-header">%s</h1>'
HTML_TABLE_START = '''
<table id="dropbox-index-list">
	<thead>
		<tr>
			<th class="thname">%s</th><th class="thsize">%s</th><th class="thdate">%s</th>
		</tr>
	</thead>
	<tbody>
'''
#HTML_BACK = '<tr><td class="name back"><a href="../index.html">..</a></td><td class="size">&nbsp;</td><td class="date">&nbsp;</td></tr>'
HTML_DIR = '<tr><td class="name dir"><a href="%(URI_name)s/index.html">%(file_name)s</a></td><td class="size" sort="%(file_size_sort)s">%(file_size)s</td><td class="date" sort="%(file_time_sort)s">%(file_time)s</td></tr>\n'
HTML_FILE = '<tr><td class="name file%(file_type)s"><a title=\'%(title)s\' href="%(URI_name)s" >%(file_name)s</a></td><td class="size" sort="%(file_size_sort)s">%(file_size)s</td><td class="date" sort="%(file_time_sort)s">%(file_time)s</td></tr>\n'
HTML_TABLE_END = '''
	</tbody>
</table>
<div id="dropbox-index-footer">Generated on <strong>%s</strong> using <a href="%s">Dropbox-index</a>-%s</a></div>'''
HTML_DIR_INFO = '''
<div id="dropbox-index-dir-info">
%(DIR_INFO)s
</div>'''
HTML_END = '''
</body>
</html>'''

def colorize(s,color):
	#color=0,1,4,5,7,30~37,40~47
	return "\x1B[1;{}m{}\x1B[0m".format(color,s)


def table_headers():
	if LANG in TABLE_HEADERS:
		return TABLE_HEADERS[LANG]
	else:
		return TABLE_HEADERS['en_GB']


def get_size(file):
	size = os.path.getsize(file)

	if size < 1000:
		return '%s bytes' % size

	kilo = size / 1024
	if kilo < 1000:
		return '%s KB' % round(float(size) / 1024, 1)

	mega = kilo / 1024
	return '%s MB' % round(float(kilo) / 1024, 1)

def get_filetype(file_name,file):

	global global_back_now
	filetype = file_name.split('.')[-1].lower()
	for keys, value in FILE_TYPES.items():
		URI_name = quote_sharp(file_name)
		if filetype in keys:
			try:
				if value in ['txt', 'code']:
					global_back_now='<div class="gb"><p>'+codecs.open(file, 'r', encoding='utf-8').read(256).replace('\n','</p><p>')+'</p></div>'

				if value=='markup':
					global_back_now='<iframe class="gb" src="'+URI_name+'"> </iframe>'

				if value=='image' :
					global_back_now='<img class="gb" src='+URI_name+'> </img>'
			except BaseException, e:
				global_back_now=''
			




			return ' %s' % value

	return ''


def html_render(path,fullpath, back, dirs, files, template_file=None,jList=None):
	global PATH,FULLPATH
	PATH = os.path.basename(os.path.realpath(path))

	FULLPATH = '<a href="'+''.join(['../']*(len(fullpath)-1))+'./index.html">Home</a>'
	for i,dir in enumerate(fullpath[1:]):
					FULLPATH+=' > <a href="'+''.join(['../']*(len(fullpath)-i-2))+'./index.html">'+dir+'</a>'

	print(colorize(fullpath,34))

	index = codecs.open(os.path.join(path, 'index.html'), 'w',encoding='utf-8')

	if template_file:
		template = open(template_file, 'r').read()
		head_start = template.find('<head>') + 6
		table_start = template.find('%(FILES)s')
		other_start = template.find('%(DIR_INFO)s')
		index.write(template[0:head_start] % globals())
		index.write(HTML_STYLE + HTML_JAVASCRIPT)
		index.write(template[head_start:table_start] % globals())
	else:
		index.write(HTML_START % globals())
		index.write(HTML_HEADER % PATH)

	index.write(HTML_TABLE_START % table_headers())

	#if back:
	#	index.write(HTML_BACK)

	for file in dirs:
		file_name = os.path.basename(file)
		URI_name = quote_sharp(file_name)
		file_size = len(os.listdir(file))
		file_size_sort = file_size
		file_time = time.strftime(DATE_FORMAT, time.localtime(os.path.getmtime(file)))
		file_time_sort = os.path.getmtime(file)
		index.write(HTML_DIR % locals())

	dir_info = None
	global global_back, global_back_now
	global_back=None
	latest=0
	for i,file in enumerate(files):
		file_name = os.path.basename(file)
		if 'dir-info' in file_name:
			dir_info = open(file, 'r').read().replace('\n','<br>')
			continue

		global_back_now=None
		file_type = get_filetype(file_name,file)
		file_size = get_size(file)
		file_size_sort = os.path.getsize(file)
		file_time = time.strftime(DATE_FORMAT, time.localtime(os.path.getmtime(file)))
		file_time_sort = os.path.getmtime(file)

		if (file_time_sort> latest)and(global_back_now):
			latest= file_time_sort
			global_back=global_back_now

		if jList:
			title=jList[i]['info'].decode('utf-8')#.decode('ascii')
		else:
			title=''
		URI_name = quote_sharp(file_name)
		try:
			index.write(HTML_FILE % locals())
		except UnicodeDecodeError, e:
			print(colorize( file+ repr(e), 31)+'\n')

	now = time.strftime(DATE_FORMAT, time.localtime())
	index.write(HTML_TABLE_END % (now, SCRIPT_WWW, __version__))

	if template_file:
		global DIR_INFO, GLOBAL_BACK
		DIR_INFO = dir_info or ''
		GLOBAL_BACK = global_back or '<div class="gb"><div style="margin: 40px;padding: 0;text-align: center"><img src="%s/icons/psychobox.png" /></div></div>' % FILES_URL
		#print(GLOBAL_BACK)

		index.write(template[table_start+9:other_start])
		index.write(GLOBAL_BACK)
		index.write(template[other_start:] % globals())
		DIR_INFO = None
	else:
		index.write(HTML_DIR_INFO % {'DIR_INFO': dir_info or ''})
		index.write(HTML_END)

def genList(files,json_mode):
	r=[]
	anyMod = False
	if files!=[]:

		if json_mode=='i':
			if os.path.exists(os.path.dirname(files[0]) + '/fileList.json'):
				f = codecs.open(os.path.dirname(files[0]) + '/fileList.json','r',encoding='utf-8')
				#f = open(os.path.dirname(files[0]) + '/fileList.json','r')
				#print os.path.dirname(files[0]) + '/fileList.json'
				lastInfo=json.loads(f.read())
			else:
				lastInfo=[]
				anyMod = True
		for file in files:
			try:
				file.encode('utf-8')
			except UnicodeDecodeError, e:
				print(colorize( file+ repr(e), 31)+'\n')
			else:
				item={'path' :os.path.basename(file)}
				ext=os.path.splitext(file)[1]
				item['mime']=mimetypes.types_map[ext] if mimetypes.types_map.has_key(ext) else '*/*'
				#print(file)
				if (json_mode=='s') or (json_mode=='i'):
					st=os.stat(file)
					item['st_size']=st.st_size
					item['st_ctime']=int(st.st_ctime)
					item['st_mtime']=int(st.st_mtime)
					#item['stat']=dict(os.stat(file))
				if json_mode=='i':
					modified=True
					ufn=os.path.basename(file).encode('utf-8')
					for i in lastInfo:
						if (i['path']==ufn) and i.has_key('st_mtime') and i.has_key('info') and (i['st_mtime']==item['st_mtime']):
							modified=False
							break
					if modified:
						anyMod = True
						print(colorize('{} modified'.format(file),33))
						item['info']=os.popen('file -bLn "'+file+'"').read().rstrip()
					else:
						item['info']=i['info']
				r.append(item)
	return anyMod, r

def crawl(path, fullpath,back=None, recursive=False, template_file=None, json_mode='n'):
	if not os.path.exists(path):
		print colorize('ERROR: Path %s does not exists' % path,31)
		return

	if not os.path.isdir(path):
		print colorize('ERROR: Path %s is not a directory' % path,31)
		return

	# get contents of the directory
	contents = [os.path.join(path, file) for file in os.listdir(path) if not ( (file.endswith('index.html')) or (file.endswith('fileList.json')) or (file.endswith('fileList_sub.json')) ) ]
	# remove hidden files
	# TODO: identify Windows hidden files
	contents = [file for file in contents if not os.path.basename(file).startswith('.')]

	# get only files
	files = [file for file in contents if os.path.isfile(file)]
	files.sort(key=str.lower)

	# get only directories
	if recursive:
		dirs = [file for file in contents if os.path.isdir(file)]
		dirs.sort(key=str.lower)
	else:
		dirs = [];

	if json_mode!='n':
		mod, jList=genList(files,json_mode);
		if mod:
			fj=codecs.open(path+'/fileList.json','w', encoding='utf-8')
			#fj=open(path+'/fileList.json','w')
			#print json.dumps(jList, encoding="utf-8")
			fj.write(json.dumps(jList,**JSON_STYLE))
			#json.dump(jList, fj, **JSON_STYLE)
			fj.close()

			html_render(path,fullpath, back, dirs, files, template_file,jList)
			print colorize('Created index.html for %s' % os.path.realpath(path),34)
		elif not(os.path.exists(path+'/index.html')):
			html_render(path,fullpath, back, dirs, files, template_file,jList)
			print colorize('Created index.html for %s' % os.path.realpath(path),34)

		for dir in dirs:
			subList=crawl(dir,fullpath+[dir.split('/')[-1]], path, recursive, template_file,json_mode)
			for item in subList:
				item.update({'path':dir.split('/')[-1]+'/'+item['path']})
				jList.append(item)

		#fj=codecs.open(path+'/fileList.json','w', encoding='utf-8')
		fj=open(path+'/fileList_sub.json','w')
		fj.write(json.dumps(jList,**JSON_STYLE))
		fj.close()
		if mod: 
			print(colorize('fileList.json created for {}'.format(path),34))
		return jList
	else:
		html_render(path,fullpath, back, dirs, files, template_file)
		print colorize('Created index.html for %s' % os.path.realpath(path),34)
		for dir in dirs:
			crawl(dir,fullpath+[dir.split('/')[-1]], path, recursive, template_file,json_mode)




def run():

	epilog = '''ATTENTION:
Script will overwrite any existing index.html file(s)!
	'''

	parser = OptionParser(version='%prog ' + __version__,
						  usage="%prog [options] DIRECTORY",
						  epilog=epilog)
	parser.add_option('-R', '--recursive',
					  action='store_true', default=False,
					  help='Include subdirectories [default: %default]')
	parser.add_option('-J', '--json', default='n',
					  help='generate json file list for quick acess, n for none, s for stat only, i for file info')
	parser.add_option('-T', '--template',
					  help='Use HTML file as template')

	options, args = parser.parse_args()
	if not args:
		parser.print_help()
		sys.exit()

	crawl(path=args[0], fullpath=['Home'],
		  recursive=options.recursive,
		  template_file=options.template,
		json_mode=options.json)

if __name__ == '__main__':
	mimetypes.init()
	run()

