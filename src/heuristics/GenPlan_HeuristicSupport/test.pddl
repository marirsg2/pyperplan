(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  rgripper1 lgripper1   - gripper
  room4 room3 room2 room5   - room
  ball8 ball5 ball9 ball3 ball6 ball1 ball4 ball2 ball7   - ball
)
(:init
(at-robby robot1 room2)
(at ball1 room5)
(at ball2 room5)
(at ball4 room4)
(at ball6 room5)
(at ball7 room3)
(at ball8 room5)
(at ball9 room2)
(carry ball3 rgripper1)
(carry ball5 lgripper1)
)
(:goal
(at ball9 room4)
(at ball4 room5)
(at ball5 room4)
(at ball6 room3)
(at ball1 room4)
(at ball7 room4)
(at ball2 room5)
(at ball8 room3)
(at ball3 room2)
)
)