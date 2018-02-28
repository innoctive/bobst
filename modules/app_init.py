from flask import Flask, flash, redirect, render_template, request, session, abort, json, jsonify, make_response,url_for
from sqlalchemy import create_engine
from dateutil.parser import parse
from passlib.hash import sha256_crypt
import urllib, urllib2

# Imports for the Flask Session
from sqlalchemy.orm import sessionmaker

# Import for the os.urandom(12) i.e. App Secret Key
import os, sys, subprocess

def include(filename):
    if os.path.exists(filename): 
        execfile(filename)

# Initial Flask App name and set the secret key
app = Flask(__name__)
include('secret.py')


