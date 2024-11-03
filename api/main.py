from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Import models, schemas, and controllers
from .models import models, schemas
from .controllers import orders, sandwiches, resources, recipes, order_details  # Import other controllers
from .dependencies.database import engine, get_db

# Create the database tables if they don't already exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS settings
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- ORDERS Endpoints -------------------

@app.post("/orders/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)

@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)

@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order_db = orders.read_one(db, order_id=order_id)
    if order_db is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders.update(db=db, order=order, order_id=order_id)

@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders.delete(db=db, order_id=order_id)

# ------------------- SANDWICHES Endpoints -------------------

@app.post("/sandwiches/", response_model=schemas.Sandwich, tags=["Sandwiches"])
def create_sandwich(sandwich: schemas.SandwichCreate, db: Session = Depends(get_db)):
    return sandwiches.create(db=db, sandwich=sandwich)

@app.get("/sandwiches/", response_model=list[schemas.Sandwich], tags=["Sandwiches"])
def read_sandwiches(db: Session = Depends(get_db)):
    return sandwiches.read_all(db)

@app.get("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    db_sandwich = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return db_sandwich

@app.put("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def update_sandwich(sandwich_id: int, sandwich: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    updated_sandwich = sandwiches.update(db, sandwich_id=sandwich_id, sandwich=sandwich)
    if updated_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return updated_sandwich

@app.delete("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    deleted = sandwiches.delete(db, sandwich_id=sandwich_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return {"message": "Sandwich deleted successfully"}

# ------------------- RESOURCES Endpoints -------------------

@app.post("/resources/", response_model=schemas.Resource, tags=["Resources"])
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return resources.create(db=db, resource=resource)

@app.get("/resources/", response_model=list[schemas.Resource], tags=["Resources"])
def read_resources(db: Session = Depends(get_db)):
    return resources.read_all(db)

@app.get("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = resources.read_one(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@app.put("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def update_resource(resource_id: int, resource: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    updated_resource = resources.update(db, resource_id=resource_id, resource=resource)
    if updated_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return updated_resource

@app.delete("/resources/{resource_id}", tags=["Resources"])
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    deleted = resources.delete(db, resource_id=resource_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"message": "Resource deleted successfully"}

# ------------------- RECIPES Endpoints -------------------

@app.post("/recipes/", response_model=schemas.Recipe, tags=["Recipes"])
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return recipes.create(db=db, recipe=recipe)

@app.get("/recipes/", response_model=list[schemas.Recipe], tags=["Recipes"])
def read_recipes(db: Session = Depends(get_db)):
    return recipes.read_all(db)

@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def read_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = recipes.read_one(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

@app.put("/recipes/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def update_recipe(recipe_id: int, recipe: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    updated_recipe = recipes.update(db, recipe_id=recipe_id, recipe=recipe)
    if updated_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe

@app.delete("/recipes/{recipe_id}", tags=["Recipes"])
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    deleted = recipes.delete(db, recipe_id=recipe_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}

# ------------------- ORDER_DETAILS Endpoints -------------------

@app.post("/order_details/", response_model=schemas.OrderDetail, tags=["OrderDetails"])
def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    return order_details.create(db=db, order_detail=order_detail)

@app.get("/order_details/", response_model=list[schemas.OrderDetail], tags=["OrderDetails"])
def read_order_details(db: Session = Depends(get_db)):
    return order_details.read_all(db)

@app.get("/order_details/{order_detail_id}", response_model=schemas.OrderDetail, tags=["OrderDetails"])
def read_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    db_order_detail = order_details.read_one(db, order_detail_id=order_detail_id)
    if db_order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return db_order_detail

@app.put("/order_details/{order_detail_id}", response_model=schemas.OrderDetail, tags=["OrderDetails"])
def update_order_detail(order_detail_id: int, order_detail: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    updated_order_detail = order_details.update(db, order_detail_id=order_detail_id, order_detail=order_detail)
    if updated_order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return updated_order_detail

@app.delete("/order_details/{order_detail_id}", tags=["OrderDetails"])
def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    deleted = order_details.delete(db, order_detail_id=order_detail_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return {"message": "Order detail deleted successfully"}
