.. _rktoolkit.models:

rktoolkit.models package
========================

.. _rktoolkit.models.graph:

Graph Modules
-------------

.. automodule:: rktoolkit.models.graph
   :members:
   :undoc-members:

.. _rktoolkit.models.linkage:

Linkage functions
-----------------

.. automodule:: rktoolkit.models.linkage
   :members:
   :undoc-members:

.. _rktoolkit.models.functions:

Functions for Manipulating Models
---------------------------------

.. automodule:: rktoolkit.models.functions
   :members:
   :undoc-members:

.. _rktoolkit.models.rkmodel:

RKModel Module
--------------

.. automodule:: rktoolkit.models.rkmodel
   :members:
   :undoc-members:

.. _rktoolkit.models.pipeline:

RK-Pipeline Module
------------------
An RK-Pipeline, is the process of moving between an NxM Tensor into
an RK-Model and visualized as an RK-Diagram. The benefits of an RK-Model over
traditional models are numerous, including the fact that an RK-Model is a
compact representation that perserves topology and encodes structure in high
dimensional data. The following section will focus on the RK Toolkit library
and go through the various transformation steps from an NxM Tensor into a
visualized RK-Diagram. This novel approach toward topological data analysis
is extendable through the SDK hosted on github.com/andorsk/rk_toolkit. Examples
of how to use the toolkit are also hosted there.

There are a few novel concepts and objects within the pipeline as well as
the entire pipeline itself, by virtue of it's components and ordering, that
provide a new and novel approach toward topological data analysis.

An RK-Pipeline is a unidirectonal pipeline that builds an RK-Model from a
incoming dataset.

Figure below shows a diagram with the RK-Pipeline specified

.. image:: ../../imgs/rk-flow.png
   :width: 600

Composed together are the following steps:

1. Preprocess Steps
2. Localization Algorithm
3. Hierarchical Feature Extraction Nodes
4. Filter Functions
5. Linkage Functions

Composed together, these component synethesize an RK-Model. 

.. automodule:: rktoolkit.models.pipeline 
   :members:
   :undoc-members:

Module contents
---------------

.. automodule:: rktoolkit.models
   :members:
   :undoc-members:
   :show-inheritance: