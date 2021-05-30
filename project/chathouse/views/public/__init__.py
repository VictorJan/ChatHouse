'''
This file shall contain initialization of the public Blueprint. Defines the following publicly-available routes and provides respetive [view]Controllers, which handle the requests initiating an according Strategy:
/,/start - [Start]Controller;
/signup - [SignUp]Controller;
/login - [LogIn]Controller
/verify/<token> - [Verify]Controller;
/confirm/<token> - [Cofirm]Controller.
'''

from chathouse.views.public.controller import SignUpController,StartController,LogInController,VerifyController,ConfirmController
from flask import Blueprint,request


public=Blueprint('public',__name__)

@public.route('/')
@public.route('/start')
def start():
	'''
	Goal: accept requests aimed at the '/' or '/start' route.
	Actions: handling is executed by a respective view controller - StartContoller, by providing incoming headers and an empty dictionary - for the data, due to acception of only GET requests.
	Returns:render_template|redirect|make_response - result of the respective handling.
	'''
	return StartController.handle(dict(request.headers),{})

@public.route('/signup')
def signup():
	'''
	Goal: accept requests aimed at the 'signup' route.
	Actions: handling is executed by a respective view controller - SignUpContoller, by providing incoming headers and an empty dictionary - for the data, due to acception of only GET requests.
	Returns:render_template|redirect|make_response - result of the respective handling.
	'''
	return SignUpController.handle(dict(request.headers),{})

@public.route('/login')
def login():
	'''
	Goal: accept requests aimed at the '/login' route.
	Actions: handling is executed by a respective view controller - LogInContoller, by providing incoming headers and an empty dictionary - for the data, due to acception of only GET requests.
	Returns:render_template|redirect|make_response - result of the respective handling.
	'''
	return LogInController.handle(dict(request.headers),{})

@public.route('/verify/<string:token>')
def verify(token):
	'''
	Goal: accept requests aimed at the '/verify' route.
	Actions: handling is executed by a respective view controller - VerifyContoller, by providing modified incoming headers and an empty dictionary - for the data, due to acception of only GET requests.
	Arguments:token:str - meant to store a verification token.
	[Note headers are explictly populated with the provided verification token, by injecting it to a new field transmited-verification_token. This is done to perform validaton of the token/outcast
	requests with such invalid tokens, before serving the page.]
	Returns:render_template|redirect|make_response - result of the respective handling.
	'''
	return VerifyController.handle(dict(request.headers,**{'transmited-verification_token':token}),{})

@public.route('/confirm/<string:token>')
def confirm(token):
	'''
	Goal: accept requests aimed at the '/confirm' route.
	Actions: handling is executed by a respective view controller - ConfirmContoller, by providing modified incoming headers and an empty dictionary - for the data, due to acception of only GET requests.
	Arguments:token:str - meant to store a confirmation token.
	[Note headers are explictly populated with the provided confirmation token, by injecting it to a new field transmited-confirmation_token. This is done to perform validaton of the token/outcast
	requests with such invalid tokens, before serving the page.]
	Returns:render_template|redirect|make_response - result of the respective handling.
	'''
	return ConfirmController.handle(dict(request.headers,**{'transmited-confirmation_token':token}),{})

