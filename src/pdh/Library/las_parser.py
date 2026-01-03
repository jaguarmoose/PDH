'''LAS Parser Class and Exceptions'''
import os
import re
import traceback
from collections import deque

class LASParser(object):
	'''LAS Parser returns parsed lines'''

	parameter_rule = re.compile(r'([^\.]*)\.([^\s]*)\s*([^:]*):([^\n\|]*)\|*([^\n]*)')
	section_rule = re.compile(r'~([^ \[]*)')
	vers_parameters = set(('wrap', 'vers', 'sep'))
	well_parameters = set(('strt', 'stop', 'step', 'null'))

	def __init__(self, data=None):
		'''Initialize LASParser'''
		if data != None:
			self.__dict__ = data
		self.curves = []
		self.current_section = None
		self.line_type = None
		self.line_num = 1
		self.SEP = None
		self.WRAP = None
		self.STRT = None
		self.STOP = None
		self.STEP = None
		self.NULL = None
		self.VERS = None

	@staticmethod
	def get_section(match):
		'''get section type'''
		return {
			'V': 'VERSION',
			'W': 'WELL',
			'P': 'PARAMETER',
			'PARAMETERS': 'PARAMETER',
			'LOG_PARAMETER': 'PARAMETER',
			'C': 'CURVE',
			'LOG_DEFINITION': 'CURVE',
			'O': 'OTHER',
			'A': 'ASCII',
			'LOG_DATA': 'ASCII',
		}.get(match, match)

	@staticmethod
	def get_line_type(match):
		'''get line type'''
		return {
			'VERSION': 'PARAMETER',
			'WELL': 'PARAMETER',
			'CURVE': 'PARAMETER',
			'PARAMETER': 'PARAMETER',
			'ASCII': 'ASCII',
			'OTHER': 'COMMENT',
			'COMMENT': 'COMMENT',
		}.get(match, "COMMENT")

	@staticmethod
	def parse_parameter_line(line):
		'''Parses Parameters Line Returning Components
		Split Parameter Line Format into pieces and strip'''
		return tuple(val.strip() for val in LASParser.parameter_rule.match(line).groups())

	@staticmethod
	def parse_section_line(line):
		'''Parses Section Line Returning Section'''
		match = LASParser.section_rule.match(line)
		return match.group(1).upper() if match else None

	def parse_las(self, lines):
		'''Pass in raw las file lines'''
		for self.line_num, line in enumerate(lines, self.line_num):
			# Check for Section Delimiter Character ~
			if line.strip() == '':
				pass
			elif line.strip().startswith('~'):
				section_match = LASParser.parse_section_line(line.strip().lower())
				self.current_section = LASParser.get_section(section_match)
				self.line_type = LASParser.get_line_type(self.current_section)
			elif self.line_type == 'ASCII':
				self.parse_ascii(lines)
			elif line.strip().startswith('#'):
				yield ('COMMENT', self.parse_comment(line))
			else:
				parse_function = getattr(self, 'parse'+self.line_type)
				if parse_function:
					yield (self.current_section, parse_function(line))
				else:
					raise LASParseError(
						"Unknown Section: {} Line: {} at Line#: {}".format(self.current_section, line.strip(), self.line_num))

	def parse_comment(self, line):
		'''Parse the line_type Comment'''
		return line

	def parse_parameter(self, line):
		'''Parse the line_type Parameter'''
		try:
			parameter, unit, value, description, group = LASParser.parse_parameter_line(line)
			if self.VERS is not None and self.VERS < 2:
				value, description = description, value
		except:
			raise LASParseError("Unable to parse parameter line: {} at Line#: {}".format(
				line.strip(), self.line_num))
		if self.current_section == 'CURVE':
			# build list so we can use these later
			self.curves.append(parameter.strip())
		elif ((self.current_section == 'WELL' and parameter.lower() in LASParser.well_parameters) or
			(self.current_section == 'VERSION' and parameter.lower() in LASParser.vers_parameters)):
				try:
					getattr(self, 'parameter'+parameter.upper())(value)
				except AttributeError:
					self.__dict__[parameter] = value
		return (parameter, unit, value, description, group)

	def parameter_vers(self, value):
		'''Set Version Value'''
		try:
			self.VERS = float(value)
		except ValueError:
			self.VERS = value

	def parse_ascii(self, lines):
		'''handle ascii block'''
		first_line = True
		line = ""
		for self.line_num, line in enumerate(lines, self.line_num):
			if self.SEP is None:
				values = line.split()
			else:
				values = line.split(self.SEP)
			if len(values) != len(self.curves):
				raise LASParseError("Mismatch Length of Curves: {} and Values: {} for Line#: {}".format(
					values[0], self.curves[0], line))
			else:
				if first_line:
					first_line = False
					if float(self.STRT) != float(values[0]):
						if float(self.STOP) == float(values[0]):
							raise LASParseError("Stop Value: {} matches First Value: {} in Reference: {} for Line#: {}".format(
								self.STOP, values[0], self.curves[0], line))
						else:
							raise LASParseError("Start Value: {} does not match First Value: {} in Reference: {} for Line#: {}".format(
								self.STRT, values[0], self.curves[0], line))
				yield (self.current_section, values)

		if float(self.STOP) != float(values[0]):
			raise LASParseError("Stop Value: {} does not match Last Value: {} in Reference: {} for Line#: {}".format(
				self.STOP, values[0], self.curves[0], line))

class LASParseError(Exception):
	'''LAS Parsing Errors'''
	pass

def exception_processor(las_file, parser):
	'''Continue processing LAS after exception'''
	try:
		deque(parser.parse_las(las_file))
	except LASParseError as ex:
		print(ex, las_file.name)
		print(traceback.format_exc())
		if las_file is not None:
			exception_processor(las_file, parser)


def validate_folder(folder_path=None):
	'''Validate LAS files in a folder using the class-based parser.'''
	if folder_path is None:
		folder_path = os.path.realpath(os.path.join("Development", "LAS", "LAS Files"))

	for root, dirs, files in os.walk(folder_path, topdown=False):
		for filename in files:
			if filename.lower().endswith('.las'):
				filepath = os.path.join(root, filename)
				with open(filepath, 'r') as las_file:
					parser = LASParser()
					exception_processor(las_file, parser)


def main():
	'''Run LAS validation using default folder location.'''
	validate_folder()


if __name__ == '__main__':
	main()
