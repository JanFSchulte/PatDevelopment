def main():
	
	
	#~ from electronSelector_cfi import *
	PhysicsTools =  __import__('PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi')
	PhysicsTools =  __import__('PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi')	
	print PhysicsTools

	print PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi.selectedPatElectrons.src
	print PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi.selectedPatMuons.src
	
main()
