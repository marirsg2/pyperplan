


(define (problem gripper-1-5-5)
(:domain gripper-strips)
(:objects robot1 - robot
rgripper1 lgripper1 - gripper
room1 room2 - room
ball1 ball2 ball3 ball4 ball5 ball6 ball7 ball8 ball9 ball10 - ball)
(:init
(at-robby robot1 room1)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at ball1 room1)
(at ball2 room1)
(at ball3 room1)
(at ball4 room1)
(at ball5 room1)
(at ball6 room1)
(at ball7 room1)
(at ball8 room1)
(at ball9 room1)
(at ball10 room1)
)
(:goal
(and
(at ball1 room2)
(at ball2 room2)
(at ball3 room2)
(at ball4 room2)
(at ball5 room2)
(at ball6 room2)
(at ball7 room2)
(at ball8 room2)
(at ball9 room2)
(at ball10 room2)
)
)
)
