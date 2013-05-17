import FWCore.ParameterSet.Config as cms

#from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.tauTools import *

from PhysicsTools.PatAlgos.tools.helpers import listModules, applyPostfix

from copy import deepcopy

#def applyPostfix(process, label, postfix):
#    ''' If a module is in patDefaultSequence use the cloned module.
#    Will crash if patDefaultSequence has not been cloned with 'postfix' beforehand'''
#    result = None
#    defaultLabels = [ m.label()[:-len(postfix)] for m in listModules( getattr(process,"patDefaultSequence"+postfix))]
#    if label in defaultLabels:
#        result = getattr(process, label+postfix)
#    else:
#        print "WARNING: called applyPostfix for module %s which is not in patDefaultSequence!"%label
#        result = getattr(process, label)
#    return result

#def removeFromSequence(process, seq, postfix, baseSeq='patDefaultSequence'):
#    defaultLabels = [ m.label()[:-len(postfix)] for m in listModules( getattr(process,baseSeq+postfix))]
#    for module in listModules( seq ):
#        if module.label() in defaultLabels:
#            getattr(process,baseSeq+postfix).remove(getattr(process, module.label()+postfix))

def warningIsolation():
    print "WARNING: particle based isolation must be studied"

from CommonTools.ParticleFlow.Tools.pfIsolation import setupPFElectronIso, setupPFMuonIso

def useGsfElectrons(process, postfix, dR = "04"):
    print "using Gsf Electrons in PF2PAT"
    print "WARNING: this will destory the feature of top projection which solves the ambiguity between leptons and jets because"
    print "WARNING: there will be overlap between non-PF electrons and jets even though top projection is ON!"
    print "********************* "
    module = applyPostfix(process,"patElectrons",postfix)
    module.useParticleFlow = False
    print "Building particle-based isolation for GsfElectrons in PF2PAT(PFBRECO)"
    print "********************* "
    adaptPFIsoElectrons( process, module, postfix+"PFIso", dR )
    getattr(process,'patDefaultSequence'+postfix).replace( getattr(process,"patElectrons"+postfix),
                                                   setupPFElectronIso(process, 'gsfElectrons', "PFIso", postfix, runPF2PAT=True) +
                                                   getattr(process,"patElectrons"+postfix) )

def adaptPFIsoElectrons(process,module, postfix = "PFIso", dR = "04"):
    #FIXME: adaptPFElectrons can use this function.
    module.isoDeposits = cms.PSet(
        pfChargedHadrons = cms.InputTag("elPFIsoDepositCharged" + postfix),
        pfChargedAll = cms.InputTag("elPFIsoDepositChargedAll" + postfix),
        pfPUChargedHadrons = cms.InputTag("elPFIsoDepositPU" + postfix),
        pfNeutralHadrons = cms.InputTag("elPFIsoDepositNeutral" + postfix),
        pfPhotons = cms.InputTag("elPFIsoDepositGamma" + postfix)
        )
    module.isolationValues = cms.PSet(
        pfChargedHadrons = cms.InputTag("elPFIsoValueCharged"+dR+"PFId"+ postfix),
        pfChargedAll = cms.InputTag("elPFIsoValueChargedAll"+dR+"PFId"+ postfix),
        pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU"+dR+"PFId" + postfix),
        pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral"+dR+"PFId" + postfix),
        pfPhotons = cms.InputTag("elPFIsoValueGamma"+dR+"PFId" + postfix)
        )
    module.isolationValuesNoPFId = cms.PSet(
        pfChargedHadrons = cms.InputTag("elPFIsoValueCharged"+dR+"NoPFId"+ postfix),
        pfChargedAll = cms.InputTag("elPFIsoValueChargedAll"+dR+"NoPFId"+ postfix),
        pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU"+dR+"NoPFId" + postfix),
        pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral"+dR+"NoPFId" + postfix),
        pfPhotons = cms.InputTag("elPFIsoValueGamma"+dR+"NoPFId" + postfix)
        )

def adaptPFIsoMuons(process,module, postfix = "PFIso", dR = "04"):
    #FIXME: adaptPFMuons can use this function.
    module.isoDeposits = cms.PSet(
        pfChargedHadrons = cms.InputTag("muPFIsoDepositCharged" + postfix),
        pfChargedAll = cms.InputTag("muPFIsoDepositChargedAll" + postfix),
        pfPUChargedHadrons = cms.InputTag("muPFIsoDepositPU" + postfix),
        pfNeutralHadrons = cms.InputTag("muPFIsoDepositNeutral" + postfix),
        pfPhotons = cms.InputTag("muPFIsoDepositGamma" + postfix)
        )
    module.isolationValues = cms.PSet(
        pfChargedHadrons = cms.InputTag("muPFIsoValueCharged" + dR + postfix),
        pfChargedAll = cms.InputTag("muPFIsoValueChargedAll" + dR + postfix),
        pfPUChargedHadrons = cms.InputTag("muPFIsoValuePU" + dR + postfix),
        pfNeutralHadrons = cms.InputTag("muPFIsoValueNeutral" + dR + postfix),
        pfPhotons = cms.InputTag("muPFIsoValueGamma" + dR + postfix)
        )

def usePFIso(process, postfix = "PFIso"):
    print "Building particle-based isolation "
    print "***************** "
    process.eleIsoSequence = setupPFElectronIso(process, 'gsfElectrons', postfix)
    process.muIsoSequence = setupPFMuonIso(process, 'muons', postfix)
    adaptPFIsoMuons( process, applyPostfix(process,"patMuons",""), postfix)
    adaptPFIsoElectrons( process, applyPostfix(process,"patElectrons",""), postfix)
    getattr(process,'patDefaultSequence').replace( getattr(process,"patCandidates"),
                                                   process.pfParticleSelectionSequence +
                                                   process.eleIsoSequence +
                                                   process.muIsoSequence +
                                                   getattr(process,"patCandidates") )

