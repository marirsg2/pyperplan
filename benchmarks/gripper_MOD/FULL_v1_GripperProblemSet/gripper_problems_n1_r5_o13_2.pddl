


(define (problem gripper-1-5-13)
(:domain gripper-strips)
(:objects robot1 - robot
rgripper1 lgripper1 - gripper
room1 room2 room3 room4 room5 - room
ball1 ball2 ball3 ball4 ball5 ball6 ball7 ball8 ball9 ball10 ball11 ball12 ball13 - ball)
(:init
(at-robby robot1 room5)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at ball1 room5)
(at ball2 room1)
(at ball3 room1)
(at ball4 room2)
(at ball5 room2)
(at ball6 room1)
(at ball7 room2)
(at ball8 room4)
(at ball9 room3)
(at ball10 room4)
(at ball11 room4)
(at ball12 room4)
(at ball13 room2)
)
(:goal
(and
(at ball1 room3)
(at ball2 room1)
(at ball3 room4)
(at ball4 room2)
(at ball5 room5)
(at ball6 room4)
(at ball7 room3)
(at ball8 room5)
(at ball9 room3)
(at ball10 room2)
(at ball11 room4)
(at ball12 room1)
(at ball13 room4)
)
)
)


