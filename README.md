# remove_fhem_graph_spikes_alecto_ws1700
This script removes the spikes (incorrect measurements) from a FHEM pilight temperature and humidty sensor log.
The log contains temperature, humidity and battery data, which is coming in from a Alecto WS1700 sensor via Pilight.
It it is interpreted by the pilight_ctrl plugin within FHEM.

It detects the spikes by running through the logfile and calculating the differences between every 3 consecutive values.
If the difference reaches a given threshold, the spike is flattened to the average of is predecessor and successor.
