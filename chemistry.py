class Molecules:
    def __init__(self, molecular_form, name):
        self.molecular_form = molecular_form
        self.name = name

    def __eq__(self, other):
        if (isinstance(other, Molecules)):
            return self.molecular_form == other.molecular_form
        return False


class System:

    storage = []

    def __init__(self, entities):
        storage.append(*entities)

    def do_reaction(self, reagents, reaction_products):
        for reagent in reagents:
            if self.storage.count(reagent) < reagents.count(reagent):
                return "it's impossible do the reaction!"
        
        for reagent in reagents:
            for i in range(0, reagents.count(reagent)):
                self.storage.remove(reagent)
        
        self.storage.append(*reaction_products)
        

    def add_molecule(self, molecule_object):
        storage.append(molecule_object)

    def remove_molecule(self, molecule_object):
        storage.remove(molecule_object)

    def length(self, molecule_object):
        return storage.count(molecule_object)
    
