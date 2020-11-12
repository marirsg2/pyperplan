


(define (problem gripper-1-5-5)
(:domain gripper-strips)
(:objects robot1 - robot
rgripper1 lgripper1 - gripper
room1 room2 room3 room4 room5 - room
ball1 ball2 ball3 ball4 ball5 - ball)
(:init
(at-robby robot1 room1)
(free rgripper1 robot1)
(free lgripper1 robot1)
(at ball1 room1)
(at ball2 room2)
(at ball3 room2)
(at ball4 room3)
(at ball5 room4)
)
(:goal
(and
(at ball1 room2)
(at ball2 room3)
(at ball3 room4)
(at ball4 room5)
(at ball5 room1)
)
)
)


