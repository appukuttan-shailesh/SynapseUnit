import sciunit

class ProducesAMPAVector(sciunit.Capability):
    def set_waiting_period(self, waiting_period):
        raise NotImplementedError("Must implement set_waiting_period.")
    def set_frequency(self, frequency):
        raise NotImplementedError("Must implement set_frequency.")
    def set_delta_t_vector(self, delta_t_vector):
        raise NotImplementedError("Must implement set_delta_t_vector.")
    def set_spike_pair_count(self, spike_pair_count):
        raise NotImplementedError("Must implement set_spike_pair_count.")
    def set_soma_spike_count(self, soma_spike_count):
        raise NotImplementedError("Must implement set_soma_spike_count.")
    def produce_AMPA_vector(self):
        raise NotImplementedError("Must implement produce_AMPA.")
    def calc_tstop(self):
        return self.waiting_period + self.spike_pair_count*(1000/self.frequency) + 200
