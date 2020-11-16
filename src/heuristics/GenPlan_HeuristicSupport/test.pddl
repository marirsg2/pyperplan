(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  rgripper1 lgripper1   - gripper
  room3 room5 room4   - room
  ball5 ball4 ball2 ball1 ball3   - ball
)
(:init
(at-robby robot1 room3)
(at ball1 room3)
(at ball2 room3)
(at ball3 room5)
(at ball4 room4)
(at ball5 room5)
(free robot1 lgripper1)
(free robot1 rgripper1)
)
(:goal
(at ball1 room4)
(at ball2 room4)
(at ball3 room5)
(at ball5 room5)
(at ball4 room3)
)
)