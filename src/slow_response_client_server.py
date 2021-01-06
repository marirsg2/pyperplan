import socket

def start_server ():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # "127.0.0.1"
    s.bind(('localhost', 1800))
    print('Starting')
    print("REMEMBER TO START CLIENT FIRST, else you may have to restart computer")
    print("REMEMBER TO pass in arguments like ./run-deepplan.sh blocksworld test.pddl")
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
        # clientsocket.send(bytes("(define (problem train5) (:domain blocksworld) (:objects a b - block) (:init (arm-empty) (clear b) (on-table a) (on b a)) (:goal (and (on a b))))\n", "utf-8"))
        clientsocket.send(bytes("(define (problem gripper) (:domain gripper-strips) (:objects   robot1   - robot   rgripper1 lgripper1   - gripper   room8 room5 room10 room9 room3 room4 room6 room2 room1 room7 room13 room11   - room   ball8 ball9 ball15 ball1 ball3 ball14 ball4 ball7 ball10 ball13 ball5 ball12 ball11 ball6 ball2   - ball ) (:init (at ball1 room2) (at ball10 room9) (at ball11 room11) (at ball12 room4) (at ball13 room6) (at ball14 room3) (at ball15 room10) (at ball2 room9) (at ball3 room11) (at ball4 room13) (at ball5 room1) (at ball6 room7) (at ball7 room5) (at ball8 room11) (at ball9 room3) (at-robby robot1 room8) (free robot1 lgripper1) (free robot1 rgripper1) ) (:goal (at ball12 room9) (at ball1 room8) (at ball14 room14) (at ball13 room1) (at ball7 room8) (at ball4 room3) (at ball10 room14) (at ball5 room6) (at ball11 room11) (at ball9 room11) (at ball6 room12) (at ball8 room8) (at ball15 room12) (at ball2 room11) (at ball3 room12) ) )\n", "utf-8"))
        print('  Problem sent')
        print('  Receiving new generalized state')
        msg = clientsocket.recv(100000).decode("utf-8")
        while not msg.endswith("\""): #yup thats a lousy end char, but so it is
            msg += clientsocket.recv(100000).decode("utf-8")
        print('  Received', msg)
    clientsocket.close()
    return None

start_server()
