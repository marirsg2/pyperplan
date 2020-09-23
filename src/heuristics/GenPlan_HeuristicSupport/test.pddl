(define (problem logistics)
(:domain logistics-strips)
(:objects
  c0 c1   - TYPcity
  l13 l01 l03 l02 l10 l11 l12 l00   - TYPlocation
  t1 t0   - TYPtruck
  a0   - TYPairplane
  p0   - TYPpackage
)
(:init
(airplane a0)
(airport l00)
(airport l10)
(at a0 l00)
(at t0 l00)
(at t1 l10)
(city c0)
(city c1)
(in-city l00 c0)
(in-city l01 c0)
(in-city l02 c0)
(in-city l03 c0)
(in-city l10 c1)
(in-city l11 c1)
(in-city l12 c1)
(in-city l13 c1)
(in p0 a0)
(location l00)
(location l01)
(location l02)
(location l03)
(location l10)
(location l11)
(location l12)
(location l13)
(obj p0)
(truck t0)
(truck t1)
)
(:goal
(at p0 l13)
)
)