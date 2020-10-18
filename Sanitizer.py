import json
import re

#types: i - integer, f - float, s - str, n - number, a - array, st - structure 

class Sanitizer():
	__data = ""
	__errors = []
	__methods = {}

	def __init__(self, data):
		self.__data = data.copy()
		self.__methods = {'i':self.__is_int, 'f':self.__is_float, 's':self.__is_string, 
						'n':self.__is_number, 'a':self.__is_array, 'st':self.__is_structure}

	def get_err(self):
		return self.__errors

	def clear_err(self):
		self.__errors = []

	def validate(self, types):
		try:
			res = dict()
			keys = list(self.__data.keys())

			if len(keys) != len(types):
				self.__errors.append("wrong number of types")
				return dict()

			for i, t in enumerate(types):
				name = keys[i]
				data = self.__data[name]

				if t in self.__methods.keys():
					temp = self.__methods[t](name, data)
				else:
					self.__errors.append("undefined data type")
					res.update([(name, None)])
					continue

				if not (isinstance(temp, tuple) and len(temp) == 2 and isinstance(temp[0], bool)):
					self.__errors.append("the function returns invalid data format")
					res.update([(name, None)])
					continue

				if temp[0]:
					res.update([(name, temp[1])])
				else:
					res.update([(name, None)])

			return res

		except Exception as e:
			self.__errors.append(e)
			return dict()

	def add_type(self, name, func):
		self.__methods.update([(name, func)]) #name - type name; func(name, data) - type checking function, must return a pair (bool, data);

	def __is_int(self, name, data): 
		try:
			return (True, int(data))
		except Exception:
			self.__errors.append("'%s' not integer" % (name,))
			return (False, None)

	def __is_float(self, name, data): 
		try:
			return (True, float(data))
		except Exception:
			self.__errors.append("'%s' not float" % (name,))
			return (False, None)		

	def __is_string(self, name, data): 
		try:
			if isinstance(data, str):
				return (True, str(data))
			else:
				self.__errors.append("'%s' not string" % (name,))
				return (False, None)
		except Exception:
			self.__errors.append("'%s' not string" % (name,))
			return (False, None)

	def __is_number(self, name, data): 
		try:
			temp = re.findall('\d+', data) #getting numbers only

			if len(temp) != 5:
				self.__errors.append("'%s' incorrect number" % (name,))
				return (False, None)

			if "%s (%s) %s-%s-%s" % tuple(temp) != data:
				self.__errors.append("'%s' incorrect number" % (name,))
				return (False, None)

			if not (temp[0] == '8' and temp[1][0] == '9'):
				self.__errors.append("'%s' incorrect number" % (name,))
				return (False, None)

			temp = '7'+''.join(temp)[1:]

			if len(temp) != 11:
				self.__errors.append("'%s' incorrect number" % (name,))
				return (False, None)

			return (True, temp)

		except Exception:
			self.__errors.append("'%s' not a number" % (name,))
			return (False, None)

	def __is_array(self, name, data): 
		try:
			if isinstance(data, (list, tuple)):
				el_type = type(data[0])

				for i in data[1:]: #elements type checking
					if type(i) != el_type:
						self.__errors.append("'%s' has elements of different types", (name,))
						return (False, None)

				return (True, list(data))
			else:
				self.__errors.append("'%s' not array" % (name,))
				return (False, None)				
		except Exception:
			self.__errors.append("'%s' not array" % (name,))
			return (False, None)

	def __is_structure(self, name, data):
		try:
			if isinstance(data, dict):
				return (True, data)
			else:
				self.__errors.append("'%s' not structure" % (name,))
				return (False, None)				
		except Exception:
			self.__errors.append("'%s' not structure" % (name,))
			return (False, None)

	def p(self):
		print(self.__data)
