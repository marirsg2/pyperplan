


(define (problem gripper-1-2-100)
(:domain gripper-strips)
(:objects robot1 - robot
rgripper1 lgripper1 - gripper
room1 room2 - room
ball1 ball2 ball3 ball4 ball5 ball6 ball7 ball8 ball9 ball10 ball11 ball12 ball13 ball14 ball15 ball16 ball17 ball18 ball19 ball20 ball21 ball22 ball23 ball24 ball25 ball26 ball27 ball28 ball29 ball30 ball31 ball32 ball33 ball34 ball35 ball36 ball37 ball38 ball39 ball40 ball41 ball42 ball43 ball44 ball45 ball46 ball47 ball48 ball49 ball50 ball51 ball52 ball53 ball54 ball55 ball56 ball57 ball58 ball59 ball60 ball61 ball62 ball63 ball64 ball65 ball66 ball67 ball68 ball69 ball70 ball71 ball72 ball73 ball74 ball75 ball76 ball77 ball78 ball79 ball80 ball81 ball82 ball83 ball84 ball85 ball86 ball87 ball88 ball89 ball90 ball91 ball92 ball93 ball94 ball95 ball96 ball97 ball98 ball99 ball100 - ball)
(:init
(at-robby robot1 room2)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at ball1 room2)
(at ball2 room2)
(at ball3 room2)
(at ball4 room1)
(at ball5 room2)
(at ball6 room1)
(at ball7 room2)
(at ball8 room1)
(at ball9 room2)
(at ball10 room1)
(at ball11 room1)
(at ball12 room1)
(at ball13 room1)
(at ball14 room1)
(at ball15 room1)
(at ball16 room1)
(at ball17 room2)
(at ball18 room1)
(at ball19 room2)
(at ball20 room1)
(at ball21 room2)
(at ball22 room2)
(at ball23 room2)
(at ball24 room1)
(at ball25 room1)
(at ball26 room1)
(at ball27 room1)
(at ball28 room1)
(at ball29 room2)
(at ball30 room2)
(at ball31 room2)
(at ball32 room2)
(at ball33 room2)
(at ball34 room2)
(at ball35 room1)
(at ball36 room2)
(at ball37 room2)
(at ball38 room2)
(at ball39 room2)
(at ball40 room2)
(at ball41 room2)
(at ball42 room1)
(at ball43 room1)
(at ball44 room1)
(at ball45 room1)
(at ball46 room1)
(at ball47 room2)
(at ball48 room2)
(at ball49 room1)
(at ball50 room1)
(at ball51 room1)
(at ball52 room1)
(at ball53 room1)
(at ball54 room2)
(at ball55 room2)
(at ball56 room1)
(at ball57 room1)
(at ball58 room2)
(at ball59 room1)
(at ball60 room1)
(at ball61 room1)
(at ball62 room2)
(at ball63 room2)
(at ball64 room1)
(at ball65 room2)
(at ball66 room2)
(at ball67 room2)
(at ball68 room2)
(at ball69 room1)
(at ball70 room2)
(at ball71 room1)
(at ball72 room1)
(at ball73 room2)
(at ball74 room1)
(at ball75 room2)
(at ball76 room1)
(at ball77 room2)
(at ball78 room1)
(at ball79 room1)
(at ball80 room1)
(at ball81 room1)
(at ball82 room1)
(at ball83 room2)
(at ball84 room1)
(at ball85 room1)
(at ball86 room1)
(at ball87 room2)
(at ball88 room1)
(at ball89 room2)
(at ball90 room2)
(at ball91 room1)
(at ball92 room1)
(at ball93 room2)
(at ball94 room1)
(at ball95 room1)
(at ball96 room2)
(at ball97 room2)
(at ball98 room1)
(at ball99 room1)
(at ball100 room1)
)
(:goal
(and
(at ball1 room1)
(at ball2 room1)
(at ball3 room2)
(at ball4 room2)
(at ball5 room2)
(at ball6 room1)
(at ball7 room1)
(at ball8 room2)
(at ball9 room1)
(at ball10 room1)
(at ball11 room1)
(at ball12 room2)
(at ball13 room1)
(at ball14 room2)
(at ball15 room1)
(at ball16 room2)
(at ball17 room2)
(at ball18 room2)
(at ball19 room2)
(at ball20 room1)
(at ball21 room2)
(at ball22 room1)
(at ball23 room1)
(at ball24 room2)
(at ball25 room1)
(at ball26 room2)
(at ball27 room1)
(at ball28 room1)
(at ball29 room1)
(at ball30 room1)
(at ball31 room2)
(at ball32 room1)
(at ball33 room2)
(at ball34 room1)
(at ball35 room1)
(at ball36 room2)
(at ball37 room1)
(at ball38 room1)
(at ball39 room2)
(at ball40 room2)
(at ball41 room1)
(at ball42 room2)
(at ball43 room1)
(at ball44 room2)
(at ball45 room1)
(at ball46 room1)
(at ball47 room1)
(at ball48 room1)
(at ball49 room1)
(at ball50 room1)
(at ball51 room2)
(at ball52 room2)
(at ball53 room2)
(at ball54 room1)
(at ball55 room1)
(at ball56 room1)
(at ball57 room2)
(at ball58 room2)
(at ball59 room1)
(at ball60 room1)
(at ball61 room2)
(at ball62 room2)
(at ball63 room1)
(at ball64 room2)
(at ball65 room2)
(at ball66 room1)
(at ball67 room2)
(at ball68 room1)
(at ball69 room1)
(at ball70 room1)
(at ball71 room2)
(at ball72 room2)
(at ball73 room2)
(at ball74 room1)
(at ball75 room1)
(at ball76 room1)
(at ball77 room1)
(at ball78 room1)
(at ball79 room1)
(at ball80 room1)
(at ball81 room2)
(at ball82 room2)
(at ball83 room1)
(at ball84 room1)
(at ball85 room2)
(at ball86 room2)
(at ball87 room1)
(at ball88 room2)
(at ball89 room1)
(at ball90 room2)
(at ball91 room2)
(at ball92 room1)
(at ball93 room1)
(at ball94 room2)
(at ball95 room2)
(at ball96 room1)
(at ball97 room1)
(at ball98 room1)
(at ball99 room2)
(at ball100 room2)
)
)
)


