import sciunit

class ProducesAMPA(sciunit.Capability):
    def set_waiting_period(self, waiting_period):
        raise NotImplementedError("Must implement set_waiting_period.")
    def set_frequency(self, frequency):
        raise NotImplementedError("Must implement set_frequency.")
    def set_delta_t(self, delta_t):
        raise NotImplementedError("Must implement set_delta_t.")
    def set_spike_pair_count(self, spike_pair_count):
        raise NotImplementedError("Must implement set_spike_pair_count.")
    def set_soma_spike_count(self, soma_spike_count):
        raise NotImplementedError("Must implement set_soma_spike_count.")
    def produce_AMPA(self):
        raise NotImplementedError("Must implement produce_AMPA.")
