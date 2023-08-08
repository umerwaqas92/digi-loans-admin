from flask import Blueprint, render_template, request, jsonify
from app import app

auth_routes = Blueprint('auth_routes', __name__)
