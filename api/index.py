import sys
import os

# Adds the backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app import app

# This entry point is used by Vercel for the Serverless Function
