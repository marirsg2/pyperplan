(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  lgripper1 rgripper1   - gripper
  room1 room4 room3 room5 room2   - room
  ball1 ball3 ball5 ball2 ball4   - ball
)
(:init
(at ball1 room4)
(at ball2 room5)
(at ball3 room2)
(at ball4 room1)
(at ball5 room3)
(at-robby robot1 room2)
(free lgripper1 robot1)
(free rgripper1 robot1)
)
(:goal
(at ball2 room3)
(at ball4 room5)
(at ball3 room4)
(at ball5 room1)
(at ball1 room2)
)
)