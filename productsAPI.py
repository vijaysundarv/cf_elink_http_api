from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

products = [
    {
        "productName": "Nokia",
        "productModel": 1100,
        "productDescription": "The Greatest Feature Phone Ever"
    },
    {
        "productName": "Pixel",
        "productModel": 5,
        "productDescription": "A Good smart phone. Because I'm using it"
    },
    {
        "productName": "Apple",
        "productModel": 5,
        "productDescription": "Super handy smart mobile"
    }
]

class Product(Resource):
    def get(self, name):
        for product in products:
            if(name == product["productName"]):
                return product, 200
        return "Product not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("productModel")
        parser.add_argument("productDescription")
        args = parser.parse_args()

        for product in products:
            if(name == product["productName"]):
                return "Product with name {} already exists".format(name), 400

        product = {
            "productName": name,
            "productModel": args["productModel"],
            "productDescription": args["productDescription"]
        }
        products.append(product)
        return product, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("productModel")
        parser.add_argument("productDescription")
        args = parser.parse_args()

        for product in products:
            if(name == product["productName"]):
                product["productModel"] = args["productModel"]
                product["productDescription"] = args["productDescription"]
                return product, 200
        
        product = {
            "productName": name,
            "productModel": args["productModel"],
            "productDescription": args["productDescription"]
        }
        products.append(product)
        return product, 201

    def delete(self, name):
        global products
        products = [product for product in products if product["productName"] != name]
        return "{} is deleted.".format(name), 200
      
api.add_resource(Product, "/product/<string:name>")

@app.route('/', methods=['GET'])
def index():
  return 'Server Works!'

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5001, debug = True) 