def adaptPFMuons(process,module,postfix="" ):
    print "Adapting PF Muons "
    print "***************** "
    warningIsolation()
    print
    module.useParticleFlow = True
    module.pfMuonSource    = cms.InputTag("pfIsolatedMuonsClones" + postfix)
    module.userIsolation   = cms.PSet()
    module.isoDeposits = cms.PSet(
        pfChargedHadrons = cms.InputTag("muPFIsoDepositCharged" + postfix),
        pfChargedAll = cms.InputTag("muPFIsoDepositChargedAll" + postfix),
        pfPUChargedHadrons = cms.InputTag("muPFIsoDepositPU" + postfix),
        pfNeutralHadrons = cms.InputTag("muPFIsoDepositNeutral" + postfix),
        pfPhotons = cms.InputTag("muPFIsoDepositGamma" + postfix)
        )
    module.isolationValues = cms.PSet(
        pfChargedHadrons = cms.InputTag("muPFIsoValueCharged04"+ postfix),
        pfChargedAll = cms.InputTag("muPFIsoValueChargedAll04"+ postfix),
        pfPUChargedHadrons = cms.InputTag("muPFIsoValuePU04" + postfix),
        pfNeutralHadrons = cms.InputTag("muPFIsoValueNeutral04" + postfix),
        pfPhotons = cms.InputTag("muPFIsoValueGamma04" + postfix)
        )
    # matching the pfMuons, not the standard muons.
    applyPostfix(process,"muonMatch",postfix).src = module.pfMuonSource

    print " muon source:", module.pfMuonSource
    print " isolation  :",
    print module.isolationValues
    print " isodeposits: "
    print module.isoDeposits
    print


def adaptPFElectrons(process,module, postfix):
    # module.useParticleFlow = True
    print "Adapting PF Electrons "
    print "********************* "
    warningIsolation()
    print
    module.useParticleFlow = True
    module.pfElectronSource = cms.InputTag("pfIsolatedElectronsClones" + postfix)
    module.userIsolation   = cms.PSet()
    module.isoDeposits = cms.PSet(
        pfChargedHadrons = cms.InputTag("elPFIsoDepositCharged" + postfix),
        pfChargedAll = cms.InputTag("elPFIsoDepositChargedAll" + postfix),
        pfPUChargedHadrons = cms.InputTag("elPFIsoDepositPU" + postfix),
        pfNeutralHadrons = cms.InputTag("elPFIsoDepositNeutral" + postfix),
        pfPhotons = cms.InputTag("elPFIsoDepositGamma" + postfix)
        )
    module.isolationValues = cms.PSet(
        pfChargedHadrons = cms.InputTag("elPFIsoValueCharged04PFId"+ postfix),
        pfChargedAll = cms.InputTag("elPFIsoValueChargedAll04PFId"+ postfix),
        pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU04PFId" + postfix),
        pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral04PFId" + postfix),
        pfPhotons = cms.InputTag("elPFIsoValueGamma04PFId" + postfix)
        )

    # COLIN: since we take the egamma momentum for pat Electrons, we must
    # match the egamma electron to the gen electrons, and not the PFElectron.
    # -> do not uncomment the line below.
    # process.electronMatch.src = module.pfElectronSource
    # COLIN: how do we depend on this matching choice?

    print " PF electron source:", module.pfElectronSource
    print " isolation  :"
    print module.isolationValues
    print " isodeposits: "
    print module.isoDeposits
    print

    print "removing traditional isolation"

    removeIfInSequence(process,  "patElectronIsolation",  "patPF2PATSequence", postfix)

def adaptPFPhotons(process,module):
    raise RuntimeError, "Photons are not supported yet"

from RecoTauTag.RecoTau.TauDiscriminatorTools import adaptTauDiscriminator, producerIsTauTypeMapper

