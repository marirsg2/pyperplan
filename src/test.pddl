(define (problem gripper)
(:domain gripper-strips)
(:objects
  robot1   - robot
  lgripper1 rgripper1   - gripper
  room4 room9 room2 room5 room1 room6 room10 room3   - room
  ball4 ball8 ball9 ball5 ball1 ball6 ball7 ball3 ball10 ball2   - ball
)
(:init
(at ball1 room2)
(at ball10 room10)
(at ball2 room3)
(at ball3 room4)
(at ball4 room5)
(at ball5 room2)
(at ball6 room6)
(at ball7 room2)
(at ball8 room1)
(at ball9 room9)
(at-robby robot1 room1)
(free robot1 lgripper1)
(free robot1 rgripper1)
)
(:goal
(at ball7 room2)
(at ball8 room1)
(at ball2 room3)
(at ball9 room9)
(at ball10 room10)
(at ball5 room2)
(at ball3 room4)
(at ball4 room5)
(at ball1 room2)
(at ball6 room6)
)
)