"""LAS Parser Class and Exceptions"""
import re
import os
from collections import deque



class LASParser(object):
	"""LAS Parser returns parsed lines"""

	sep = None
	version = None
	wrap = None
	strt = None
	stop = None
	step = None
	null = None
	curves = []
	version = None
	current_section = None
	parameter_rule = re.compile(r'([^\.]*)\.([^\s]*)\s*([^:]*):([^\n]*)')

	def __init__(self):
		"""Initialize LASParser"""
		pass

	@staticmethod
	def getSection(match):
		"""get section name from first Upper character"""
		return {
			'A': 'ascii',
			'C': 'curve',
			'V': 'version',
			'W': 'well',
			'P': 'parameter',
			'O': 'other'
		}[match]

	@staticmethod
	def parseParameterLine(self,line):
		"""Parses Parameters Line Returning Components"""
		# Split common line format into pieces and clean
		match = self.parameter_rule.match(line)
		map(str.strip, match.groups())
		if match:
			if self.version is not None and self.version < 2:
				return map(str.strip, match.groups())[0, 1, 3, 2]
			return map(str.strip, match.groups())[0, 1, 3, 2]
		else:
			raise LASParseError(
				"Unable to parse line: {} at Line#: {}".format(line.strip(), i))

	def parseLAS(self, lines):
		"""Pass in raw las file lines"""
		for i, line in enumerate(lines):
			# Check for Section Delimiter Character ~
			if line.strip().startswith('~'):
				try:
					self.current_section = LASParser.getSection(
						line.strip()[1:2].upper())
				except:
					raise LASParseError(
						"Unknown Section: {} at Line#: {}".format(line.strip(), i))
			if line.strip().startswith('#') or self.current_section == 'other':
				yield('comment', line)
			elif self.current_section != 'ascii':
				parameter, unit, value, description = parseParameterLine(line)
				if self.current_section == 'version':
					if parameter.upper() == 'WRAP':
						self.wrap = value
					elif parameter.upper() == 'VERS':
						# Try to float value so we can compare it
						# numerically
						try:
							self.version = float(value)
						except ValueError:
							self.version = value
					elif parameter.upper() == 'SEP':
						self.sep = value
				elif self.current_section == 'well':
					if parameter.upper() == 'STRT':
						self.strt = value
					elif parameter.upper() == 'STOP':
						self.stop = value
					elif parameter.upper() == 'STEP':
						self.step = value
					elif parameter.upper() == 'NULL':
						self.null = value
				elif self.current_section == 'curve':
					# build list so we can use these later
					self.curves.append(parameter.strip())
				yield(self.current_section, (parameter, unit, value, description))
			else:
				# handle ascii block
				first_line = True
				for i, line in enumerate(lines, i):
					if self.sep is None:
						values = line.split()
					else:
						values = line.split(self.sep)
					if len(values) != len(self.curves):
						raise LASParseError("Mismatch Length of Curves: {} and Values: {} for Line#: {}".format(
							values[0], self.curves[0], line))
					else:
						if first_line:
							first_line = False
							if float(self.strt) != float(values[0]):
								if float(self.stop) == float(values[0]):
									raise LASParseError("Stop Value: {} matches First Value: {} in Reference: {} for Line#: {}".format(
										self.stop, values[0], self.curves[0], line))
								else:
									raise LASParseError("Start Value: {} does not match First Value: {} in Reference: {} for Line#: {}".format(
										self.strt, values[0], self.curves[0], line))
						yield (self.current_section, values)

				if float(self.stop) != float(values[0]):
					raise LASParseError("Stop Value: {} does not match Last Value: {} in Reference: {} for Line#: {}".format(
						self.stop, values[0], self.curves[0], line))


class LASParseError(Exception):
	"""LAS Parsing Errors"""
	pass


if __name__ == '__main__':
	__folder_path__ = os.path.realpath(os.path.join("Development", "LAS",
													"LAS Files"))

	__parser__ = LASParser()
	for root, dirs, files in os.walk(__folder_path__, topdown=False):
		for filename in files:
			if filename.lower().endswith('.las'):
				filepath = os.path.join(root, filename)
				with open(filepath, 'r') as las_file:
					try:
						deque(__parser__.parseLAS(las_file))
						# print('\n'.join(map(str, parseLAS(lashan))))
					except LASParseError as ex:
						print(ex, filepath)
						# exc_type, exc_obj, tb = sys.exc_info()
						# f = tb.tb_frame
						# lineno = tb.tb_lineno
						# python_filename = f.f_code.co_filename
						# print 'EXCEPTION {}, FILE {},
						# {}'.format(type(e).__name__,filepath, e)
