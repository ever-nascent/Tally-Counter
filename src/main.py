from util import *
from counter_manager import CounterManager
from gui import GUI

if __name__ == "__main__":
	counter_data = data_file_exists("counter_data.pickle")

	manager = CounterManager(counter_data)
	create_initial_counter(manager)

	gui = GUI(manager)
	gui.run()