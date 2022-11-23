#!/usr/bin/python

import pywikibot
import sqlite3

def open_db(name):
    print ('Connecting to',name)
    conn = sqlite3.connect(name)
    conn.row_factory = sqlite3.Row
    return conn

conn_inwoners = open_db('NederlandInwoners.db')
cinw = conn_inwoners.cursor()
sql = 'DROP TABLE `gwb_codes`'
res = cinw.execute(sql)
sql = 'CREATE TABLE "gwb_codes" (`gwb-code` TEXT, `regio` TEXT, `inwoners`, `bag`, `voorgekomen` INTEGER )'
res = cinw.execute(sql)
sql = 'INSERT INTO gwb_codes SELECT gwb_code_8, regio, a_inw, "", 0 FROM `kwb-2021`'
res = cinw.execute(sql)

## Controleer aanwezigheid niet-ingedeelde gwb_code_8
cinw2 = conn_inwoners.cursor()
cinw3 = conn_inwoners.cursor()
sql = 'SELECT DISTINCT(`bag`) FROM `WoonplaatsenMetBag`'
sql2 = 'SELECT `gwb_code` FROM `bag_regio` WHERE `bag` = ?'    
sql3 = 'UPDATE `gwb_codes` SET `bag` = ?,  `voorgekomen` = `voorgekomen` + 1 WHERE `gwb-code` LIKE ?'
    
res1 = cinw.execute(sql)
for row in res1.fetchall():
  bag = row[0] 
  query2 = [bag,]
  res2 = cinw2.execute( sql2, query2 )
  for row2 in res2.fetchall():
    codes = row2[0].split(",")
    for code in codes:
      query3 = [bag, code + '%',]
      res3 = cinw3.execute( sql3, query3 )

sql = 'SELECT `gwb-code` FROM `gwb_codes` WHERE `voorgekomen` = 0 AND LENGTH(`gwb-code`) < 8 ORDER BY `gwb-code` DESC'
sql2 = 'SELECT COUNT(`gwb-code`) AS `Aantal`, SUM(`voorgekomen`) AS voorgekomen FROM `gwb_codes` WHERE `gwb-code` LIKE ? AND LENGTH(`gwb-code`)> ?'
sql3 = 'UPDATE `gwb_codes` SET `voorgekomen`=? WHERE `gwb-code` = ?'
res1 = cinw.execute(sql)
for row in res1.fetchall():
  gwbcode = row[0]
  query2 = [gwbcode + "%", len(gwbcode),]
  res2 = cinw2.execute( sql2, query2 )
  for row2 in res2.fetchall():
    if row2[0] == row2[1]:
      query3 = [1, gwbcode,]
      res3 = cinw3.execute( sql3, query3 )
    
conn_inwoners.commit()
