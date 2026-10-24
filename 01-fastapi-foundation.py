from fastapi import FastAPI
from fastapi import Request
import uvicorn



app = FastAPI(
    title="Swiggy Order Service",
    description=(
        "Internal API for managing orders"
        "Habdle creation, tracking of delivery system"
    ),
    version="1.1.2.3",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

@app.get("/")
def read_root():
    """Root endpoint - Health Check"""
    # FatsAPI convert this dict to json
    return {
        "message": "Welcome to swiggy Order service",
        "status":"healthy"
    }

@app.get("/about")
def about():
    """Return API metaData"""
    return {
        "serive":"Order_service",
        "team":"Backend plateform",
        "region":"ap-south-1",
        "version":"1.2.2"
    }


@app.get("/orders")
def list_orders():
    """List recent orders"""
    return {
        "orders":[
                {"id":1,"item":"butter chicken","status":"dilivered"},
                {"id":1,"item":"paneer tikkan","status":"preparing"},
                {"id":1,"item":"masala dosa","status":"dilivered"},
        ]
    }


@app.get("/orders/status")
def order_status():
    """Get order status"""
    return {
        "total_today":2_340_23,
        "top_city":"bengaluru"
    }


@app.get("/debug/request-info")
async def request_info(request:Request):  # ew can use also async function when we need
    """Inspect the raw request object"""
    return {
        "method":request.method,
        "url":str(request.url),
        "headers":dict(request.headers),
        "path_params":request.path_params,
        "query_params":dict(request.query_params)
    }

@app.get(  # we can cutomize documentation and write want i want
   "/orders/active",
    summary="Get Active Orders",
    description=(
        "Returns all orders that are currently being prepared"
        "or are out for delivery"
    ),
    tags=["orders"],
    response_description="List of active orders objects",
    deprecated=False

    )
def get_active_order():
    """This docstring also appears in docs"""
    return {
        "active_orders":[
            {"id":1, "item":"Masala Dosa","status":"Out-for_delivery"}
        ]
    }


@app.get("/restuarant",tags=["Restuarents"]) # we do not need write everything we can only write what we need to write
def list_restro():
    """another docstring for another endpoint"""
    return {
        "restaurent":[{
            "test":"test"
        }]
    }
