import pandas as pd
import difflib
import os
from pywebio import *
from pywebio.input import input, TEXT
from pywebio.output import put_info
from flask import Flask


app = Flask(__name__)
data = pd.read_csv('names_tribe.csv')


def make_tuple(data):
    name_tribe = []
    """This function creates a tuple of (name, tribe) and adds it into
        the name_tribe list
    """
    start = 0
    for i in range(0, data.shape[0]):
        detail = data.iloc[start] # scanning through each line of the data set to pull out name and tribe
        name, tribe = detail.loc['name'], detail.loc['tribe']
        details = (name, tribe)
        name_tribe.append(details)
        start +=1
    return name_tribe


name_tribe = make_tuple(data) # Storing list of name,tribe tuples.


def tribe_detect(name_tribe):
    # name = input("enter your name: ")
    name_entered = input('Tribe Detection System', type=TEXT, placeholder='Enter your name')
    similarity_tuple = []
    """This function calculates the sequence similarity between name entered
        and names available in dataset then returns a tuple
    """
    for names in name_tribe:
        sequence = difflib.SequenceMatcher(isjunk=None, a = name_entered.lower(), b = names[0].lower())
        similarity = sequence.ratio()*100 # Converting sequence matcher object into percentage
        similarity = round(similarity,1) # Rounding up similarity into 1dp
        similarity_tuple.append((names[0], names[1], similarity))
    run_sort(name_entered, similarity_tuple)


def run_sort(name_entered, similarity_tuple):
    """This function runs the entire code then sorts the given tuple list
        based on the 3rd item in a tuple, index [2] in descending order
    """
    similarity_tuple.sort(key = lambda x:x[2], reverse = True) #Grabbing the tuple with the highest score above 70%
    
    if similarity_tuple[0][2] > 70:
        put_info(f"The name '{name_entered}' is most likely to be a/an '{similarity_tuple[0][1]}' name",
        closable=True, scope=None, position=- 1)
        
    else:
        put_info("Sorry, your name could not be matched.", closable=True, scope=None, position=- 1)


# tribe_detect(name_tribe)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)