def reconfigurePF2PATTaus(process,
      tauType='shrinkingConePFTau',
      pf2patSelection=["DiscriminationByIsolation", "DiscriminationByLeadingPionPtCut"],
      selectionDependsOn=["DiscriminationByLeadingTrackFinding"],
      producerFromType=lambda producer: producer+"Producer",
      postfix = ""):
   print "patTaus will be produced from taus of type: %s that pass %s" \
	 % (tauType, pf2patSelection)

   #get baseSequence
   baseSequence = getattr(process,"pfTausBaseSequence")
   #clean baseSequence from old modules
   for oldBaseModuleName in baseSequence.moduleNames():
       oldBaseModule = getattr(process,oldBaseModuleName+postfix)
       process.patPF2PATSequence.remove(oldBaseModule)

   # Get the prototype of tau producer to make, i.e. fixedConePFTauProducer
   producerName = producerFromType(tauType)
   # Set as the source for the pf2pat taus (pfTaus) selector
   applyPostfix(process,"pfTaus", postfix).src = producerName+postfix
   # Start our pf2pat taus base sequence
   oldTauSansRefs = getattr(process,'pfTausProducerSansRefs'+postfix)
   oldTau = getattr(process,'pfTausProducer'+postfix)
   ## copy tau and setup it properly
   newTauSansRefs = None
   newTau = getattr(process,producerName).clone()

   
   ## adapted to new structure in RecoTauProducers PLEASE CHECK!!!
   if tauType=='shrinkingConePFTau':
       newTauSansRefs = getattr(process,producerName+"SansRefs").clone()
       newTauSansRefs.modifiers[1] = cms.PSet(
           pfTauTagInfoSrc = cms.InputTag("pfTauTagInfoProducer"+postfix),
           name = cms.string('pfTauTTIworkaround'+postfix),
           plugin = cms.string('RecoTauTagInfoWorkaroundModifer')
           )
       newTau.modifiers[1] = newTauSansRefs.modifiers[1]
       newTauSansRefs.piZeroSrc = "pfJetsLegacyTaNCPiZeros"+postfix
       newTau.piZeroSrc = newTauSansRefs.piZeroSrc
       newTauSansRefs.builders[0].pfCandSrc = oldTauSansRefs.builders[0].pfCandSrc
       newTauSansRefs.jetRegionSrc = oldTauSansRefs.jetRegionSrc
       newTauSansRefs.jetSrc = oldTauSansRefs.jetSrc
   elif tauType=='fixedConePFTau':
       newTau.piZeroSrc = "pfJetsLegacyTaNCPiZeros"+postfix
   elif tauType=='hpsPFTau':
       
       newTau = process.combinatoricRecoTaus.clone()
       newTau.piZeroSrc="pfJetsLegacyHPSPiZeros"+postfix
       newTau.modifiers[3] = cms.PSet(
           pfTauTagInfoSrc = cms.InputTag("pfTauTagInfoProducer"+postfix),
           name = cms.string('pfTauTTIworkaround'+postfix),
           plugin = cms.string('RecoTauTagInfoWorkaroundModifer')
           )
       from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
       cloneProcessingSnippet(process, process.produceHPSPFTaus, postfix)
       massSearchReplaceParam(getattr(process,"produceHPSPFTaus"+postfix),
                              "PFTauProducer",
                              cms.InputTag("combinatoricRecoTaus"),
                              cms.InputTag("pfTausBase"+postfix) )
       massSearchReplaceParam(getattr(process,"produceHPSPFTaus"+postfix),
                              "src",
                              cms.InputTag("combinatoricRecoTaus"),
                              cms.InputTag("pfTausBase"+postfix) )

   #newTau.builders[0].pfCandSrc = oldTau.builders[0].pfCandSrc
   #newTau.jetRegionSrc = oldTau.jetRegionSrc
   #newTau.jetSrc = oldTau.jetSrc

   # replace old tau producer by new one put it into baseSequence
   setattr(process,"pfTausBase"+postfix,newTau)
   if tauType=='shrinkingConePFTau':
       setattr(process,"pfTausBaseSansRefs"+postfix,newTauSansRefs)
       getattr(process,"pfTausBase"+postfix).src = "pfTausBaseSansRefs"+postfix
       baseSequence += getattr(process,"pfTausBaseSansRefs"+postfix)
   baseSequence += getattr(process,"pfTausBase"+postfix)
   if tauType=='hpsPFTau':
       baseSequence += getattr(process,"produceHPSPFTaus"+postfix)
   #make custom mapper to take postfix into account (could have gone with lambda of lambda but... )
   def producerIsTauTypeMapperWithPostfix(tauProducer):
       return lambda x: producerIsTauTypeMapper(tauProducer)+x.group(1)+postfix

   def recoTauTypeMapperWithGroup(tauProducer):
       return "%s(.*)"%recoTauTypeMapper(tauProducer)

   # Get our prediscriminants
   for predisc in selectionDependsOn:
      # Get the prototype
      originalName = tauType+predisc # i.e. fixedConePFTauProducerDiscriminationByLeadingTrackFinding
      clonedName = "pfTausBase"+predisc+postfix
      clonedDisc = getattr(process, originalName).clone()
      # Register in our process
      setattr(process, clonedName, clonedDisc)
      baseSequence += getattr(process, clonedName)

      tauCollectionToSelect = None
      if tauType != 'hpsPFTau' :
          tauCollectionToSelect = "pfTausBase"+postfix
          #cms.InputTag(clonedDisc.PFTauProducer.value()+postfix)
      else:
          tauCollectionToSelect = "hpsPFTauProducer"+postfix
      # Adapt this discriminator for the cloned prediscriminators
      adaptTauDiscriminator(clonedDisc, newTauProducer="pfTausBase",
                            oldTauTypeMapper=recoTauTypeMapperWithGroup,
                            newTauTypeMapper=producerIsTauTypeMapperWithPostfix,
                            preservePFTauProducer=True)
      clonedDisc.PFTauProducer = tauCollectionToSelect

   # Reconfigure the pf2pat PFTau selector discrimination sources
   applyPostfix(process,"pfTaus", postfix).discriminators = cms.VPSet()
   for selection in pf2patSelection:
      # Get our discriminator that will be used to select pfTaus
      originalName = tauType+selection
      clonedName = "pfTausBase"+selection+postfix
      clonedDisc = getattr(process, originalName).clone()
      # Register in our process
      setattr(process, clonedName, clonedDisc)

      tauCollectionToSelect = None

      if tauType != 'hpsPFTau' :
          tauCollectionToSelect = cms.InputTag("pfTausBase"+postfix)
          #cms.InputTag(clonedDisc.PFTauProducer.value()+postfix)
      else:
          tauCollectionToSelect = cms.InputTag("hpsPFTauProducer"+postfix)
      #Adapt our cloned discriminator to the new prediscriminants
      adaptTauDiscriminator(clonedDisc, newTauProducer="pfTausBase",
                            oldTauTypeMapper=recoTauTypeMapperWithGroup,
                            newTauTypeMapper=producerIsTauTypeMapperWithPostfix,
                            preservePFTauProducer=True)
      clonedDisc.PFTauProducer = tauCollectionToSelect
      baseSequence += clonedDisc
      # Add this selection to our pfTau selectors
      applyPostfix(process,"pfTaus", postfix).discriminators.append(cms.PSet(
         discriminator=cms.InputTag(clonedName), selectionCut=cms.double(0.5)))
      # Set the input of the final selector.
      if tauType != 'hpsPFTau':
          applyPostfix(process,"pfTaus", postfix).src = "pfTausBase"+postfix
      else:
          # If we are using HPS taus, we need to take the output of the clenaed
          # collection
          applyPostfix(process,"pfTaus", postfix).src = "hpsPFTauProducer"+postfix



