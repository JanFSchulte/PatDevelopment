## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

runOnMC = False

#if runOnMC:
    #from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValProdTTbarAODSIM
    #process.source.fileNames = filesRelValProdTTbarAODSIM
#else:
    #from PhysicsTools.PatAlgos.patInputFiles_cff import filesSingleMuRECO
    #process.source.fileNames = filesSingleMuRECO
    #process.GlobalTag.globaltag = cms.string("FT_P_V42::All" )
from PhysicsTools.PatAlgos.tools.helpers import loadWithPostFix

loadWithPostFix(process,'PhysicsTools.PatAlgos.patSequences_cff','')

#print process.patDefaultSequence
# Configure PAT to use PF2PAT instead of AOD sources
# this function will modify the PAT sequences.
from PhysicsTools.PatAlgos.tools.pfTools import *




# An empty postfix means that only PF2PAT is run,
# otherwise both standard PAT and PF2PAT are run. In the latter case PF2PAT
# collections have standard names + postfix (e.g. patElectronPFlow)
postfix = "PFlow"
postfix2 = 'PFlow2'
jetAlgo = "AK5"
jetAlgo2 = "AK7"
#Define Objects to be excluded from Top Projection. Default is Tau, so objects are not cleaned for taus
excludeFromTopProjection=['Tau']
usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo, runOnMC=runOnMC, postfix=postfix,typeIMetCorrections=False,excludeFromTopProjection=excludeFromTopProjection)
usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo2, runOnMC=runOnMC, postfix=postfix2,typeIMetCorrections=False,excludeFromTopProjection=excludeFromTopProjection)

# to run second PF2PAT+PAT with different postfix uncomment the following lines
# and add the corresponding sequence to path
#postfix2 = "PFlow2"
#jetAlgo2="AK7"
#usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo2, runOnMC=True, postfix=postfix2)

# to use tau-cleaned jet collection uncomment the following:
#getattr(process,"pfNoTau"+postfix).enable = True

# to switch default tau (HPS) to old default tau (shrinking cone) uncomment
# the following:
# note: in current default taus are not preselected i.e. you have to apply
# selection yourself at analysis level!
#adaptPFTaus(process,"shrinkingConePFTau",postfix=postfix)


if not runOnMC:
    # removing MC matching for standard PAT sequence
    # for the PF2PAT+PAT sequence, it is done in the usePF2PAT function
    removeMCMatchingPF2PAT( process, '' )


# Let it run
#process.p = cms.Path(
    #process.countPatCandidatesPFlow
#    second PF2PAT
#    + getattr(process,"patPF2PATSequence"+postfix2)
#)



# Add PF2PAT output to the created file
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
process.out.outputCommands = cms.untracked.vstring('drop *',
                                                   'keep recoPFCandidates_particleFlow_*_*',
						   'keep *_selectedPatPhotons'+postfix+'*_*_*',
						   'keep *_selectedPatElectrons'+postfix+'*_*_*',
					           'keep *_selectedPatMuons'+postfix+'*_*_*',
					           'keep *_selectedPatTaus'+postfix+'*_*_*',
					           'keep *_selectedPatJets'+postfix+'*_*_*',
						   'keep *_patMETs'+postfix+'*_*_*',
						   'keep *_selectedPatPhotons'+postfix2+'*_*_*',
						   'keep *_selectedPatElectrons'+postfix2+'*_*_*',
					           'keep *_selectedPatMuons'+postfix2+'*_*_*',
					           'keep *_selectedPatTaus'+postfix2+'*_*_*',
					           'keep *_selectedPatJets'+postfix2+'*_*_*',
						   'keep *_patMETs'+postfix2+'*_*_*', 				
						   'keep *_selectedPatPhotons'+'*_*_*',
						   'keep *_selectedPatElectrons'+'*_*_*',
					           'keep *_selectedPatMuons'+'*_*_*',
					           'keep *_selectedPatTaus'+'*_*_*',
					           'keep *_selectedPatJets'+'*_*_*',
						   'keep *_patMETs'+'*_*_*',		   						   
 )





# verbose flags for the PF2PAT modules
getattr(process,"pfNoMuon"+postfix).verbose = False
process.options.allowUnscheduled = cms.untracked.bool(True)
#process.Tracer = cms.Service("Tracer")
## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
#
#   process.GlobalTag.globaltag =  ...    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#                                         ##
#   process.source.fileNames =  ...       ##  (e.g. 'file:AOD.root')
#
process.source.fileNames = cms.untracked.vstring('file:/user/jschulte/52X/RelValTTbar_5_3_6_START53_V14_AOD.root')                                         ##
process.maxEvents.input = 100
#                                         ##
#   process.out.outputCommands = [ ... ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
process.out.fileName = 'patTuple_PATandPF2PAT.root'
#                                         ##
#   process.options.wantSummary = False   ##  (to suppress the long output at the end of the job)

#process.prune(verbose=True)
