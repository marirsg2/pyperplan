(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  rgripper1 lgripper1   - gripper
  room2 room1   - room
  ball3 ball2 ball5 ball4 ball1   - ball
)
(:init
(at ball1 room2)
(at ball2 room1)
(at ball3 room2)
(at ball4 room2)
(at ball5 room1)
(at-robby robot1 room1)
(free lgripper1 robot1)
(free rgripper1 robot1)
)
(:goal
(at ball5 room1)
(at ball2 room1)
(at ball4 room2)
(at ball1 room2)
(at ball3 room2)
)
)