def adaptPFTaus(process,tauType = 'shrinkingConePFTau', postfix = ""):
    # Set up the collection used as a preselection to use this tau type
    if tauType != 'hpsPFTau' :
        reconfigurePF2PATTaus(process, tauType, postfix=postfix)
    else:
        reconfigurePF2PATTaus(process, tauType,
                              ["DiscriminationByLooseCombinedIsolationDBSumPtCorr"],
                              ["DiscriminationByDecayModeFinding"],
                              postfix=postfix)
    # new default use unselected taus (selected only for jet cleaning)
    if tauType != 'hpsPFTau' :
        applyPostfix(process,"patTaus", postfix).tauSource = cms.InputTag("pfTausBase"+postfix)
    else:
        applyPostfix(process,"patTaus", postfix).tauSource = cms.InputTag("hpsPFTauProducer"+postfix)
    # to use preselected collection (old default) uncomment line below
    #applyPostfix(process,"patTaus", postfix).tauSource = cms.InputTag("pfTaus"+postfix)


    #redoPFTauDiscriminators(process,
                            #cms.InputTag(tauType+'Producer'),
                            #applyPostfix(process,"patTaus", postfix).tauSource,
                            #tauType, postfix=postfix)
    #print "hier du nase"
    print applyPostfix(process,"patTaus", postfix).tauSource
    
    if tauType != 'hpsPFTau' :
	switchToPFTauByType(process, pfTauType=tauType,
				patTauLabel="pfTausBase"+postfix,
				tauSource=cms.InputTag(tauType+'Producer'),
				postfix=postfix)	    
        #applyPostfix(process,"patTaus", postfix).tauSource = cms.InputTag("pfTausBase"+postfix)
    else:
	switchToPFTauByType(process, pfTauType=tauType,
				patTauLabel="",
				tauSource=cms.InputTag(tauType+'Producer'),
				postfix=postfix)	    
        #applyPostfix(process,"patTaus", postfix).tauSource = cms.InputTag("hpsPFTauProducer"+postfix)    


    #applyPostfix(process,"patPF2PATSequence", postfix).remove(
        #applyPostfix(process,"patPFCandidateIsoDepositSelection", postfix)
        #)

#helper function for PAT on PF2PAT sample
def tauTypeInPF2PAT(process,tauType='shrinkingConePFTau', postfix = ""):
    process.load("CommonTools.ParticleFlow.pfTaus_cff")
    applyPostfix(process, "pfTaus",postfix).src = cms.InputTag(tauType+'Producer'+postfix)


def addPFCandidates(process,src,patLabel='PFParticles',cut="",postfix=""):
    from PhysicsTools.PatAlgos.producersLayer1.pfParticleProducer_cfi import patPFParticles
    # make modules
    producer = patPFParticles.clone(pfCandidateSource = src)
    filter   = cms.EDFilter("PATPFParticleSelector",
                    src = cms.InputTag("pat" + patLabel),
                    cut = cms.string(cut))
    counter  = cms.EDFilter("PATCandViewCountFilter",
                    minNumber = cms.uint32(0),
                    maxNumber = cms.uint32(999999),
                    src       = cms.InputTag("pat" + patLabel))
    # add modules to process
    setattr(process, "pat"         + patLabel, producer)
    setattr(process, "selectedPat" + patLabel, filter)
    setattr(process, "countPat"    + patLabel, counter)
    # insert into sequence
    getattr(process, "patPF2PATSequence"+postfix).replace(
        applyPostfix(process, "patCandidateSummary", postfix),
        producer+applyPostfix(process, "patCandidateSummary", postfix)
    )
    getattr(process, "patPF2PATSequence"+postfix).replace(
        applyPostfix(process, "selectedPatCandidateSummary", postfix),
        filter+applyPostfix(process, "selectedPatCandidateSummary", postfix)
    )
    index = len( applyPostfix( process, "patPF2PATSequence", postfix ).moduleNames() )
    applyPostfix( process, "patPF2PATSequence", postfix ).insert( index, counter )
    # summary tables
    applyPostfix(process, "patCandidateSummary", postfix).candidates.append(cms.InputTag('pat' + patLabel))
    applyPostfix(process, "selectedPatCandidateSummary", postfix).candidates.append(cms.InputTag('selectedPat' + patLabel))


def switchToPFMET(process,input=cms.InputTag('pfMET'), type1=False, postfix=""):
    print 'MET: using ', input
    if( not type1 ):
        oldMETSource = applyPostfix(process, "patMETs",postfix).metSource
        applyPostfix(process, "patMETs",postfix).metSource = input
        applyPostfix(process, "patMETs",postfix).addMuonCorrections = False
        #getattr(process, "patPF2PATSequence"+postfix).remove(applyPostfix(process, "patMETCorrections",postfix))
    else:
        # type1 corrected MET
        # name of corrected MET hardcoded in PAT and meaningless
        print 'Apply TypeI corrections for MET'
        #getattr(process, "patPF2PATSequence"+postfix).remove(applyPostfix(process, "patMETCorrections",postfix))
        jecLabel = getattr(process,'patJetCorrFactors'+postfix).payload.pythonValue().replace("'","")
        getattr(process,jecLabel+'CorMet'+postfix).inputUncorMetLabel = input.getModuleLabel()
        getattr(process,'patMETs'+postfix).metSource = jecLabel+'CorMet'+postfix
        getattr(process,'patMETs'+postfix).addMuonCorrections = False

