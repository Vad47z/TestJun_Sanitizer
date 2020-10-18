import unittest
from Sanitizer import Sanitizer
import json

class TestSanitizer(unittest.TestCase):

	def setUp(self):
		test_data = ''
		with open('test.json', 'r') as f:
			test_data = json.load(f)

		self.sanitizer = Sanitizer(test_data)

	def test_integer(self):
		self.assertEqual(self.sanitizer.validate(['i' for i in range(9)]), {'integer': 123, 'float':None, 'string':None, 'array_1':None, 'array_2':None, 
																			'number_1':None, 'number_2':None, 'number_3':None, 'structure':None})

	def test_float(self):
		self.assertEqual(self.sanitizer.validate(['f' for i in range(9)]), {'integer': None, 'float':123.0, 'string':None, 'array_1':None, 'array_2':None, 
																			'number_1':None, 'number_2':None, 'number_3':None, 'structure':None})

	def test_string(self):		
		self.assertEqual(self.sanitizer.validate(['s' for i in range(9)]), {'integer': '123', 'float':'123.0', 'string':'abc', 'array_1':None, 'array_2':None, 
																			'number_1':'8 (950) 123-45-67', 'number_2':'8 )950( 123-45-67', 
																			'number_3':'8 (950) 123a-4a5-67a', 'structure':None})

	def test_number(self):
		self.assertEqual(self.sanitizer.validate(['n' for i in range(9)]), {'integer': None, 'float':None, 'string':None, 'array_1':None, 'array_2':None, 
																			'number_1':'79501234567', 'number_2':None, 'number_3':None, 'structure':None})

	def test_array(self):
		self.assertEqual(self.sanitizer.validate(['a' for i in range(9)]), {'integer': None, 'float':None, 'string':None, 'array_1':[1, 2, 3], 'array_2':None, 
																			'number_1':None, 'number_2':None, 'number_3':None, 'structure':None})
	def test_structure(self):
		self.assertEqual(self.sanitizer.validate(['st' for i in range(9)]), {'integer': None, 'float':None, 'string':None, 'array_1':None, 'array_2':None, 
																			'number_1':None, 'number_2':None, 'number_3':None,
																			'structure':{'1':'1', '2':['2', '2'], '3':{'a':'3', '3':['3.0', 'b']}}})


if __name__ == "__main__":
  unittest.main()