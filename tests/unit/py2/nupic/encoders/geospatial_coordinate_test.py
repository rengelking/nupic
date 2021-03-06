#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import numpy as np
import unittest

from nupic.encoders.base import defaultDtype
from nupic.encoders.geospatial_coordinate import (
  GeospatialCoordinateEncoder)

# Disable warnings about accessing protected members
# pylint: disable=W0212



class GeospatialCoordinateEncoderTest(unittest.TestCase):
  """Unit tests for GeospatialCoordinateEncoder class"""

  def testCoordinateForPosition(self):
    scale = 30  # meters
    encoder = GeospatialCoordinateEncoder(scale, 60)
    coordinate = encoder.coordinateForPosition(
      -122.229194, 37.486782
    )
    self.assertEqual(coordinate.tolist(), [-453549, 150239])


  def testCoordinateForPositionOrigin(self):
    scale = 30  # meters
    encoder = GeospatialCoordinateEncoder(scale, 60)
    coordinate = encoder.coordinateForPosition(0, 0)
    self.assertEqual(coordinate.tolist(), [0, 0])


  def testRadiusForSpeed(self):
    scale = 30  # meters
    timestep = 60  #seconds
    speed = 50  # meters per second
    encoder = GeospatialCoordinateEncoder(scale, timestep)
    radius = encoder.radiusForSpeed(speed)
    self.assertEqual(radius, 75)


  def testRadiusForSpeed0(self):
    scale = 30  # meters
    timestep = 60  #seconds
    speed = 0  # meters per second
    n = 999
    w = 27
    encoder = GeospatialCoordinateEncoder(scale, timestep, n=n, w=w)
    radius = encoder.radiusForSpeed(speed)
    self.assertEqual(radius, 3)


  def testRadiusForSpeedInt(self):
    """Test that radius will round to the nearest integer"""
    scale = 30  # meters
    timestep = 62  #seconds
    speed = 25  # meters per second
    encoder = GeospatialCoordinateEncoder(scale, timestep)
    radius = encoder.radiusForSpeed(speed)
    self.assertEqual(radius, 38)


  def testEncodeIntoArray(self):
    scale = 30  # meters
    timestep = 60  #seconds
    speed = 2.5  # meters per second
    encoder = GeospatialCoordinateEncoder(scale, timestep,
                                          n=999,
                                          w=25)
    encoding1 = encode(encoder, -122.229194, 37.486782, speed)
    encoding2 = encode(encoder, -122.229294, 37.486882, speed)
    encoding3 = encode(encoder, -122.229294, 37.486982, speed)

    overlap1 = overlap(encoding1, encoding2)
    overlap2 = overlap(encoding1, encoding3)

    self.assertTrue(overlap1 > overlap2)



def encode(encoder, longitude, latitude, speed):
  output = np.zeros(encoder.getWidth(), dtype=defaultDtype)
  encoder.encodeIntoArray((longitude, latitude, speed), output)
  return output

def overlap(sdr1, sdr2):
  assert sdr1.size == sdr2.size
  return float((sdr1 & sdr2).sum()) / sdr1.sum()



if __name__ == "__main__":
  unittest.main()