def switchToPFJets(process, input=cms.InputTag('pfNoTauClones'), algo='AK5', postfix = "", jetCorrections=('AK5PFchs', ['L1FastJet','L2Relative', 'L3Absolute']), type1=False, outputModules=['out']):

    print "Switching to PFJets,  ", algo
    print "************************ "
    print "input collection: ", input

    if( algo == 'IC5' ):
        genJetCollection = cms.InputTag('iterativeCone5GenJetsNoNu')
    elif algo == 'AK5':
        genJetCollection = cms.InputTag('ak5GenJetsNoNu')
    elif algo == 'AK7':
        genJetCollection = cms.InputTag('ak7GenJetsNoNu')
    else:
        print 'bad jet algorithm:', algo, '! for now, only IC5, AK5 and AK7 are allowed. If you need other algorithms, please contact Colin'
        sys.exit(1)

    # changing the jet collection in PF2PAT:
    from CommonTools.ParticleFlow.Tools.jetTools import jetAlgo
    inputCollection = getattr(process,"pfJets"+postfix).src
    setattr(process,"pfJets"+postfix,jetAlgo(algo)) # problem for cfgBrowser
    getattr(process,"pfJets"+postfix).src = inputCollection
    inputJetCorrLabel=jetCorrections
    #switchJetCollection(process,
                        #input,
                        #jetIdLabel = algo,
                        #doJTA=True,
                        #doBTagging=True,
                        #jetCorrLabel=inputJetCorrLabel,
                        #doType1MET=type1,
                        #genJetCollection = genJetCollection,
                        #doJetID = True,
			#postfix = postfix,
                        #outputModules = outputModules
                        #)
    print inputJetCorrLabel
    switchJetCollection(process,
                        jetSource = input,
                        jetTrackAssociation=True,
                        jetCorrections=inputJetCorrLabel,
                        outputModules = outputModules,
                        )
    print "hallo22"			
    # check whether L1FastJet is in the list of correction levels or not
    applyPostfix(process, "patJetCorrFactors", postfix).useRho = False
    for corr in inputJetCorrLabel[1]:
        if corr == 'L1FastJet':
            applyPostfix(process, "patJetCorrFactors", postfix).useRho = True
            applyPostfix(process, "pfJets", postfix).doAreaFastjet = True
            # do correct treatment for TypeI MET corrections
	    #type1=True
            if type1:
                #for mod in getattr(process,'patPF2PATSequence'+postfix).moduleNames():
		print "searching something"
                for mod in modulesInPath(process,path):
		    print "found something"	
			
                    if mod.startswith("kt6"):
                        prefix = mod.replace(postfix,'')
                        prefix = prefix.replace('kt6PFJets','')
                        prefix = prefix.replace('kt6CaloJets','')
                        prefix = getattr(process,'patJetCorrFactors'+prefix+postfix).payload.pythonValue().replace("'","")
                        for essource in process.es_sources_().keys():
                            if essource == prefix+'L1FastJet':
                                setattr(process,essource+postfix,getattr(process,essource).clone(srcRho=cms.InputTag(mod,'rho')))
                                setattr(process,prefix+'CombinedCorrector'+postfix,getattr(process,prefix+'CombinedCorrector').clone())
                                getattr(process,prefix+'CorMet'+postfix).corrector = prefix+'CombinedCorrector'+postfix
                                for cor in getattr(process,prefix+'CombinedCorrector'+postfix).correctors:
                                    if cor == essource:
                                        idx = getattr(process,prefix+'CombinedCorrector'+postfix).correctors.index(essource);
                                        getattr(process,prefix+'CombinedCorrector'+postfix).correctors[idx] = essource+postfix

    if hasattr( getattr( process, "patJets" + postfix), 'embedCaloTowers' ): # optional parameter, which defaults to 'False' anyway
        applyPostfix(process, "patJets", postfix).embedCaloTowers = False
    applyPostfix(process, "patJets", postfix).embedPFCandidates = True

#-- Remove MC dependence ------------------------------------------------------
def removeMCMatchingPF2PAT( process, postfix="", outputModules=['out'] ):
    #from PhysicsTools.PatAlgos.tools.coreTools import removeMCMatching
    #removeIfInSequence(process, "genForPF2PATSequence", "patDefaultSequence", postfix)
    removeMCMatching(process, names=['All'], postfix=postfix, outputModules=outputModules)


def adaptPVs(process, pvCollection=cms.InputTag('offlinePrimaryVertices'), postfix=''):

    print "Switching PV collection for PF2PAT:", pvCollection
    print "***********************************"

    # PV sources to be exchanged:
    pvExchange = ['Vertices','vertices','pvSrc','primaryVertices','srcPVs']
    # PV sources NOT to be exchanged:
    #noPvExchange = ['src','PVProducer','primaryVertexSrc','vertexSrc','primaryVertex']

    # find out all added jet collections (they don't belong to PF2PAT)
    interPostfixes = []
    for m in getattr(process,'patPF2PATSequence'+postfix).moduleNames():
        if m.startswith('patJets') and m.endswith(postfix) and not len(m)==len('patJets')+len(postfix):
            interPostfix = m.replace('patJets','')
            interPostfix = interPostfix.replace(postfix,'')
            interPostfixes.append(interPostfix)

    # exchange the primary vertex source of all relevant modules
    for m in getattr(process,'patPF2PATSequence'+postfix).moduleNames():
        modName = m.replace(postfix,'')
        # only if the module has a source with a relevant name
        for namePvSrc in pvExchange:
            if hasattr(getattr(process,m),namePvSrc):
                # only if the module is not coming from an added jet collection
                interPostFixFlag = False
                for pfix in interPostfixes:
                    if modName.endswith(pfix):
                        interPostFixFlag = True
                        break
                if not interPostFixFlag:
                    setattr(getattr(process,m),namePvSrc,deepcopy(pvCollection))


