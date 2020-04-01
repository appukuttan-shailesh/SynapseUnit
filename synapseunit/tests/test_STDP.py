import os
import json
import sciunit
try:
    from sciunit import ObservationError
except:
    from sciunit.errors import ObservationError
import synapseunit.capabilities as cap
from synapseunit.scores import RMSscore

class STDPtest(sciunit.Test):

    config_dir = os.path.join(os.path.dirname(__file__), "./stimuli/STDPtest")
    required_capabilities = (cap.ProducesAMPAVector,)
    score_type = RMSscore
    valid_protocols = ["ltp", "ltd", "bidirectional"]

    def __init__(self, observation={}, protocol="", name="STDP"):
        if protocol not in self.valid_protocols:
            raise ValueError("Test requires 'protocol' parameter to be set from: {}".format(self.valid_protocols))
        super().__init__(observation, name+"_"+protocol)
        self.protocol = protocol
        self.read_protocol_json(os.path.join(self.config_dir, "protocol_{}.json".format(self.protocol)))

    def read_protocol_json(self, path):
        with open(path, 'r') as f:
            self.protocol_params = json.load(f)

    def prepare_protocol(self, model):
        model.set_frequency(self.protocol_params['frequency'])
        model.set_spike_pair_count(self.protocol_params['spike_pair_count'])
        model.set_soma_spike_count(self.protocol_params['soma_spike_count'])
        model.set_delta_t_vector(self.protocol_params['delta_t_vector'])
        model.set_waiting_period(1)

    def validate_observation(self, observation):
        if type(observation) is not dict:
            raise ObservationError("Observation must be a Python dictionary!")

    def generate_prediction(self, model):
        self.prepare_protocol(model)
        return model.produce_AMPA_vector()

    def compute_score(self, observation, prediction):
        rms = RMSscore.compute(list(observation.values()), prediction)
        score = self.score_type(rms.score)
        score.description = ("")
        return score
