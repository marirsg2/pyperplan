(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  rgripper1 lgripper1   - gripper
  room4 room5 room3   - room
  ball4 ball2 ball3 ball1 ball5   - ball
)
(:init
(at-robby robot1 room4)
(at ball1 room4)
(at ball4 room3)
(at ball5 room5)
(carry ball2 rgripper1)
(carry ball3 lgripper1)
)
(:goal
(at ball2 room4)
(at ball5 room5)
(at ball1 room4)
(at ball4 room3)
(at ball3 room3)
)
)