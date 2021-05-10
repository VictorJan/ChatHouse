from abc import ABC, abstractmethod

class Handler:
	@abstractmethod
	def accept(self,headers,data,**kwargs):
		pass
