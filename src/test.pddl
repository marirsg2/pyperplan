(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  rgripper1 lgripper1   - gripper
  room7 room8 room4 room5 room9 room1 room3   - room
  ball5 ball3 ball2 ball6 ball4 ball7 ball1   - ball
)
(:init
(at ball1 room4)
(at ball2 room9)
(at ball3 room8)
(at ball4 room7)
(at ball5 room3)
(at ball6 room1)
(at ball7 room5)
(at-robby robot1 room5)
(free robot1 lgripper1)
(free robot1 rgripper1)
)
(:goal
(at ball4 room7)
(at ball3 room8)
(at ball6 room1)
(at ball5 room3)
(at ball1 room4)
(at ball7 room5)
(at ball2 room9)
)
)