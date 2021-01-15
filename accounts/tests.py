import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "..settings")
import django
django.setup()
from django.test import TestCase, Client
import unittest

# my django imports
from models import *

class CreateUserFormTest(unittest.TestCase):

    def test_new_agent_form(self):
        return True

if __name__ == "__main__":
    unittest.main()
