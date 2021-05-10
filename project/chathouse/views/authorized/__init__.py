from chathouse.views.authorized.controller import ChatController
from flask import Blueprint,request

authorized=Blueprint('authorized',__name__)

@authorized.route('/chat')
def chat():
	return ChatController.handle(dict(request.headers),request.data)