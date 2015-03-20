#!/usr/bin/env python

from bs4 import BeautifulSoup

import codecs
import dicttoxml
import glob
import json
import os

for file in glob.glob('json/*'):
   print 'Converting ' + file + ' to xml ...'

   f = codecs.open(file, 'r', encoding='utf-8')
   j = json.loads(f.read())
   f.close()

   xml = dicttoxml.dicttoxml(j, custom_root="cards", attr_type=False)
   soup = BeautifulSoup(xml)

   if not os.path.isdir('xml'):
      os.mkdir('xml')

   if not os.path.isdir('xml/' + file.split('.')[1]):
      os.mkdir('xml/' + file.split('.')[1])

   f = codecs.open('xml/' + file.split('.')[1] + '/' + '.'.join(file.split('/')[-1].split('.')[:-1]) + '.xml', 'w', encoding='utf-8')
   f.write(soup.prettify())
   f.close()

   print 'Prettifying JSON ...'

   if not os.path.isdir('json/' + file.split('.')[1]):
      os.mkdir('json/' + file.split('.')[1])

   f = codecs.open('json/' + file.split('.')[1] + '/' + file.replace('json/', "") , 'w', encoding='utf-8')
   f.write(unicode(json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '))))
   f.close()