def usePF2PAT(process,runPF2PAT=True, jetAlgo='ak5', runOnMC=True, postfix="", jetCorrections=('AK5PFchs', ['L1FastJet','L2Relative','L3Absolute'],'None'), pvCollection=cms.InputTag('offlinePrimaryVertices'), typeIMetCorrections=False, outputModules=['out']):
    # PLEASE DO NOT CLOBBER THIS FUNCTION WITH CODE SPECIFIC TO A GIVEN PHYSICS OBJECT.
    # CREATE ADDITIONAL FUNCTIONS IF NEEDED.

    """Switch PAT to use PF2PAT instead of AOD sources. if 'runPF2PAT' is true, we'll also add PF2PAT in front of the PAT sequence"""

    # -------- CORE ---------------
   
    if runPF2PAT:
        process.load("CommonTools.ParticleFlow.PF2PAT_cff")
        #add Pf2PAT *before* cloning so that overlapping modules are cloned too
        #process.patDefaultSequence.replace( process.patCandidates, process.PF2PAT+process.patCandidates)
        #add clones of some stuff here
        process.patPFClones = cms.Sequence(process.pfNoJetClones+process.pfNoTauClones)
        process.patPF2PATSequence = cms.Sequence( process.PF2PAT + process.patPFClones + process.patDefaultSequence)
    else:
        process.patPF2PATSequence = cms.Sequence( process.patDefaultSequence )

    if not postfix == "":
	print "here4?"    
        from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
	
        #cloneProcessingSnippet(process, process.patPF2PATSequence,"")
        cloneProcessingSnippet(process, process.patPF2PATSequence, postfix)
	#applyPostfix(process,"countPatCandidates",postfix)
	#getattr(process,path)+=process.patPF2PATSequence	
	print "here5?"
	#print process.patPF2PATSequence
	#print process.patDefaultSequence
        #delete everything pat PF2PAT modules! if you want to test the postfixing for completeness
        #from PhysicsTools.PatAlgos.tools.helpers import listModules,listSequences
        #for module in listModules(process.patDefaultSequence):
        #    if not module.label() is None: process.__delattr__(module.label())
        #for sequence in listSequences(process.patDefaultSequence):
        #    if not sequence.label() is None: process.__delattr__(sequence.label())
        #del process.patDefaultSequence
    process.countPatCandidatesPFlow = cms.Sequence(process.countPatElectronsPFlow+process.countPatMuonsPFlow+process.countPatTausPFlow+process.countPatLeptonsPFlow+process.countPatPhotonsPFlow+process.countPatJetsPFlow)	
    removeCleaning(process, postfix=postfix, outputModules=outputModules)

    # -------- OBJECTS ------------
    # Muons
    print "here6?"
    adaptPFMuons(process,
                 applyPostfix(process,"patMuons",postfix),
                 postfix)

    # Electrons
    print "here7?"
    adaptPFElectrons(process,
                     applyPostfix(process,"patElectrons",postfix),
                     postfix)

    # Photons
    print "Temporarily switching off photons completely"

    removeSpecificPATObjects(process,names=['Photons'],outputModules=outputModules,postfix=postfix)
    removeIfInSequence(process,"patPhotonIsolation","patPF2PATSequence",postfix)

    # Jets
    if runOnMC :
        switchToPFJets( process, cms.InputTag('pfNoTauClones'+postfix), jetAlgo, postfix=postfix,
                        jetCorrections=jetCorrections, type1=typeIMetCorrections, outputModules=outputModules )
        #applyPostfix(process,"patPF2PATSequence",postfix).replace(
            #applyPostfix(process,"patJetGenJetMatch",postfix),
            #getattr(process,"patPF2PATSequence") *
            #applyPostfix(process,"patJetGenJetMatch",postfix)
            #)
    else :
        if not 'L2L3Residual' in jetCorrections[1]:
            print '#################################################'
            print 'WARNING! Not using L2L3Residual but this is data.'
            print 'If this is okay with you, disregard this message.'
            print '#################################################'
        switchToPFJets( process, cms.InputTag('pfNoTauClones'+postfix), jetAlgo, postfix=postfix,
                        jetCorrections=jetCorrections, type1=typeIMetCorrections, outputModules=outputModules )
    print "here9?"	
    # Taus
    #adaptPFTaus( process, tauType='shrinkingConePFTau', postfix=postfix )
    #adaptPFTaus( process, tauType='fixedConePFTau', postfix=postfix )
    adaptPFTaus( process, tauType='hpsPFTau', postfix=postfix )
    print "here10?" 	
    # MET
    switchToPFMET(process, cms.InputTag('pfMET'+postfix), type1=typeIMetCorrections, postfix=postfix)

    # Unmasked PFCandidates
    addPFCandidates(process,cms.InputTag('pfNoJetClones'+postfix),patLabel='PFParticles'+postfix,cut="",postfix=postfix)

    # adapt primary vertex collection
    adaptPVs(process, pvCollection=pvCollection, postfix=postfix)

    if runOnMC:
        process.load("CommonTools.ParticleFlow.genForPF2PAT_cff")
        #getattr(process, "patPF2PATSequence"+postfix).replace(
            #applyPostfix(process,"patCandidates",postfix),
            #process.genForPF2PATSequence+applyPostfix(process,"patCandidates",postfix)
            #)
    else:
        removeMCMatchingPF2PAT(process,postfix=postfix,outputModules=outputModules)

    print "Done: PF2PAT interfaced to PAT, postfix=", postfix


class RemoveCleaning(ConfigToolBase):

    """ remove PAT cleaning from the default sequence:
    """
    _label='removeCleaning'
    _defaultParameters=dicttypes.SortedKeysDict()
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'outputModules',['out'], "names of all output modules specified to be adapted (default is ['out'])")
        self.addParameter(self._defaultParameters,'postfix',"", "postfix of default sequence")
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""

    def getDefaultParameters(self):
        return self._defaultParameters

    def __call__(self,process,
                 outputInProcess = None,
                 postfix         = None,
                 outputModules   = None) :
        ## stop processing if 'outputInProcess' exists and show the new alternative
        if  not outputInProcess is None:
            depricatedOptionOutputInProcess(self)
        if  outputModules is None:
            outputModules=self._defaultParameters['outputModules'].value
        if postfix  is None:
            postfix=self._defaultParameters['postfix'].value

        self.setParameter('outputModules',outputModules)
        self.setParameter('postfix',postfix)

        self.apply(process)

    def toolCode(self, process):
        outputModules=self._parameters['outputModules'].value
        postfix=self._parameters['postfix'].value

        ## adapt single object counters
        for m in listModules(applyPostfix(process,"countPatCandidates",postfix)):
            if hasattr(m, 'src'): m.src = m.src.value().replace('cleanPat','selectedPat')

        ## adapt lepton counter
        countLept = applyPostfix(process,"countPatLeptons",postfix)
        countLept.electronSource = countLept.electronSource.value().replace('cleanPat','selectedPat')
        countLept.muonSource = countLept.muonSource.value().replace('cleanPat','selectedPat')
        countLept.tauSource = countLept.tauSource.value().replace('cleanPat','selectedPat')
        #for m in getattr(process, "cleanPatCandidates").moduleNames():
            #getattr(process, "patDefaultSequence"+postfix).remove(
                #applyPostfix(process,m,postfix)
                #)
        if len(outputModules) > 0:
            print "------------------------------------------------------------"
            print "INFO   : cleaning has been removed. Switching output from"
            print "         clean PAT candidates to selected PAT candidates."
            ## add selected pat objects to the pat output
            from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
            for outMod in outputModules:
                if hasattr(process,outMod):
                    getattr(process,outMod).outputCommands = patEventContentNoCleaning
                else:
                    raise KeyError, "process has no OutModule named", outMod

removeCleaning=RemoveCleaning()



