(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  rgripper1 lgripper1   - gripper
  room25 room8 room13 room20 room7 room51   - room
  ball4 ball2 ball1 ball5 ball3   - ball
)
(:init
(at-robby robot1 room20)
(at ball1 room51)
(at ball2 room13)
(at ball3 room25)
(at ball4 room7)
(at ball5 room8)
(free robot1 lgripper1)
(free robot1 rgripper1)
)
(:goal
(at ball1 room59)
(at ball3 room28)
(at ball5 room17)
(at ball2 room2)
(at ball4 room51)
)
)