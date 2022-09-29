import pandas as pd
from .htg_transformers import (
    BaseOntologyTransform
)

sampleHierarchy = {
  "root": {
    "A": {
      "A_1": {},
      "A_2": {},
    },
    "B": {
      "B_1": {},
      "B_2": {},
    }
   }
}

def testBaseOntologyTransform():
    df = pd.DataFrame([[1,2,3,4]], columns=["A_1", "A_2", "B_1", "B_2"])
    transform = BaseOntologyTransform(mapping=sampleHierarchy)
    g = transform.transform(df.iloc[0])
    assert len(g.nodes) == 7
    assert len(g.edges) == 6
    assert g.is_connected() == True
    assert g.is_dag() == True
    assert g.validate() == True

