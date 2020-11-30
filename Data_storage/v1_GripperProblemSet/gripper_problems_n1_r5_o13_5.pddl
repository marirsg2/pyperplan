


(define (problem gripper-1-5-13)
(:domain gripper-strips)
(:objects robot1 - robot
rgripper1 lgripper1 - gripper
room1 room2 room3 room4 room5 - room
ball1 ball2 ball3 ball4 ball5 ball6 ball7 ball8 ball9 ball10 ball11 ball12 ball13 - ball)
(:init
(at-robby robot1 room4)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at ball1 room4)
(at ball2 room5)
(at ball3 room3)
(at ball4 room5)
(at ball5 room4)
(at ball6 room4)
(at ball7 room5)
(at ball8 room3)
(at ball9 room5)
(at ball10 room5)
(at ball11 room1)
(at ball12 room5)
(at ball13 room2)
)
(:goal
(and
(at ball1 room1)
(at ball2 room4)
(at ball3 room5)
(at ball4 room4)
(at ball5 room4)
(at ball6 room3)
(at ball7 room2)
(at ball8 room5)
(at ball9 room4)
(at ball10 room5)
(at ball11 room2)
(at ball12 room1)
(at ball13 room1)
)
)
)


