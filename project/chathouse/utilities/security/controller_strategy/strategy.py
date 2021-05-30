from abc import ABC, abstractmethod

class Strategy:
	'''
	Strategy - an abstract class meant to be implemented with planned out steps, involving verification and authorization of requests, thus providing certain guildelines.
	Inherits: ABC.
	
	Methods:
		accept(self,headers,data,**kwargs):
			Goal:shall provide an application of a certain acceptance - defining inner guidelines.
	'''
	@abstractmethod
	def accept(self,headers,data,**kwargs):
		pass
