(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  lgripper1 rgripper1   - gripper
  room4 room3 room1 room2   - room
  ball1 ball4 ball2 ball5 ball3   - ball
)
(:init
(at-robby robot1 room2)
(at ball1 room1)
(at ball2 room3)
(at ball3 room4)
(at ball4 room4)
(at ball5 room2)
(free robot1 lgripper1)
(free robot1 rgripper1)
)
(:goal
(at ball5 room2)
(at ball3 room5)
(at ball4 room1)
(at ball2 room5)
(at ball1 room3)
)
)