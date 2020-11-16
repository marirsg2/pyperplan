(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  rgripper1 lgripper1   - gripper
  room2 room1 room4   - room
  ball4 ball2 ball5 ball1 ball3   - ball
)
(:init
(at ball1 room1)
(at ball2 room4)
(at ball4 room1)
(at ball5 room4)
(at-robby robot1 room2)
(carry ball3 rgripper1)
(free robot1 lgripper1)
)
(:goal
(at ball4 room5)
(at ball2 room3)
(at ball5 room1)
(at ball3 room4)
(at ball1 room2)
)
)