import websocket, base64, json

# If set enableTLS to true, your have to set tlsEnabled to true in conf/websocket.conf.
enable_TLS = False
scheme = 'ws'
if enable_TLS:
    scheme = 'wss'

TOPIC = scheme + '://192.168.1.181:8080/ws/v2/reader/persistent/public/default/my-topic'
ws = websocket.create_connection(TOPIC)

while True:
    msg = json.loads(ws.recv())
    if not msg: break

    print( "Received: {} - payload: {}".format(msg, base64.b64decode(msg['payload'])))

    # Acknowledge successful processing
    ws.send(json.dumps({'messageId' : msg['messageId']}))

ws.close()
