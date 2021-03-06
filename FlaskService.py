#!/usr/bin/python3
from flask import Flask, request
import pika
import json

app = Flask(__name__)

@app.route("/rabbit", methods=['POST'])
def create():
  nom = request.form["nom"]
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()
  channel.queue_declare(queue=nom)
  connection.close()
  
  res = {}
  res["code"] = 200
  res["message"] = "File OK"
  return json.dumps(res)
 
@app.route("/rabbit/<nom>", methods=['POST'])
def send(nom=None):
  message = request.form["message"]
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()
  channel.basic_publish(exchange='', routing_key=nom, body=message)
  connection.close()
  
  res = {}
  res["code"] = 200
  res["message"] = "Message OK"
  return json.dumps(res)
  
@app.route("/rabbit/<nom>", methods=['GET'])
def receive(nom=None):
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()
  method_frame, header_frame, body = channel.basic_get(nom)
  if method_frame:
    channel.basic_ack(method_frame.delivery_tag)
    c = 200
    m = "OK"
    body = body.decode("utf-8")
  else:
    c = 404
    m = "NOK"
    body = ""
  
  res = {}
  res["code"] = c
  res["message"] = m
  res["body"] = body
  
  return json.dumps(res)
  
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
