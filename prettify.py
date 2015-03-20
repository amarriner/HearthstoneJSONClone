#!/usr/bin/env python

from bs4 import BeautifulSoup

import codecs
import dicttoxml
import glob
import json
import os
import sys

# Loop through each available language in the input directory and create
# an 'All' file containing all of the sets for the given langauge
def do_languages():
   for language in glob.glob('input/Basic*'):
      language = language.split('.')[1]

      print 'Creating All JSON for ' + language

      j = {}

      # Loop through each file for the given language and add it to the transient 
      # JSON object
      for file in glob.glob('input/*.' + language + '.json'):
         f = codecs.open(file, 'r', encoding='utf-8')
         cards = json.loads(f.read())
         f.close()

         j[file.replace('input/', "").split('.')[0]] = cards

      # Write the JSON file to disk
      f = codecs.open('input/All.' + language + '.json', 'w', encoding='utf-8')
      f.write(unicode(json.dumps(j), 'utf-8'))
      f.close()
      
# Loop through all the JSON files in the input directory for processing
def do_prettify():
   for file in glob.glob('input/*'):

      # Convert to XML
      print 'Converting ' + file + ' to xml ...'

      f = codecs.open(file, 'r', encoding='utf-8')
      j = json.loads(f.read())
      f.close()

      # Prettify the XML
      xml = dicttoxml.dicttoxml(j, custom_root="cards", attr_type=False)
      soup = BeautifulSoup(xml)

      # Create directories if they're not there
      if not os.path.isdir('xml'):
         os.mkdir('xml')

      if not os.path.isdir('xml/' + file.split('.')[1]):
         os.mkdir('xml/' + file.split('.')[1])

      # Write the XML file to disk
      f = codecs.open('xml/' + file.split('.')[1] + '/' + '.'.join(file.split('/')[-1].split('.')[:-1]) + '.xml', 'w', encoding='utf-8')
      f.write(soup.prettify())
      f.close()

      # Process the JSON file itself 
      print 'Prettifying JSON ...'

      # Create directories if necessary
      if not os.path.isdir('json/' + file.split('.')[1]):
         os.mkdir('json/' + file.split('.')[1])

      # Write file to disk
      f = codecs.open('json/' + file.split('.')[1] + '/' + file.replace('input/', "") , 'w', encoding='utf-8')
      f.write(unicode(json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '))))
      f.close()

# Initial entry point
def main():
   do_languages()
   do_prettify()


if __name__ == "__main__":
   sys.exit(main())
