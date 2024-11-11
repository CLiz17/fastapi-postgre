from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items/")
def create_item(name: str, db: Session = Depends(database.get_db)):
    item = models.Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/items/")
def read_items(db: Session = Depends(database.get_db)):
    return db.query(models.Item).all()