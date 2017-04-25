"""
Copyright (C) 2017 Open Source Robotics Foundation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import math

from point import Point


class Circle(object):

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @classmethod
    def from_points_and_radius(cls, start_point, end_point, radius):
        # the path between start_point and end_point is walked in counter_clockwise direction
        # angular length between start_point and end_point is <= 180
        if start_point == end_point:
            raise ValueError("start_point and end_point must be different")
        d = start_point.distance_to(end_point)
        a = math.sqrt(radius ** 2 - (d / 2) ** 2)
        vector = end_point - start_point
        orthonormal_vector = vector.orthonormal_vector()
        mid_point = start_point.mid_point(end_point)
        center = mid_point + (orthonormal_vector * a)
        return Circle(center, radius)

    def __eq__(self, other):
        return self.center == other.center and self.radius == other.radius

    def __hash__(self):
        return hash((self.center, self.radius))

    def almost_equal_to(self, other):
        return self.center.almost_equal_to(other.center, 5) and abs(self.radius - other.radius) < 1e-5

    def intersection(self, other):
        d = (other.center - self.center).norm()
        r1 = self.radius
        r2 = other.radius
        if d == 0 and r1 == r2:
            return [self]
        if d == 0 and r1 != r2:
            return []
        if (d > self.radius + other.radius) or (d < abs(self.radius - other.radius)):
            return []
        if d == self.radius + other.radius:
            return [self.center + (other.center - self.center) * (self.radius / d)]
        if d == abs(self.radius - other.radius):
            if self.radius > other.radius:
                return [self.center + (other.center - self.center) * (self.radius / d)]
            if self.radius < other.radius:
                return [other.center + (self.center - other.center) * (other.radius / d)]
        if max(r1, r2) <= d < self.radius + other.radius:
            a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
            h = math.sqrt(r1 ** 2 - a ** 2)
            auxiliary_point = self.center + (other.center - self.center) * (a / d)
            p1 = auxiliary_point + (other.center - self.center).orthogonal_vector() * (h / d)
            p2 = auxiliary_point - (other.center - self.center).orthogonal_vector() * (h / d)
            return [p1, p2]
        if abs(r1 - r2) < d < max(r1, r2):
            if r1 > r2:
                a = (r1 ** 2 - r2 ** 2 - d ** 2) / (2 * d)
                h = math.sqrt(r2 ** 2 - a ** 2)
                auxiliary_point = other.center + (other.center - self.center) * (a / d)
                p1 = auxiliary_point + (other.center - self.center).orthogonal_vector() * (h / d)
                p2 = auxiliary_point - (other.center - self.center).orthogonal_vector() * (h / d)
                return [p1, p2]
            if r2 > r1:
                a = (r2 ** 2 - r1 ** 2 - d ** 2) / (2 * d)
                h = math.sqrt(r1 ** 2 - a ** 2)
                auxiliary_point = self.center + (self.center - other.center) * (a / d)
                p1 = auxiliary_point + (self.center - other.center).orthogonal_vector() * (h / d)
                p2 = auxiliary_point - (self.center - other.center).orthogonal_vector() * (h / d)
                return [p1, p2]
