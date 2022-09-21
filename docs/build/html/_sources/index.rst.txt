.. rktoolkit documentation master file, created by
   sphinx-quickstart on Sun May 16 14:42:05 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. _index:

RK-Toolkit Documentation
=====================================

RK-Toolkit is the toolkit used for transforming an NxM Tensor into a RK-Model that is visualized as an RK-Diagram. The benefits of an RK-Model over
traditional models are numerous, including the fact that an RK-Model is a compact representation that perserves topology and encodes structure in high
dimensional data. This documentation will focus on the RK Toolkit library and go through the various transformation steps from an NxM Tensor into a
visualized RK-Diagram. This novel approach toward topological data analysis is extendable through the SDK hosted `Here <github.com/andorsk/rk_toolkit>`_. Examples
of how to use the toolkit are also hosted there.
  

.. toctree::
   :hidden:
   :maxdepth: 1
   
   
   rktoolkit.rst


.. toctree::
   :hidden:
   :maxdepth: 1

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Readme File
===========

Example Pipeline
======================

.. code-block:: python

   example_pipeline = RKPipeline(preprocess_nodes=[MinMaxNormalizerNode()],
                                 localization_algorithm=MaxLocalizer(),
                                 hierarchical_embedding_nodes= [
                                    {
                                       "HFeatureExtractor1": HierarchicalFeatureExtractor1()
                                    }
                                 ],
                                 filter_functions=[
                                    {
                                       "HFeatureExtractor1" :
                                       {
                                             'range_measure': StaticFilter(min=.2, max=.8),
                                             'max_measure': StaticFilter(min=0, max=1)
                                       }
                                    }
                                 ], # question: how to define which limits for which measure. Each filter and linkage has to be BY CLUSTER
                                 linkage_function=SimpleLinkage(threshold=.8))
                                 example_pipeline.build()
   example_pipeline.fit(X)
   rk_model = example_pipeline.transform(X)
   rk_models.append(rk_model)

   visualizer = RKModelVisualizer(method="circular")
   visualizer.build(rk_models) # build requires a list of rk_models
   visualizer.show()