class RemoveSpecificPATObjects(ConfigToolBase):

    """ Remove a specific PAT object from the default sequence
    """
    _label='removeSpecificPATObjects'
    _defaultParameters=dicttypes.SortedKeysDict()
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'names',self._defaultValue, "list of collection names; supported are 'Photons', 'Electrons', 'Muons', 'Taus', 'Jets', 'METs'", Type=list, allowedValues=['Photons', 'Electrons', 'Muons', 'Taus', 'Jets', 'METs'])
        self.addParameter(self._defaultParameters,'outputModules',['out'], "names of all output modules specified to be adapted (default is ['out'])")
        self.addParameter(self._defaultParameters,'postfix',"", "postfix of default sequence")
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""

    def getDefaultParameters(self):
        return self._defaultParameters

    def __call__(self,process,
                 names           = None,
                 outputInProcess = None,
                 postfix         = None,
                 outputModules   = None) :
        ## stop processing if 'outputInProcess' exists and show the new alternative
        if  not outputInProcess is None:
            depricatedOptionOutputInProcess(self)
        if  names is None:
            names=self._defaultParameters['names'].value
        if  outputModules is None:
            outputModules=self._defaultParameters['outputModules'].value
        if postfix  is None:
            postfix=self._defaultParameters['postfix'].value
        self.setParameter('names',names)
        self.setParameter('outputModules',outputModules)
        self.setParameter('postfix',postfix)
        self.apply(process)

    def toolCode(self, process):
        names=self._parameters['names'].value
        outputModules=self._parameters['outputModules'].value
        postfix=self._parameters['postfix'].value

        ## remove pre object production steps from the default sequence
        for obj in range(len(names)):
            if( names[obj] == 'Photons' ):
                removeIfInSequence(process, 'patPhotonIsolation', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'photonMatch', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'patPhotons', "patPF2PATSequence", postfix)
            if( names[obj] == 'Electrons' ):
                removeIfInSequence(process, 'patElectronId', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'patElectronIsolation', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'electronMatch', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'patElectrons', "patPF2PATSequence", postfix)
            if( names[obj] == 'Muons' ):
                removeIfInSequence(process, 'muonMatch', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'patMuons', "patPF2PATSequence", postfix)
            if( names[obj] == 'Taus' ):
                removeIfInSequence(process, 'patPFCandidateIsoDepositSelection', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'patPFTauIsolation', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'tauMatch', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'tauGenJets', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'tauGenJetsSelectorAllHadrons', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'tauGenJetMatch', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'patTaus', "patPF2PATSequence", postfix)
            if( names[obj] == 'Jets' ):
                removeIfInSequence(process, 'patJetCharge', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'patJetCorrections', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'patJetPartonMatch', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'patJetGenJetMatch', "patPF2PATSequence", postfix)
                removeIfInSequence(process, 'patJetFlavourId', "patPF2PATSequence", postfix)
            if( names[obj] == 'METs' ):
                removeIfInSequence(process, 'patMETCorrections', "patPF2PATSequence", postfix)

            ## remove object production steps from the default sequence
            if( names[obj] == 'METs' ):
                process.patDefaultSequence.remove( getattr(process, 'pat'+names[obj]) )
            else:
                if( names[obj] == 'Jets' ):
                    applyPostfix(process,"patPF2PATSequence",postfix).remove(
                        getattr(process, jetCollectionString()+postfix) )
                    applyPostfix(process,"patPF2PATSequence",postfix).remove(
                        getattr(process, jetCollectionString('selected')+postfix) )
                    applyPostfix(process,"patPF2PATSequence",postfix).remove(
                        getattr(process, jetCollectionString('count')+postfix) )
                else:
                    applyPostfix(process,"patPF2PATSequence",postfix).remove(
                        getattr(process, 'pat'+names[obj]+postfix) )
                    applyPostfix(process,"patPF2PATSequence",postfix).remove(
                        getattr(process, 'selectedPat'+names[obj]+postfix) )
                    applyPostfix(process,"patPF2PATSequence",postfix).remove(
                        getattr(process, 'countPat'+names[obj]+postfix) )
            ## in the case of leptons, the lepton counter must be modified as well
            if( names[obj] == 'Electrons' ):
                print 'removed from lepton counter: electrons'
                applyPostfix(process,"countPatLeptons",postfix).countElectrons = False
            elif( names[obj] == 'Muons' ):
                print 'removed from lepton counter: muons'
                applyPostfix(process,"countPatLeptons",postfix).countMuons = False
            elif( names[obj] == 'Taus' ):
                print 'removed from lepton counter: taus'
                applyPostfix(process,"countPatLeptons",postfix).countTaus = False
            ## remove from summary
            if( names[obj] == 'METs' ):
                applyPostfix(process,"patCandidateSummary",postfix).candidates.remove(
                    cms.InputTag('pat'+names[obj]+postfix) )
            else:
                if( names[obj] == 'Jets' ):
                    applyPostfix(process,"patCandidateSummary",postfix).candidates.remove(
                        cms.InputTag(jetCollectionString()+postfix) )
                    applyPostfix(process,"selectedPatCandidateSummary",postfix).candidates.remove(
                        cms.InputTag(jetCollectionString('selected')+postfix) )
                    applyPostfix(process,"cleanPatCandidateSummary",postfix).candidates.remove(
                        cms.InputTag(jetCollectionString('clean')+postfix) )
                else:
                    ## check whether module is in sequence or not
                    result = [ m.label()[:-len(postfix)] for m in listModules( getattr(process,"patPF2PATSequence"+postfix))]
                    result.extend([ m.label()[:-len(postfix)] for m in listSequences( getattr(process,"patPF2PATSequence"+postfix))]  )
                    if applyPostfix(process,"patCandidateSummary",postfix) in result :
                        applyPostfix(process,"patCandidateSummary",postfix).candidates.remove(
                            cms.InputTag('pat'+names[obj]+postfix) )
                    if applyPostfix(process,"selectedPatCandidateSummary",postfix) in result :
                        applyPostfix(process,"selectedPatCandidateSummary",postfix).candidates.remove(
                            cms.InputTag('selectedPat'+names[obj]+postfix) )
                    if applyPostfix(process,"cleanPatCandidateSummary",postfix) in result :
                        applyPostfix(process,"cleanPatCandidateSummary",postfix).candidates.remove(
                            cms.InputTag('cleanPat'+names[obj]+postfix) )
        ## remove cleaning for the moment; in principle only the removed object
        ## could be taken out of the checkOverlaps PSet
        if len(outputModules) > 0:
            print "---------------------------------------------------------------------"
            print "INFO   : some objects have been removed from the sequence. Switching "
            print "         off PAT cross collection cleaning, as it might be of limited"
            print "         sense now. If you still want to keep object collection cross"
            print "         cleaning within PAT you need to run and configure it by hand"
            #removeCleaning(process,outputModules=outputModules,postfix=postfix)

