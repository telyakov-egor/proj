import unittest
from main import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_products(self):
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        response = self.app.post('/products', json={
            'id': 2,
            'name': 'Banana',
            'category': 'Fruit',
            'price': 0.3,
            'quantity': 200
        })
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()
