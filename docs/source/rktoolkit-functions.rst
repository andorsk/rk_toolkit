R-K Utility Functions
=====================

**Range Filter**
++++++++++++++++

.. autoclass:: rktoolkit.functions.filters.RangeFilter
    :members:
    :undoc-members:

**Leaf Linker**
+++++++++++++++

.. autoclass:: rktoolkit.functions.linkers.SimpleChildLinker
    :members:
    :undoc-members: 

**Localization Functions**
++++++++++++++++++++++++++

.. automodule:: rktoolkit.functions.localizers

**Circular Visualizer**
+++++++++++++++++++++++

Cicular Visualizer Makes an almost "Mandlebot" like visualization
of the RKModel.

**How it works:** based on the center, and relative number of children nodes,
it expands outward using a circular pattern. As the expansion continues,
children birth more children in circular patterns.

The distance and sizes of of the node between each parent -> child in the visualization
decreases each iteration.

You can override any particular value using the attributes of a node.

.. automodule:: rktoolkit.visualizers.circular

