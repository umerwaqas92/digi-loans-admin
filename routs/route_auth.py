from flask import Blueprint, render_template, request, jsonify
from flask_app import app  # Import the main Flask app instance


api_routes = Blueprint('api_routes', __name__)
