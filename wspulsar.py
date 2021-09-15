import websocket, base64, json

# If set enableTLS to true, your have to set tlsEnabled to true in conf/websocket.conf.
enable_TLS = False
scheme = 'ws'
if enable_TLS:
    scheme = 'wss'

TOPIC = scheme + '://192.168.1.181:8080/ws/v2/producer/persistent/public/default/my-topic'

ws = websocket.create_connection(TOPIC)


message = "Hello World 345345"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

ws.send(json.dumps({
   'payload' : base64_message,
   'properties': {
       'device' : 'jetson2gb',
       'protocol' : 'websockets'
   },
   'context' : 5
}))

response =  json.loads(ws.recv())
if response['result'] == 'ok':
    print ('Message published successfully')
else:
    print ('Failed to publish message:', response)
ws.close()
