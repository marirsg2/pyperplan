(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  lgripper1 rgripper1   - gripper
  room8 room13 room51 room20 room7 room25   - room
  ball2 ball5 ball4 ball3 ball1   - ball
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