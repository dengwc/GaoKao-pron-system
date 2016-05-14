# _*_ coding: utf-8 _*_
import MySQLdb

class db_mysql:

	def __init__(self):
		try:
			self.conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='cee',charset='utf8')
			self.cur = self.conn.cursor()
		except Exception,e:
			print "error occured in connecting dataabase",e

	def executeInsert(self,sql,data):
		try:
			n = self.cur.execute(sql,data)
			self.conn.commit()
			return n
		except Exception,e:
			print "error occured in inserting data", e


	def executeUpdate(self,sql):
		try:
			n = self.cur.execute(sql)
			self.conn.commit()
			return n
		except Exception,e:
			print "error occured in updating data", e


	def executeQuery(self,sql):
		try:
			n = self.cur.execute(sql)
			return self.cur
		except Exception,e:
			print "error occured in searching data", e

	def executeDelete(self,sql):
		try:
			n = self.cur.execute(sql)
			return n
		except Exception,e:
			print "error occured in deleting data", e

	def close(self):
		try:
			self.cur.close()
			self.conn.close()
		except Exception,e:
			print "error occured in closing connecion",e

