from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class TodosItem(BaseModel):
    text: str
    is_complete: bool


@app.get("/all-todos")
def read_todos() -> [TodosItem]:
    data = read()
    return data


def save(data):
    with open('data.json', 'w') as output:
        output.write(json.dumps(data))

def read():
    data = json.load(open("data.json"))

@app.get("/filter-by-id/{item_id}/")
def filter_todos(item_id:int) -> [TodosItem]:
    data = read()
    for item in data:
        if item['id'] == item_id:
            return item
    return {'error': 'item not found'}

@app.delete("/delete/{item_id}/")
def delete_todos(item_id:int):
    data = read()
    for index, item in enumirate(data):
        if item['id'] == item_id:
            data.pop(index)
            save(data)
            return {'success': True, 'error': ''}
        return {'success': False, 'error': 'item not found'}

@app.post("/create/")
def create_todos(item: TodosItem):
    data = read()
    last_id = data[-1]['id']
    item['id'] = last_id + 1
    data.append(item)
    save(data)
    return {'success': True, 'error': ''}