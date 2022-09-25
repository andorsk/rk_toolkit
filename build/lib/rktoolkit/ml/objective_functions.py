import numpy as np

class SampleObjectiveFunction():
    '''
    Sample objective function reduces distance
    '''
    def __init__(self, pipeline, sample_size, w0, df, hft, mdist, distance_function):
        self.pipeline = pipeline
        self.sample_size = sample_size
        self.w0 = w0
        self.df = df
        self.hft = hft
        self.mdist = mdist
        self.dfunc = distance_function

    def evaluate(self, w):
        '''

        :param w: Weights to be used for evaluation in the objective function
        :type w: tuple
        :return: The R-K distance evaluated from the objective function
        :rtype: float
        '''
        pupdate = self.pipeline.remap(w, self.w0[1])
        models = []
        sample = self.df.sample(n=self.sample_size)
        for i, row in sample.iterrows():
            g = self.hft.transform(row)
            g = pupdate.transform(g)
            g.id = i
            models.append(g)

        distances = self.dfunc(models, self.mdist, [1, 0])
        c = 1 - np.mean(distances)
        return c
