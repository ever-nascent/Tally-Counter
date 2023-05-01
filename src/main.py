from util import data_file_exists, create_initial_counter
from counter_manager import CounterManager
from gui import GUI

def main():
    counter_data = data_file_exists("counter_data.pickle")

    manager = CounterManager(counter_data)
    create_initial_counter(manager)

    gui = GUI(manager)
    gui.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occured:", e)