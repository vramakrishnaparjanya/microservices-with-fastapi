from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import logging

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
    host="redis-10223.c8.us-east-1-2.ec2.cloud.redislabs.com:10223",
    port=123456,
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



@app.get("/products/getproducts")
def getProducts():
    try:
        return [format(pk) for pk in Product.all_pks()]
    except Exception as e:
        logging.error(e)
        logging.error("Unable to fetch the products at this time")


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }



@app.post("/products/createProduct")
def createProduct(product: Product):
    try:
        return product.save()
    except Exception as e:
        logging.error(e)
        logging.error("Could not save the product")



@app.get("/products/deleteProduct/{pk}")
def deleteProduct(pk: str):
    try:
        deletedCount = Product.delete(pk)
        logging.info("Items deleted : ",deletedCount)
        return deletedCount
    except Exception as e:
        logging.error(e)
        logging.error("Could not delete the product. please try later")









