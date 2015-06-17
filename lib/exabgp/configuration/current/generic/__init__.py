# encoding: utf-8
"""
generic/__init__.py

Created by Thomas Mangin on 2015-06-04.
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""


class Generic (object):
	name = 'undefined'
	known = dict()     # command/section and code to handle it
	default = dict()   # command/section has a a defult value, use it if no data was provided
	add = []           # we use the add method of the last object
	append = []        # this key is storing a list
	nlri = []          # nlri modificator

	def __init__ (self, tokerniser, scope, error, logger):
		self.tokeniser = tokerniser
		self.scope = scope
		self.error = error
		self.logger = logger

	def clear (self):
		raise RuntimeError('not implemented in subclass as should be')

	@classmethod
	def register (cls, name):
		def inner (function):
			cls.known[name] = function
			return function
		return inner

	def pre (self):
		return True

	def post (self):
		return True

	def parse (self, name, command):
		if command not in self.known:
			return self.error.set('unknown command')

		try:
			if command in self.default:
				insert = self.known[command](self.tokeniser.iterate,self.default[command])
			else:
				insert = self.known[command](self.tokeniser.iterate)

			if command in self.add:
				self.scope.add(name,insert)
			elif command in self.append:
				self.scope.append(name,insert)
			elif command in self.nlri:
				self.scope.nlri(name,command,insert)
			else:
				self.scope.set(command,insert)
			return True
		except ValueError, exc:
			return self.error.set(str(exc))