
from flask import Flask, render_template, request

app = Flask(__name__)


from app.templates import *
from app.controllers import router