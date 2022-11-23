#!/usr/bin/python

import pywikibot
import sqlite3
#import re
import sys

arg1 = ''
if len(sys.argv) > 1:
  arg1 = sys.argv[1]

def open_db(name):
  print ('Connecting to',name)
  conn = sqlite3.connect(name)
  conn.row_factory = sqlite3.Row
  return conn

conn_inwoners = open_db('NederlandInwoners.db')
cinw = conn_inwoners.cursor()
cinw2 = conn_inwoners.cursor()

# INSERT INTO bag_regio 
# SELECT bag, SUBSTR(GMCode,3) || '9999' FROM WoonplaatsenMetBag AS WB, WoonplaatsenNederland2022 AS WN 
#  WHERE WB.bag NOT IN (SELECT bag from bag_regio) 
#  AND WB.bag = SUBSTR(WN.WPCode,3)

sql = 'SELECT `wmb`.`plaatsLabel`, `wmb`.bag, `bag`.`gwb_code` as `code` FROM `WoonplaatsenMetBag` AS `wmb`, `bag_regio` as `bag` WHERE `bag`.`gwb_code` LIKE ? AND `bag`.`bag` = `wmb`.`bag` ORDER BY `wmb`.`plaatsLabel`'
sql2 = 'SELECT `a_inw` FROM `kwb-2021` WHERE `gwb_code_8` = ?'    
sql3 = 'SELECT `a_inw`, `regio` FROM `kwb-2021` WHERE `gwb_code_8` = ?'
  
f = open(f'D://Wikipedia//inwoners_{arg1}.txt', "w")
f.write( 'Gegevens ontleend aan:\n')
f.write( '# Kerncijfers wijken en buurten 2021 (CBS)\n')
f.write( '# BAG-CBS-tabel woonplaatsen en Gemeentecodes (CBS)\n')
f.write( '# Arraysjabloon bagcodes\n')
f.write( '\n')


def verwerkgemeente(arg1):
  totinwoners = totplaatsen = 0
  query3 = [arg1,]
  res3 = cinw.execute(sql3, query3)
  for row in res3.fetchall():
    gemnaam = row[1]
    geminwoners = int(row[0])
    
  f.write( f'== {gemnaam} ==\n' )
  f.write( '{| class="wikitable"\n' )
  f.write( '! Plaatsnaam !! Inwoners !! Datum !! Codes\n' )
      
  query1 = [arg1 + "%", ]
  res1 = cinw.execute(sql, query1)
  for row in res1.fetchall():
    codes = row[2].split(",")
    inwoners = 0
    gevondenvermelding = False
  #  print (gemnaam, codes)
    for code in codes:
      query2 = [code,]
      res2 = cinw2.execute( sql2, query2 )
      for row2 in res2.fetchall():
        gevondenvermelding = True
        inwoners = inwoners + int(row2[0]) 
    f.write(f"|-\n")
    if gevondenvermelding:
      f.write(f"| {row[0]} || {inwoners} || 2021 || {codes}\n")
      totinwoners += inwoners
    else:
      f.write(f"| {row[0]} || Geen buurt gekoppeld aan {row[1]} || - || {codes}\n")
    totplaatsen += 1
    
  if geminwoners - totinwoners !=0: 
    f.write(f"|-\n")
    if abs(geminwoners - totinwoners) < 2*totplaatsen:
      f.write(f"| Afrondingsverschil ({totplaatsen}) || {geminwoners - totinwoners} || 2021 ||\n")
    else:
      if abs(geminwoners - totinwoners) < 100:
        f.write(f"| Overig ({totplaatsen}) || {geminwoners - totinwoners} || 2021 ||\n")
      else:
        f.write(f"| '''Overig''' ({totplaatsen}) || {geminwoners - totinwoners} || 2021||\n")
  f.write(f"|-\n")
  f.write(f"| Totaal {gemnaam} || {geminwoners} || 2021 || {arg1}\n")
  f.write("|}\n")
  f.write("\n")
  
if arg1 == '':
  sqlg = "SELECT `gwb_code_8` FROM `kwb-2021` WHERE `recs`= 'Gemeente' ORDER BY `regio`"
  cgem = conn_inwoners.cursor()
  resg = cgem.execute(sqlg)
  for row in resg.fetchall():
    verwerkgemeente(row[0])   
else:
  verwerkgemeente(arg1)

f.close()

