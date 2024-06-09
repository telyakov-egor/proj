from flask import Flask, request, jsonify  # Импорт необходимых модулей из Flask
from flask_restx import Api, Resource, fields  # Импорт модулей из Flask-RESTX для создания API
from models import Product  # Импорт модели Product из файла models.py (предполагается, что этот файл существует)

app = Flask(__name__)  # Создание экземпляра Flask
api = Api(app, version='1.0', title='Product Sales API', description='A simple Product Sales API')  # Создание экземпляра API с описанием

ns = api.namespace('products', description='Product operations')  # Создание namespace для операций с продуктами

# Определение модели продукта для API
product_model = api.model('Product', {
    'id': fields.Integer(required=True, description='The product identifier'),  # Поле идентификатора продукта
    'name': fields.String(required=True, description='The product name'),  # Поле имени продукта
    'category': fields.String(required=True, description='The product category'),  # Поле категории продукта
    'price': fields.Float(required=True, description='The product price'),  # Поле цены продукта
    'quantity': fields.Integer(required=True, description='The product quantity')  # Поле количества продукта
})

# Список для хранения данных о продуктах
products = []

@ns.route('/')  # Определение маршрута для операций с продуктами
class ProductList(Resource):
    @ns.doc('list_products')  # Документация для метода list_products
    @ns.marshal_list_with(product_model)  # Определение схемы данных для ответа
    def get(self):
        """Получить список всех продуктов"""
        return products  # Возвращаем список продуктов

    @ns.doc('create_product')  # Документация для метода create_product
    @ns.expect(product_model)  # Ожидаемая структура данных для запроса
    @ns.marshal_with(product_model, code=201)  # Определение схемы данных для ответа и код ответа 201
    def post(self):
        """Создать новый продукт"""
        data = request.json  # Получаем данные запроса в формате JSON
        new_product = {
            'id': data['id'],
            'name': data['name'],
            'category': data['category'],
            'price': data['price'],
            'quantity': data['quantity']
        }  # Создаем новый продукт
        products.append(new_product)  # Добавляем новый продукт в список
        return new_product, 201  # Возвращаем созданный продукт и код ответа 201

@ns.route('/<int:id>')  # Определение маршрута для операций с конкретным продуктом
@ns.response(404, 'Product not found')  # Ответ в случае, если продукт не найден
@ns.param('id', 'The product identifier')  # Описание параметра id
class Product(Resource):
    @ns.doc('get_product')  # Документация для метода get_product
    @ns.marshal_with(product_model)  # Определение схемы данных для ответа
    def get(self, id):
        """Получить продукт по идентификатору"""
        product = next((prod for prod in products if prod['id'] == id), None)  # Поиск продукта по идентификатору
        if product is None:  # Если продукт не найден
            api.abort(404, "Product {} doesn't exist".format(id))  # Прервать выполнение с ошибкой 404
        return product  # Возвращаем найденный продукт

    @ns.doc('delete_product')  # Документация для метода delete_product
    @ns.response(204, 'Product deleted')  # Ответ в случае успешного удаления
    def delete(self, id):
        """Удалить продукт по идентификатору"""
        global products  # Используем глобальную переменную products
        products = [prod for prod in products if prod['id'] != id]  # Удаляем продукт по идентификатору
        return '', 204  # Возвращаем пустой ответ и код 204

    @ns.doc('update_product')  # Документация для метода update_product
    @ns.expect(product_model)  # Ожидаемая структура данных для запроса
    @ns.marshal_with(product_model)  # Определение схемы данных для ответа
    def put(self, id):
        """Обновить продукт по идентификатору"""
        product = next((prod for prod in products if prod['id'] == id), None)  # Поиск продукта по идентификатору
        if product is None:  # Если продукт не найден
            api.abort(404, "Product {} doesn't exist".format(id))  # Прервать выполнение с ошибкой 404
        data = request.json  # Получаем данные запроса в формате JSON
        product.update(data)  # Обновляем данные продукта
        return product  # Возвращаем обновленный продукт

@ns.route('/stats')  # Определение маршрута для получения статистики
class ProductStats(Resource):
    @ns.doc('get_product_stats')  # Документация для метода get_product_stats
    def get(self):
        """Получить статистику по продуктам"""
        if not products:  # Если список продуктов пуст
            return {"message": "No products available to calculate statistics"}, 404  # Возвращаем сообщение об ошибке и код 404

        prices = [prod['price'] for prod in products]  # Получаем список цен всех продуктов
        quantities = [prod['quantity'] for prod in products]  # Получаем список количеств всех продуктов

        # Вычисляем статистику для цен и количеств
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
        return stats  # Возвращаем вычисленную статистику

if __name__ == '__main__':
    app.run(debug=True)  # Запускаем приложение Flask в режиме отладки
