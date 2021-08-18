// -*- C++ -*-
#include "Rivet/Analyses/MC_JetSplittings.hh"
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Projections/VetoedFinalState.hh"

namespace Rivet {




  /// @brief MC validation analysis for higgs [-> tau tau] + jets events
  class MC_H_KTSPLITTINGS : public MC_JetSplittings {
  public:

    /// Default constructor
    MC_H_KTSPLITTINGS()
      : MC_JetSplittings("MC_H_KTSPLITTINGS", 4, "Jets")
    {    }


    /// @name Analysis methods
    //@{

    /// Book histograms
    void init() {
      FinalState fs;
      IdentifiedFinalState higgses(PID::HIGGS);
      IdentifiedFinalState photons(PID::PHOTON);
      VetoedFinalState rest(fs);
      rest.addVetoOnThisFinalState(higgses);
      rest.addVetoOnThisFinalState(photons);
      //rest.addVetoId(82);
      declare(fs, "FS");
      declare(higgses, "Higgses");
      declare(photons, "Photons");
      declare(rest, "Rest");
      FastJets jetpro(rest, FastJets::KT,0.6);     
      //FastJets jetpro(hfinder.remainingFinalState(), FastJets::KT, 0.6);
      declare(jetpro, "Jets");

      MC_JetSplittings::init();
    }



    /// Do the analysis
    void analyze(const Event & e) {
       // Get the final state particles ordered by pT
      const Particles& fs = apply<FinalState>(e, "FS").particlesByPt();

      // Find a stable Higgs (mandatory)
      const auto higgsiter = std::find_if(fs.begin(), fs.end(), [](const Particle& p){ return p.pid() == PID::HIGGSBOSON; });
      if (higgsiter == fs.end()) vetoEvent;
      MC_JetSplittings::analyze(e);
    }


    /// Finalize
    void finalize() {
      MC_JetSplittings::finalize();
    }

    //@}

  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(MC_H_KTSPLITTINGS);

}
