from abc import ABC, abstractmethod

class Strategy:
	@abstractmethod
	def accept(self,headers,data,**kwargs):
		pass
