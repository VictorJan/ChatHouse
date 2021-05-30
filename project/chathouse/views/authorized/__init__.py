from chathouse.views.authorized.controller import ChatController,LogoutController
from flask import Blueprint,request

authorized=Blueprint('authorized',__name__)

@authorized.route('/chat')
def chat():
	'''
	Goal: accept requests aimed at the '/chat' route.
	Actions: handling is executed by a respective view controller - ChatContoller, by providing modified incoming headers and an empty dictionary - for the data, due to acception of only GET requests.
	Returns:render_template|redirect|make_response - result of the respective handling.
	'''
	return ChatController.handle(dict(request.headers),{},chat_id=request.args.get('id',None,int))

@authorized.route('/logout')
def logout():
	'''
	Goal: accept requests aimed at the '/logout' route.
	Actions: handling is executed by a respective view controller - LogoutContoller, by providing modified incoming headers and an empty dictionary - for the data, due to acception of only GET requests.
	Returns:redirect|make_response - result of the respective handling.
	'''
	return LogoutController.handle(dict(request.headers),{})