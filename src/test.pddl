(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  rgripper1 lgripper1   - gripper
  room1 room3 room4 room2   - room
  ball5 ball1 ball4 ball3 ball2   - ball
)
(:init
(at ball1 room1)
(at ball2 room2)
(at ball3 room2)
(at ball4 room3)
(at ball5 room4)
(at-robby robot1 room1)
(free robot1 lgripper1)
(free robot1 rgripper1)
)
(:goal
(at ball2 room3)
(at ball5 room1)
(at ball1 room2)
(at ball4 room5)
(at ball3 room4)
)
)