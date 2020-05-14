Examples
========

some brief description how to build up a dataset...


You usually create a new dataset in the initial section:

.. code-block:: python



  def initial(self):

    self.luemem = LueMemory(self.nrTimeSteps())

    dataset_name = os.path.join('example.lue')
    self.luemem.open(dataset_name)


Creating a new phenomenon

.. code-block:: python:

   self.household = self.luemem.add_phenomenon('household', locations.nr_items)






Adding a property set to a phenomenon:

.. code-block:: python:

   self.household.add_property_set('frontdoor', locations, fame.TimeDomain.dynamic)

Afterwards you can add properties:

.. code-block:: python:


   self.household.frontdoor.add_property('propensity')


















