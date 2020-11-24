


(define (problem gripper-1-5-5)
(:domain gripper-strips)
(:objects robot1 - robot
rgripper1 lgripper1 - gripper
room1 room2 room3 room4 room5 room6 room7 room8 room9 room10 - room
ball1 ball2 ball3 ball4 ball5 ball6 ball7 ball8 ball9 ball10 - ball)
(:init
(at-robby robot1 room1)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at ball1 room1)
(at ball2 room2)
(at ball3 room2)
(at ball4 room3)
(at ball5 room4)
(at ball6 room2)
(at ball7 room6)
(at ball8 room10)
(at ball9 room5)
(at ball10 room7)
)
(:goal
(and
(at ball1 room2)
(at ball2 room3)
(at ball3 room4)
(at ball4 room5)
(at ball5 room2)
(at ball6 room6)
(at ball7 room2)
(at ball8 room1)
(at ball9 room9)
(at ball10 room10)
)
)
)
