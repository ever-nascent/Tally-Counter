import os.path
import pickle

def data_file_exists(file_name):
    if os.path.isfile(file_name):
        with open(file_name, "rb") as file:
            return pickle.load(file)
    else:
        counter_dict = {}
        
        with open(file_name, "wb") as file:
            pickle.dump(counter_dict, file)
        return counter_dict

def create_initial_counter(manager):
    counter_dict_length = manager.get_counter_dict_length()

    if counter_dict_length == 0:
        manager.create_new_counter()
    
def save_counter_data(updated_counter_dict):
    with open("counter_data.pickle", "wb") as file:
        pickle.dump(updated_counter_dict, file)