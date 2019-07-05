from rdkit import Chem
import json
from rdkit.Chem import rdMolDescriptors, Descriptors
import matplotlib
matplotlib.use('Agg')
matplotlib.matplotlib_fname()
import numpy
from openpyxl import Workbook, load_workbook

def loader():
	wb = load_workbook(filename = "acid_amine_final_320.xlsx")
	sheet = wb['Sheet1']

	allprods = []
	first = True
	for f in sheet:
		mol = Chem.MolFromSmiles(f[0].value)
		Chem.SanitizeMol(mol)
		Chem.Kekulize(mol, clearAromaticFlags=True)
		allprods.append(mol)
	print(len(allprods))


	with open('alldrugsprops.json') as f:
		drugProps = json.load(f) #load info into drugProps

	mols = []
	for f in drugProps:
		mol = Chem.MolFromSmiles(f["SMILES"])
		Chem.SanitizeMol(mol)
		Chem.Kekulize(mol, clearAromaticFlags=True)
		mols.append(mol)

	N = 320
	dist = int(200000/N)


	cmap = plt.get_cmap(name='plasma')
	drug_counter=0
	all_links = []
	# single = Chem.MolFromSmiles("[H][C@]1([C@]2([H])C(C=CC(OC)=C3OC)=C3C(O2)=O)C4=C(OC)C5=C(OCO5)C=C4CCN1C")
	# Chem.SanitizeMol(single)
	# Chem.Kekulize(single, clearAromaticFlags=True)
	# mols = [single]
	for drug in mols:
		reaction_counter = 9300
		rxn_counter = 0
		for prod in allprods:
			hits = drug.GetSubstructMatches(prod)
			if hits:
				inter = numpy.interp(len(hits), (1, 10), (-0, +1))
				color = tuple(255*x for x in cmap(inter)[0:3])

				link = "hs1 " + str(drug_counter) + " " + str(drug_counter+1) + " hs2 " + str(reaction_counter) + " " + str(reaction_counter+dist) + " color=(" + str(color[0])+","+ str(color[1])+","+str(color[2])+",.1)"
				all_links.append(link)
				print("hs2 " + str(reaction_counter) + " " + str(reaction_counter+dist) + " O color=(32,146,140,1)")
			reaction_counter = reaction_counter + dist
			rxn_counter = rxn_counter + 1
		drug_counter = drug_counter + 1

	print(len(all_links))
	with open("links.txt", "w") as output:
		for s in all_links:
			output.write("%s\n" % s)


loader()