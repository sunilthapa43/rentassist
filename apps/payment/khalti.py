
import os
import requests
my_test_key = 'test_secret_key_628669de2b844a73b0b5a8c86db738ff'

class Khalti:

    def __init__(self, user, token, amount):
        self.user = user
        self.token = token
        self.amount = amount
        self.response = None



    def verify_request(self):
        """
        It takes the token and amount from the user and sends it to the Khalti
        API
        :return: The response is a dictionary with the following keys:
        """
        url = 'https://khalti.com/api/v2/payment/verify'
        headers = {
            'Authorization': my_test_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'token': self.token,
            'amount':
                self.amount  # In Paisa
        }
        response = requests.post(url, payload, headers=headers)
        self.response = response.json()
        return self.response