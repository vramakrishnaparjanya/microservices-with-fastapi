from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import logging

# Logging config
FORMAT = "%(levelname)s:\t%(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

app = FastAPI()


'''
Adding CORS MiddleWare for front-end to access the APIs exposed
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)


redis = get_redis_connection(
    host="redis-10223.c8.us-east-1-2.ec2.cloud.redislabs.com",
    port=10223,
    password="i5hLAg0mYAReM3XT5MEac7GWrgpAr9kg",
    decode_responses=True
)


# Model object which we insert into redis
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database: redis


@app.get("/")
async def root():
    return {"message": "Hello World"}


def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

# Fetches all the products
@app.get('/products/getAllProducts')
def getAllProducts():
    try:
        logging.info(Product.all_pks)
        return [format(pk) for pk in Product.all_pks()]
    except Exception as e:
        logging.error(e)
        logging.error("Unable to fetch the products at this time")


# Fetches product by id
@app.get("/products/getProductById/{pk}")
def getProductById(pk: str):
    try:
        getProd = Product.get(pk)
        return getProd
    except Exception as e:
        logging.error(e)
        logging.error("Unable to get the product for this id")


# Creates a product
@app.post("/products/createProduct")
def createProduct(product: Product):
    try:
        return product.save()
    except Exception as e:
        logging.error(e)
        logging.error("Could not save the product")


# Deletes a product
@app.get("/products/deleteProduct/{pk}")
def deleteProduct(pk: str):
    try:
        deletedCount = Product.delete(pk)
        logging.info("Items deleted : ",deletedCount)
        return deletedCount
    except Exception as e:
        logging.error(e)
        logging.error("Could not delete the product. please try later")

