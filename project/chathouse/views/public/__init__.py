from chathouse.views.public.controller import SignUpController,StartController,LogInController,VerifyController
from flask import Blueprint,request


public=Blueprint('public',__name__)

@public.route('/')
@public.route('/start')
def start():
	return StartController.handle(dict(request.headers),request.data)

@public.route('/signup')
def signup():
	return SignUpController.handle(dict(request.headers),request.data)

@public.route('/login')
def login():
	return LogInController.handle(dict(request.headers),request.data)

@public.route('/verify/<token>')
def verify(token):
	return VerifyController.handle(dict(request.headers),request.data,verification_token=token)