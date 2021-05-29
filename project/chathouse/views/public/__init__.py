from chathouse.views.public.controller import SignUpController,StartController,LogInController,VerifyController,ConfirmController
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
	return VerifyController.handle(dict(request.headers,**{'transmited-verification_token':token}),request.data,verification_token=token)

@public.route('/confirm/<token>')
def confirm(token):
	return ConfirmController.handle(dict(request.headers,**{'transmited-confirmation_token':token}),request.data,confirmation_token=token)

