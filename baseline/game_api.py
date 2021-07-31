#!/usr/bin/env python
import json
from typing import Optional
from pydantic import BaseModel, ValidationError
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from flask import Flask, request

app = Flask(__name__)
app.producer = None


def log_to_kafka(topic, event):
    if app.producer is None:
        try:
            app.producer = KafkaProducer(bootstrap_servers='kafka:29092')
        except NoBrokersAvailable:
            if app.debug:
                print('NoBrokersAvailable')
                return
            raise NoBrokersAvailable
    event.update(request.headers)
    app.producer.send(topic, json.dumps(event).encode())

@app.route("/", methods=['GET', 'POST'])
def home():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"


# Store Interactions

## Kept for potential future implementation
# class Purchase(BaseModel):
#     request_id: int
#     user_id: int
#     item_id: int
#     item_kind: Optional[str] = None
#     item_type: Optional[str] = None
#     quantity: int
#     price_paid: float
#     vendor_id: int
#     vendor_quantity_avail: Optional[int] = None
#     vendor_list_price: Optional[float] = None
#     client_timestamp: Optional[datetime] = None
#     request_status = "failed"


class PurchaseEvent(BaseModel):
    user_id: int
    item_id: int
    quantity: Optional[int] = None
    price_paid: Optional[float] = None
    vendor_id: Optional[int] = None
    api_string: Optional[str]
    request_status: Optional[str] = 'incomplete'

@app.route("/purchase", methods=['POST', 'GET'])
def purchase():
    # Normal behavior first
    try:
        # Validate JSON and copy if works, need to replace with proper inputs
        content = request.get_json(silent=True)
        event = PurchaseEvent(**content)
        event.api_string = json.dumps(content)  # replace w full str
        event.request_status = 'success'
    # If data missing required fields, log request and errors
    except ValidationError as e:
        # we need to get the json data again to keep the linter happy.
        content = request.get_json(silent=True)
        event = PurchaseEvent(**{
            "request_status": "invalid",
            "api_string": json.dumps(content)
        })
    event = event.dict()
    log_to_kafka("purchases", event)
    return event

# Guild Interactions

## Kept for potential future implementation
# class GuildAction(BaseModel):
#     request_id: int
#     user_id: int
#     guild_id: int
#     action: Optional[str] = None
#     client_timestamp: Optional[datetime] = None
#     request_status = "failed"


class GuildActionEvent(BaseModel):
    user_id: int
    guild_id: int
    action: Optional[str] = 'None'
    api_string: Optional[str]
    request_status: Optional[str] = 'incomplete'

@app.route("/guild", methods=['POST', 'GET'])
def guild_action():
    # Normal behavior first
    try:
        # Validate JSON and copy if works, need to replace with proper inputs
        content = request.get_json(silent=True)
        event = GuildActionEvent(**content)
        event.api_string = json.dumps(content)  # replace w full str
        event.request_status = 'success'
    # If data missing required fields, log request and errors
    except ValidationError as e:
        # we need to get the json data again to keep the linter happy.
        content = request.get_json(silent=True)
        event = GuildActionEvent(**{
            "request_status": "invalid",
            "api_string": json.dumps(content)
        })
    event = event.dict()
    log_to_kafka("guild", event)
    return event

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
