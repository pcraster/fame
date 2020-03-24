import numpy






class Values(object):
  def __init__(self, nr_objects, values):

    self.iter_idx = 0

    self.values = values
    self.nr_objects = nr_objects



  def __iter__(self):
        return self

  def __next__(self):
        if self.iter_idx == self.nr_objects:
            raise StopIteration

        values = self.values[self.iter_idx]
        self.iter_idx += 1

        return values


  def __getitem__(self, index):
    try:
      idx = index[0]
    except Exception as e:
      idx = index
    if idx < 0 or idx > self.nr_objects:
      raise IndexError

    return self.values[index]


  def __setitem__(self, index, value):
    try:
      idx = index[0]
    except Exception as e:
      idx = index

    if idx < 0 or idx > self.nr_objects:
      raise IndexError

    self.values[index] = value



  def __repr__(self):
    for v in self.values:
      print(v)
    return ''
