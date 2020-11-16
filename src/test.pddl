(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  rgripper1 lgripper1   - gripper
  room1 room5 room2 room4 room3   - room
  ball5 ball1 ball2 ball3 ball4   - ball
)
(:init
(at ball1 room2)
(at ball2 room3)
(at ball3 room4)
(at ball4 room5)
(at ball5 room1)
(at-robby robot1 room5)
(free robot1 lgripper1)
(free robot1 rgripper1)
)
(:goal
(at ball2 room3)
(at ball5 room1)
(at ball3 room4)
(at ball4 room5)
(at ball1 room2)
)
)