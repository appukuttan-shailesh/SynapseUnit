import os
import json
import sciunit
try:
    from sciunit import ObservationError
except:
    from sciunit.errors import ObservationError
import synapseunit.capabilities as cap
from synapseunit.scores import RMSscore
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import csv

class STDPtest(sciunit.Test):

    config_dir = os.path.join(os.path.dirname(__file__), "./stimuli/STDPtest")
    required_capabilities = (cap.ProducesAMPAVector,)
    score_type = RMSscore
    valid_protocols = ["ltp", "ltd", "bidirectional"]

    def __init__(self, observation={}, protocol="", name="test_STDP", output_dir=None):
        if protocol not in self.valid_protocols:
            raise ValueError("Test requires 'protocol' parameter to be set from: {}".format(self.valid_protocols))
        super().__init__(observation, name+"_"+protocol)
        self.protocol = protocol
        self.read_protocol_json(os.path.join(self.config_dir, "protocol_{}.json".format(self.protocol)))
        if not output_dir:
            self.output_dir = os.path.join(".", name+"_"+protocol, datetime.now().strftime("%Y%m%d-%H%M%S"))

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

        # create relevant output files
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
        except OSError as e:
            raise OSError("Could not create output directory: {}".format(self.output_dir))

        # 1. Create figure: obs vs pred
        delta_t_vector = list(map(int, observation.keys()))
        obs = list(observation.values())
        plt.style.use('seaborn-whitegrid')
        title_font = {'family': 'serif', 'color':  'darkred', 'weight': 'bold', 'size': 16}
        label_font = {'family': 'serif', 'color':  'darkred', 'weight': 'normal', 'size': 14}
        fig = plt.figure(figsize=(10,5))
        ax = plt.axes()
        ax.plot(delta_t_vector, obs, color='blue', marker='o', markersize=6, label='observation');
        ax.plot(delta_t_vector, prediction, color='red', marker='X', markersize=6, linestyle='dashed', label='prediction');
        plt.title('Test : {}'.format(self.name), fontdict=title_font)
        plt.xlabel('delta_t (ms)', fontdict=label_font)
        plt.ylabel('', fontdict=label_font)
        legend = ax.legend(loc='best', shadow=True, fontsize='x-large')
        filepath = os.path.join(self.output_dir, 'traces.pdf')
        fig.savefig(filepath, dpi=600)
        plt.show()
        plt.close('all')

        # 2. Create data file: observation and prediction combined
        result_json = []
        for ind, (obs_key, obs_val) in enumerate(observation.items()):
            r_tuple = (obs_key, obs_val, prediction[ind])
            result_json.append(r_tuple)
        filepath = os.path.join(self.output_dir, 'data.csv')
        with open(filepath, 'w') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(['delta_t','observation', 'prediction'])
            for row in result_json:
                csv_out.writerow(row)
        return score

    def bind_score(self, score, model, observation, prediction):
        score.related_data["figures"] = [os.path.join(self.output_dir, 'traces.pdf'),
                                         os.path.join(self.output_dir, 'data.csv')]
        return score
