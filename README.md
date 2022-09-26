# RK Toolkit

Standard package and toolkit for RK Diagrams.

#### Installation
``` sh
python -m pip install .
```

#### Using a module

**TODO: Check FIXES**
To use a module:
``` sh
from rktoolkit.visualizers.visualizer import RKModelVisualizer
from rktoolkit.pipeline import RKPipeline

# Make filters and get structural graph using Filters, Linkers and Graph modules
pipeline = RKPipeline(filter_map=filters, linkage_map=linkers, structural_graph=g) 

# Transform the pipeline into a R-K Model
rkm = pipeline.transform(g)
#Build the R-K Model Visualization
RKModelVisualizer.build(rkm)
#Render the R-K Model Visualization
RKModelVisualizer.render()
```

##### Running Tests
``` sh
pytest -m .
```

### Demos
Check these notebooks for more details.

* [Tableau Sales TDA w/ RK Diagrams](https://github.com/animikhroy/rk_toolkit_pipeline_diagrams/blob/main/02_notebooks/rk_general_applications)
* [Ligo GW Analysis](https://github.com/animikhroy/rk_toolkit_pipeline_diagrams/tree/main/02_notebooks/rk_gw_mma)
