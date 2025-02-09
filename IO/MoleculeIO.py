import xml.etree.ElementTree as ET
from Data.Molecule import Molecule
import Logger as lg
import os

from typing import Dict

def load_molecule_databases() -> Dict[str, Molecule]:

    molecules = {}
    settings_tree_data = None

    try:
            # If errors while attempt to read, requires conversion.
        with open(os.path.join(lg.current_directory,"settings.xml"))as f:
            settings_tree_data = f.read()

    except Exception as err:
        lg.log_error(f'Unable to read molecule library paths from settings xml: {err}')

    if settings_tree_data:
        settings_root = ET.fromstring(settings_tree_data)

        for databases in settings_root.findall("./settings/databases/database"):

            try:

                # If not full path uses MoleculeDatabases folder
                if ("\\") in databases.text and ("/") in databases.text:
                    # If errors while attempt to read, requires conversion.
                    with open(databases.text) as f:
                        tree_data = f.read()
                else:
                    # If errors while attempt to read, requires conversion.
                    with open(os.path.join(lg.current_directory,"MoleculeDatabases",databases.text)) as f:
                        tree_data = f.read()

                compound_root = ET.fromstring(tree_data)

                for compound_node in compound_root.findall("./compound"):

                    id = compound_node.find("./id")
                    name = compound_node.find("./name")
                    formula = compound_node.find("./formula")
                    inchi = compound_node.find("./inchi")
                    smiles = compound_node.find("./smiles")
                    synonyms = compound_node.find("./synonyms")
                    retention_time = compound_node.find("./retentiontime")
                    description = compound_node.find("./description")
                    class_desc = compound_node.find("./class")
                    mass = compound_node.find("./monoisotopicmass")
                    polarity = compound_node.find("./polarity")

                    molecule = Molecule(id.text, name.text, formula.text)
                    if inchi is not None:
                        molecule.inchi = inchi.text

                    if smiles is not None:
                        molecule.smiles = smiles.text

                    if synonyms is not None:    
                        molecule.synonyms = synonyms.text

                    if description is not None:
                        molecule.description = description.text

                    if class_desc is not None:
                        molecule.class_description = class_desc.text

                    if retention_time is not None:
                        molecule.retention_time = float(retention_time.text) * 60.0

                    if mass is not None and mass.text is not None and len(mass.text) > 0:
                        molecule.mass = mass.text
                            
                    if polarity is not None:
                        molecule.polarity = polarity.text

                    molecules[id.text] = molecule

            except Exception as err:
                lg.log_error(f'Unable to import details from molecule library: {err}')

    return molecules
            