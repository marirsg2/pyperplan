


(define (problem gripper-1-2-5)
(:domain gripper-strips)
(:objects robot1 - robot
rgripper1 lgripper1 - gripper
room1 room2 - room
ball1 ball2 ball3 ball4 ball5 - ball)
(:init
(at-robby robot1 room1)
(free rgripper1 robot1)
(free lgripper1 robot1)
(at ball1 room1)
(at ball2 room1)
(at ball3 room2)
(at ball4 room1)
(at ball5 room2)
)
(:goal
(and
(at ball1 room2)
(at ball2 room1)
(at ball3 room2)
(at ball4 room2)
(at ball5 room1)
)
)
)


