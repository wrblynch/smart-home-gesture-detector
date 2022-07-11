from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np

"""
A class to enable a simple step counter
"""
class Pedometer:
  """
  Encapsulated class attributes (with default values)
  """
  __steps = 0        # the current step count
  __jumps = 0
  __l1 = None        # CircularList containing L1-norm
  __filtered = None  # CircularList containing filtered signal
  __num_samples = 1500  # The length of data maintained
  __new_samples = 512  # How many new samples exist to process
  __fs = 300           # Sampling rate in Hz
  __b = None         # Low-pass coefficients
  __a = None         # Low-pass coefficients
  __thresh_walk_low = 2   # Threshold from Tutorial 2
  __thresh_walk_high = 30 # Threshold from Tutorial 2
  __thresh_jump_low = 30
  __thresh_jump_high = 100
  """
  Initialize the class instance
  """
  def __init__(self, num_samples, fs, data=None):
    self.__steps = 0
    self.__jumps = 0
    self.__num_samples = num_samples
    self.__fs = fs
    self.__l1 = CircularList(data, num_samples)
    self.__filtered = CircularList([], num_samples)
    self.__b, self.__a = filt.create_filter(3, 1, "lowpass", fs)

  """
  Add new samples to the data buffer
  Handles both integers and vectors!
  """
  def add(self, ax, ay, az):
    l1 = filt.l1_norm(ax, ay, az)
    if isinstance(ax, int):
      num_add = 1
    else:
      num_add = len(ax)
      l1 = l1.tolist()

    self.__l1.add(l1)
    self.__new_samples += num_add

  """
  Process the new data to update step count
  """
  def process(self):
    # Grab only the new samples into a NumPy array
    x = np.array(self.__l1[ -self.__new_samples: ])


    dt = filt.detrend(x)  # Detrend the Signal
    grad = filt.gradient(dt)
    ma = filt.moving_average(grad, 50)
    b, a = filt.create_filter(3, 1, "lowpass", self.__fs)  # Low-pass Filter Design
    lp = filt.filter(b, a, ma)  # Low-pass Filter Signal


    # Store the filtered data
    self.__filtered.add(lp.tolist())

    # Count the number of peaks in the filtered data
    step_count, peaks = filt.count_peaks(lp, self.__thresh_walk_low, self.__thresh_walk_high)

    jump_count, peaks = filt.count_peaks(lp, self.__thresh_jump_low, self.__thresh_jump_high)

    # Update the step count and reset the new sample count
    self.__steps += step_count
    self.__jumps += jump_count
    self.__new_samples = 0

    # Return the step count, peak locations, and filtered data
    return self.__steps, self.__jumps, peaks, np.array(self.__filtered)

  """
  Clear the data buffers and step count
  """
  def reset(self):
    self.__steps = 0
    self.__l1.clear()