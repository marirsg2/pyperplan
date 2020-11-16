(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  rgripper1 lgripper1   - gripper
  room3 room1 room4   - room
  ball1 ball2 ball3 ball5 ball4   - ball
)
(:init
(at-robby robot1 room4)
(at ball1 room4)
(at ball3 room1)
(at ball4 room1)
(at ball5 room3)
(carry ball2 lgripper1)
(free robot1 rgripper1)
)
(:goal
(at ball1 room5)
(at ball3 room1)
(at ball4 room1)
(at ball2 room5)
(at ball5 room3)
)
)