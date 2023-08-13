from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time
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

# Ideally should be a different database for a different microservice
redis = get_redis_connection(
    host="redis-10223.c8.us-east-1-2.ec2.cloud.redislabs.com:10223",
    port=123456,
    password="i5hLAg0mYAReM3XT5MEac7GWrgpAr9kg",
    decode_responses=True
)

# Model object for Order
class Order(HashModel):
    product_id: str
    price: float
    fee: float # 20% of price
    total: float # total = price + fee
    quantity: int
    status: str  # ("PENDING", "REFUNDED", "COMPLETED")

    class Meta:
        database: redis


@app.get('/orders/getOrder/{pk}')
def getOrderById(pk : str):
    try:
        getOrder = Order.get(pk)
        return getOrder
    except Exception as e:
        logging.error(e)
        logging.error("Unable to get the order for this id")




@app.post('/orders/placeOrder')
async def createOrder(request: Request, background_tasks: BackgroundTasks):

    requestBody = await request.json()
    product_key = str(requestBody["id"])

    logging.info("Product Key is == "+product_key)
    url = 'http://127.0.0.1:8000/products/getProductById/'+product_key
    logging.info("Inventory endpoint hit =="+url)


    # Fetch product response from Inventory
    try:
        inventory_response = requests.get(url)
        logging.info("Response received from inventory =="+str(inventory_response.json()))
    except Exception as e:
        logging.error(e)

    inventory_product = inventory_response.json()

    order = Order(
        product_id= requestBody['id'],
        price= inventory_product['price'],
        fee= 0.2 * inventory_product['price'],
        total= 1.2 * inventory_product['price'],
        quantity= inventory_product['quantity'],
        status='PENDING'
    )

    
    try:
        # Save order
        order.save()
        
        # BackgroundTasks creates a separate thread --> Callable interface
        background_tasks.add_task(order_completed, order)
        
        logging.info("Order saved successfully for the product == "+requestBody['id'])
        return order
    
    except Exception as e:
        logging.error(e)
        logging.error("Could not save the order")
    
    


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'COMPLETED'
    logging.info("Order completed method === "+str(order.status))
    order.save()
    redis_order_completed_event(order)


# Create a ORDER_COMPLETED_EVENT in redis streams
def redis_order_completed_event(order: Order):

    # first argument --> ORDER_COMPLETED_EVENT --> event
    # second argument --> order object as dict
    # third argument --> * (indicates autocreation of an id for the event)

    redis.xadd('ORDER_COMPLETED_EVENT', order.dict(), '*')

    
    




