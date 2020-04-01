import sciunit.scores
import numpy as np

class RMSscore(sciunit.scores.Score):
    """A root mean square score."""

    _allowed_types = (float,)

    _description = (' ',)

    @classmethod
    def compute(cls, observation, prediction):
        rmse = np.sqrt(np.mean((np.array(observation) - np.array(prediction))**2))
        """Compute whether the observation equals the prediction."""
        return RMSscore(rmse)

    def __str__(self):
        return '%.3g' % self.score
