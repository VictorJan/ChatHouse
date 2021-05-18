from chathouse.views.authorized.controller import ChatController,LogoutController
from flask import Blueprint,request

authorized=Blueprint('authorized',__name__)

@authorized.route('/chat')
def chat():
	return ChatController.handle(dict(request.headers),dict(request.data),chat_id=request.args.get('id',None))

@authorized.route('/logout')
def logout():
	return LogoutController.handle(dict(request.headers),dict(request.data))