import sqlite3

class Chords:
    """
    2023-06-10: Read and write to the SQLite database by first loading
    up the dictionary to use as a temporary memory store.
    """
    
    db = sqlite3.connect("chord_database.db")
    cur = db.cursor()
    loaded_chords = None
    
    # STRING STACK
    
    e_str_high = []
    b_str = []
    g_str = []
    d_str = []
    a_str = []
    e_str_low = []
    
    guitar = [e_str_high,
              b_str,
              g_str,
              d_str,
              a_str,
              e_str_low
              ]
                        
    # VARIABLES BELOW
    
    STRINGS = [
        e_str_high,
        b_str,
        g_str,
        d_str,
        a_str,
        e_str_low]    
    
    # CONSTANTS BELOW
    
    tab_lines = [
        "--",
        "--",
        "--",
        "--",
        "--",
        "--"]
    
    
    # DATABASE BELOW
    
    x = "X"
    chord_dictionary = {
                #"G": [3,0,0,0,2,3],
                #"C": [0,1,0,2,3,x],
                #"A": [0,2,2,2,0,x],
                #"D": [2,3,2,0,x,x],
                #"E": [0,0,1,2,2,x],
                #"Em": [0,0,0,2,2,x],
                #"Am": [0,1,2,2,0,0,x],
                #"Dm": [1,3,2,0,0,x],
                #"D7": [2,1,2,0,0,0],
                #"A7": [0,2,0,2,0,0],
                #"A7Maj": [0,2,1,2,0,0],
                #"F": [1,1,2,3,3,1],
                #"B": [2,4,4,4,2,2],
                #"Bm": [2,3,4,4,2,2],
                #"Bb": [1,3,3,3,1,1],
                #"GMaj": [2,0,0,0,2,3]
                #
                # Note how chords are
                # tabulated in reverse
                # order from right to left
                }
    
    reverse_chord_dict = {}
    
    def __init__(self):
        self.class_assignments()
        self.reverse_chord_dict = self.reverse_dict(self.chord_dictionary)
    
    @classmethod
    def class_assignments(cls):
        if cls.loaded_chords is None:
            cls.loaded_chords = []
        else:
            cls.load_memory()
        
    @classmethod
    def load_memory(cls):
        """
        Loads db as a class variable.
        Creates db if none exists.
        Only run the first time an instance is created
        """
        cls.db.execute("CREATE TABLE IF NOT EXISTS chords (name TEXT tab TEXT quality TEXT key TEXT)")
        cls.loaded_chords = cls.cur.fetchall()

    @staticmethod
    def stringify(list):
        stringed = ""
        for i in list:
            stringed += str(i)
        return stringed
    
    def reverse_dict(self, dict_to_reverse):
        return dict((self.stringify(v), k) for k, v in dict_to_reverse.items())

    @classmethod
    def add_chord(cls):
        print("What is the name of the new chord?")
        chord_name = input()
        # TODO: check if name already in db, if so break
        print(f"What are the tab value of {chord_name}, left to right?")
        chord_to_add = input()
        # TODO: check if tab already in db, if so give name, then break
        print(f"What is the quality of {chord_name} (e.g. major, minor, etc.)?")
        chord_quality = input()
        values = [chord_name, chord_to_add, chord_quality]
        cls.db.execute(f"INSERT INTO chords (name, tab, quality) VALUES(?, ?, ?)", values)
        cls.db.commit()
    
    def display_tab(self):
        for i in range(6):
            for j in self.guitar[i]:
                self.tab_lines[i] += str(j) + "--"
            print(self.tab_lines[i])
    
    @classmethod
    def chord_lookup(cls, e_str_high, b_str, g_str, d_str, a_str, e_str_low):
        lookup = f"{e_str_high}{b_str}{g_str}{d_str}{a_str}{e_str_low}"
        name = ""
        if lookup in cls.reverse_chord_dict:
            name = cls.reverse_chord_dict[lookup]
            return name
        else:
            print("That chord is not in the database.")
            new_chord = (name, lookup)
            lookup = list(lookup)
            for i in range(len(lookup)):
                lookup[i] = int(lookup[i])
            print("Let's add it. What should we call it?")
            # I should keep the part of the function that
            # updates the internal dict, and make it so that
            # it also updates the db. That way I can load up
            # the db just once at the start of the call for
            # a class instance, and use the same chord dict
            # across different instances (as a class attribute).
            name = input()
            cls.chord_dictionary[name] = lookup
            cls.reverse_chord_dict = cls.reverse_dict(cls, cls.chord_dictionary)
            # SQLite part below
            # use self.

