from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with

app = Flask(__name__)
api = Api(app)

product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'category': fields.String,
    'price': fields.Float,
    'quantity': fields.Integer
}

products = []

class ProductList(Resource):
    @marshal_with(product_fields)
    def get(self):
        return products

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='ID cannot be blank')
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
        parser.add_argument('category', type=str, required=True, help='Category cannot be blank')
        parser.add_argument('price', type=float, required=True, help='Price cannot be blank')
        parser.add_argument('quantity', type=int, required=True, help='Quantity cannot be blank')
        args = parser.parse_args()

        new_product = {
            'id': args['id'],
            'name': args['name'],
            'category': args['category'],
            'price': args['price'],
            'quantity': args['quantity']
        }
        products.append(new_product)
        return new_product, 201

class Product(Resource):
    @marshal_with(product_fields)
    def get(self, id):
        product = next((prod for prod in products if prod['id'] == id), None)
        if product is None:
            return {'message': 'Product not found'}, 404
        return product

    def delete(self, id):
        global products
        products = [prod for prod in products if prod['id'] != id]
        return '', 204

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('category', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('quantity', type=int)
        args = parser.parse_args()

        product = next((prod for prod in products if prod['id'] == id), None)
        if product is None:
            return {'message': 'Product not found'}, 404

        if args['name']:
            product['name'] = args['name']
        if args['category']:
            product['category'] = args['category']
        if args['price']:
            product['price'] = args['price']
        if args['quantity']:
            product['quantity'] = args['quantity']
        return product

class ProductStats(Resource):
    def get(self):
        if not products:
            return {"message": "No products available to calculate statistics"}, 404

        prices = [prod['price'] for prod in products]
        quantities = [prod['quantity'] for prod in products]

        stats = {
            "price": {
                "average": sum(prices) / len(prices),
                "max": max(prices),
                "min": min(prices)
            },
            "quantity": {
                "average": sum(quantities) / len(quantities),
                "max": max(quantities),
                "min": min(quantities)
            }
        }
        return stats

api.add_resource(ProductList, '/products')
api.add_resource(Product, '/products/<int:id>')
api.add_resource(ProductStats, '/products/stats')

if __name__ == '__main__':
    app.run(debug=True)