removeSpecificPATObjects=RemoveSpecificPATObjects()


class RemoveMCMatching(ConfigToolBase):

    """ Remove monte carlo matching from a given collection or all PAT
    candidate collections:
    """
    _label='removeMCMatching'
    _defaultParameters=dicttypes.SortedKeysDict()
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'names',['All'], "collection name; supported are 'Photons', 'Electrons','Muons', 'Taus', 'Jets', 'METs', 'All', 'PFAll', 'PFElectrons','PFTaus','PFMuons'", allowedValues=['Photons', 'Electrons','Muons', 'Taus', 'Jets', 'METs', 'All', 'PFAll', 'PFElectrons','PFTaus','PFMuons'])
        self.addParameter(self._defaultParameters,'postfix',"", "postfix of default sequence")
        self.addParameter(self._defaultParameters,'outputInProcess',True, "indicates whether the output of the pat tuple should be made persistent or not (legacy)")
        self.addParameter(self._defaultParameters,'outputModules',['out'], "names of all output modules specified to be adapted (default is ['out'])")
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""

    def getDefaultParameters(self):
        return self._defaultParameters

    def __call__(self,process,
                 names           = None,
                 postfix         = None,
                 outputInProcess = None,
                 outputModules   = None) :
        ## stop processing if 'outputInProcess' exists and show the new alternative
        if  not outputInProcess is None:
            depricatedOptionOutputInProcess(self)
        else:
            outputInProcess=self._parameters['outputInProcess'].value
        if  names is None:
            names=self._defaultParameters['names'].value
        if postfix  is None:
            postfix=self._defaultParameters['postfix'].value
        if  outputModules is None:
            outputModules=self._defaultParameters['outputModules'].value
        self.setParameter('names',names)
        self.setParameter('postfix',postfix)
        self.setParameter('outputInProcess', outputInProcess)
        self.setParameter('outputModules',outputModules)
        self.apply(process)

    def toolCode(self, process):
        names=self._parameters['names'].value
        postfix=self._parameters['postfix'].value
        outputInProcess=self._parameters['outputInProcess'].value
        outputModules=self._parameters['outputModules'].value

        if not outputInProcess:
            outputModules=['']
        
        print "************** MC dependence removal ************"
        for obj in range(len(names)):
            if( names[obj] == 'Photons'   or names[obj] == 'All' ):
                print "removing MC dependencies for photons"
                _removeMCMatchingForPATObject(process, 'photonMatch', 'patPhotons', postfix)
            if( names[obj] == 'Electrons' or names[obj] == 'All' ):
                print "removing MC dependencies for electrons"
                _removeMCMatchingForPATObject(process, 'electronMatch', 'patElectrons', postfix)
            if( names[obj] == 'Muons'     or names[obj] == 'All' ):
                print "removing MC dependencies for muons"
                _removeMCMatchingForPATObject(process, 'muonMatch', 'patMuons', postfix)
            if( names[obj] == 'Taus'      or names[obj] == 'All' ):
                print "removing MC dependencies for taus"
                _removeMCMatchingForPATObject(process, 'tauMatch', 'patTaus', postfix)
                ## remove mc extra modules for taus
                for mod in ['tauGenJets','tauGenJetsSelectorAllHadrons','tauGenJetMatch']:
                    if hasattr(process,mod+postfix):
                        getattr(process,'patDefaultSequence'+postfix).remove(getattr(process,mod+postfix))
                ## remove mc extra configs for taus
                tauProducer = getattr(process,'patTaus'+postfix)
                tauProducer.addGenJetMatch   = False
                tauProducer.embedGenJetMatch = False
                tauProducer.genJetMatch      = ''
            if( names[obj] == 'Jets'      or names[obj] == 'All' ):
                print "removing MC dependencies for jets"
                ## there may be multiple jet collection, therefore all jet collections
                ## in patDefaultSequence+postfix are threated here
                jetPostfixes = []
                for mod in getattr(process,'patDefaultSequence'+postfix).moduleNames():
                    if mod.startswith('patJets'):
                        jetPostfixes.append(getattr(process, mod).label_().replace("patJets",""))
                for pfix in jetPostfixes:
                    ## remove mc extra modules for jets
                    for mod in ['patJetPartonMatch','patJetGenJetMatch','patJetFlavourId','patJetPartons','patJetPartonAssociation','patJetFlavourAssociation']:
                        if hasattr(process,mod+pfix):
                            getattr(process,'patDefaultSequence'+postfix).remove(getattr(process,mod+pfix))
                    ## remove mc extra configs for jets
                    jetProducer = getattr(process, jetCollectionString()+pfix)
                    jetProducer.addGenPartonMatch   = False
                    jetProducer.embedGenPartonMatch = False
                    jetProducer.genPartonMatch      = ''
                    jetProducer.addGenJetMatch      = False
                    jetProducer.genJetMatch         = ''
                    jetProducer.getJetMCFlavour     = False
                    jetProducer.JetPartonMapSource  = ''
                ## adjust output
                for outMod in outputModules:
                    if hasattr(process,outMod):
                        getattr(process,outMod).outputCommands.append("drop *_selectedPatJets*_genJets_*")
                    else:
                        raise KeyError, "process has no OutModule named", outMod

            if( names[obj] == 'METs'      or names[obj] == 'All' ):
                ## remove mc extra configs for jets
                metProducer = getattr(process, 'patMETs'+postfix)
                metProducer.addGenMET           = False
                metProducer.genMETSource        = ''

removeMCMatching=RemoveMCMatching()