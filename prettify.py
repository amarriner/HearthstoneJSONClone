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

      # Delete file if it already exists
      if os.path.isfile('input/All.' + language + '.json'):
         os.remove('input/All.' + language + '.json')

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

      f = codecs.open(file, 'r', encoding='utf-8')
      j = json.loads(f.read())
      f.close()

      do_xml(j, file)
      do_csv(j, file)

      # Process the JSON file itself 
      print 'Prettifying JSON ...'

      # Create directories if necessary
      if not os.path.isdir('json/' + file.split('.')[1]):
         os.mkdir('json/' + file.split('.')[1])

      # Write file to disk
      f = codecs.open('json/' + file.split('.')[1] + '/' + file.replace('input/', "") , 'w', encoding='utf-8')
      f.write(unicode(json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '))))
      f.close()


# Convert file to XML
def do_xml(j, file):
   print 'Converting ' + file + ' to xml ...'

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


# Convert file to CSV
def do_csv(j, file):
   print 'Converting ' + file + ' to csv ...'

   headers = ""
   csv = ""
   
   if isinstance(j, dict):
      l = []

      for key in j.keys():
         l += j[key]

      data = get_csv(l)
      headers = data['headers']
      csv += data['rows']
   else:
      data = get_csv(j)
      headers = data['headers']
      csv += data['rows']

   # Create directories if they're not there
   if not os.path.isdir('csv'):
      os.mkdir('csv')
   
   if not os.path.isdir('csv/' + file.split('.')[1]):
      os.mkdir('csv/' + file.split('.')[1])
   
   # Write the XML file to disk   
   f = codecs.open('csv/' + file.split('.')[1] + '/' + '.'.join(file.split('/')[-1].split('.')[:-1]) + '.csv', 'w', encoding='utf-8')
   f.write(','.join(headers) + "\n" + csv + "\n")
   f.close()


# Convert inner JSON to CSV
def get_csv(j):

   headers = []
   rows = []

   # Find all available headers
   for card in j:
      for key in card.keys():
         if key.upper() not in headers:
            headers.append(key.upper())

   # Parse into rows
   for card in j:
      data = [""] * len(headers) 

      # For each card, find the correct column to put the data in
      for key in card.keys():
         index = headers.index(key.upper())

         # Then apply the data to the column in different ways depending on type
         if isinstance(card[key], list):
            data[index] = '|'.join(card[key])
         elif isinstance(card[key], int):
            data[index] = str(card[key])
         else:
            data[index] = card[key].replace(',', '').replace("'", "&sbquo;").replace('"', '&bdquo;')

      rows.append(','.join(data))

   return {'headers': headers, 'rows': '\n'.join(rows)}


# Initial entry point
def main():
   do_languages()
   do_prettify()


if __name__ == "__main__":
   sys.exit(main())
