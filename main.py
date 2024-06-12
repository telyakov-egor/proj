from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, doc='/docs')

product_model = api.model('Product', {
    'id': fields.Integer,
    'name': fields.String,
    'category': fields.String,
    'price': fields.Float,
    'quantity': fields.Integer
})

products = []
@api.route('/products')
class ProductList(Resource):
    @api.marshal_with(product_model, as_list=True)
    def get(self):
        return products

    @api.expect(product_model)
    def post(self):
        new_product = api.payload
        products.append(new_product)
        return new_product, 201

@api.route('/products/<int:id>')
class Product(Resource):
    @api.marshal_with(product_model)
    def get(self, id):
        product = next((prod for prod in products if prod['id'] == id), None)
        if product is None:
            return {'message': 'Product not found'}, 404
        return product

    def delete(self, id):
        global products
        products = [prod for prod in products if prod['id'] != id]
        return '', 204
    @api.expect(product_model)
    def put(self, id):
        product = next((prod for prod in products if prod['id'] == id), None)
        if product is None:
            return {'message': 'Product not found'}, 404

        data = api.payload
        product.update(data)
        return product

@api.route('/products/stats')
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

if __name__ == '__main__':
    app.run(debug=True)
