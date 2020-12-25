import socket

def start_server ():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # "127.0.0.1"
    s.bind(('localhost', 1800))
    print('Starting')
    s.listen(1)
    print('  Waiting for client')

    #while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"  Connection from {address} has been established.")
    print('  Sending OK')
    clientsocket.send(bytes("ok\n","utf-8"))
    print('  Sent OK')
    
    #msg = clientsocket.recv(10000)
    #print('Received', msg)

    for i in range(5):
        print('Sending problem')
        clientsocket.send(bytes("(define (problem train5) (:domain blocksworld) (:objects a b - block) (:init (arm-empty) (clear b) (on-table a) (on b a)) (:goal (and (on a b))))\n", "utf-8"))
        print('  Problem sent')
        print('  Receiving new generalized state')
        msg = clientsocket.recv(100000).decode("utf-8")
        while not msg.endswith("\""): #yup thats a lousy end char, but so it is
            msg += clientsocket.recv(100000).decode("utf-8")
        print('  Received', msg)
    clientsocket.close()
    return None

start_server()
