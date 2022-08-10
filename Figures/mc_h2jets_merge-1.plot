# BEGIN SPECIAL /*/*
\rput[tl](0.05,0.75){\parbox{5cm}{\textcolor{gray}{{\bf Herwig 7.2.0} \\ HJETS/ColorFull}}}
# END SPECIAL

# BEGIN PLOT /MC_H2JETS_04*/*
RightMargin=0.5
Scale=1000.0
Legend=0
LegendAlign=l
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H_KTSPLITTINGS/*
RightMargin=0.5
Scale=1000.0
Legend=0
LegendAlign=l
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet3_x
YLabel=$\text{d} \sigma/ \text{d} x_{j_3}^{\star}$ (fb)
XLabel=$x_{j_3}^{\star}$
RatioPlotYMin=0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/H_dijet_mass
YLabel=$ \text{d} \sigma/ \text{d}  \Delta m_{h,j_1j_2}$ (fb/GeV)
XLabel=$m_{h,j_1j_2}$ (GeV)
XMin=700.0
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet4_x
YLabel=$\text{d} \sigma/ \text{d} x_{j_4}^{\star}$ (fb)
XLabel=$x_{j_4}^{\star}$
RatioPlotYMin=0.2
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/gapjet1_y_incl

YLabel=$\text{d} \sigma/ \text{d} y_{jets}^{gap}$
XLabel=$y_{jets}^{gap}$
RatioPlotYMin=0.0
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/H_jj_pT_incl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2}^{incl}$ (GeV)
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/HT_jets
YLabel=$ \text{d} \sigma/ \text{d}  H_{T}(\text{jets})$ (fb/GeV)
XLabel=$H_{T}(\text{jets})$ (GeV)
XMax=1000
RaiotPlotYMin=0.5
RaiotPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/gapjet1_pt_incl
YLabel=$\text{d} \sigma/ \text{d} P_{T,jets}^{gap}$
XLabel=$p_{T,jets}^{gap}$ (GeV)
XMin=0.0
XMax=200.0
RatioPlotYMin=0.0
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j2_pullangle

YLabel=$\text{d} \sigma/ \text{d} \theta_{j1,j2}$ (fb)
XLabel=$\theta_{j1,j2}$ $(rad/\pi)$
RatioPlotYMin=0.8
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j2j3_pullangle

YLabel=$\text{d} \sigma/ \text{d} \theta_{j2,j3}$ (fb)
XLabel=$\theta_{j2,j3}$ $(rad/\pi)$
RatioPlotYMin=0.6
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j3_pullangle

YLabel=$\text{d} \sigma/ \text{d} \theta_{j1,j3}$ (fb)
XLabel=$\theta_{j1,j3}$ $(rad/\pi)$
RatioPlotYMin=0.0
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/HT_gapjets
YLabel=$\text{d} \sigma/ \text{d} H_{T,jets}^\text{gap}$ (fb/GeV)
XLabel=$H_{T,jets}^\text{gap}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/avgNGapJets_ht
YLabel=$\langle N_{gap} \rangle$
XLabel=$H_{T}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/avgNGapJets_dy

YLabel=$\langle N_{gap} \rangle$
XLabel=$\Delta y_{j_1j_2}$
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/y1j_yj2

YLabel=$ \text{d} \sigma/ \text{d}  y_{j_1}*y_{j_2}$ (fb)
XLabel=$y_{j_1}*y_{j_2}$
RatioPlotYMin=0.2
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/avgNGapJets_mjj

YLabel=$\langle N_{gap} \rangle$
XLabel=$m_{j_1j_2}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/avgNGapJets_pt
YLabel=$\langle N_{gap} \rangle$ 
XLabel=$\overline{P_{T,j_1j_2}}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/NGapJet_incl
YLabel=$ \sigma_{\text{fid}, > N_{jets}^{gap}}$ 
XLabel=$>N_{jets}^{gap}$
XMax=6.0
RatioPlotYMax=2.0
RatioPlotYMin=0.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/NGapJet_excl
YLabel=$\sigma_{\text{fid}, N_{jets}^{gap}}$ 
XLabel=$N_{jets}^{gap}$
XMax=6.0
RatioPlotYMax=2.0
RatioPlotYMin=0.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/Hj_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,hj_1}^{incl}$ (fb/GeV)
XLabel=$p_{T,hj_1}^{incl}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/Hjj_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,hj_1j_2}$ (fb/GeV)
XLabel=$p_{T,hj_1j_2}$ (GeV)
XMax=200.0
RatioPlotYMax=2.0
RatioPlotYMin=0.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/Hjj_pT_excl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,hj_1j_2}^{excl}$ (fb/GeV)
XLabel=$p_{T,hj_1j_2}^{excl}$ (GeV)
XMax=150.0
RatioPlotYMin=0.0
RatioPlotYMax=4.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/H_j_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,>Njets}$ (fb/GeV)
XLabel=$p_{T,>Njets}$ (GeV)
RatioPlotYMax=1.5
RatioPlotYMin=0.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/H_jj_pT_excl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2}^{excl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2}^{excl}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/H_jjj_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2j_3}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2j_3}^{incl}$ (GeV)
RatioPlotYMin=0.2
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/H_jjj_pT_excl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2j_3}^{excl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2j_3}^{excl}$ (GeV)
RatioPlotYMin=0.2
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/H_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,h}^{incl}$ (fb/GeV)
XLabel=$p_{T,h}^{incl}$ (GeV)
XMax=300.0
RatioPlotYMax=1.5
RatioPlotYMin=0.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/H_y
YLabel=$ \text{d} \sigma/ \text{d}  y_{h}$ (fb)
XLabel=$y_{h}$ 
RatioPlotYMin=0.2
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/H_y_abs
YLabel=$ \text{d} \sigma/ \text{d}  |y_{h}|$ (fb)
XLabel=$|y_{h}|$
XMax=5.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet1_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_1}^{incl}$ (GeV)
XMax=400.0
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet1_y_abs_incl
YLabel=$ \text{d} \sigma/ \text{d}  |y_{j_1}|$ (fb)
XLabel=$|y_{j_1}|$
XMax=5.0
RatioPlotYMin=0.8
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet1_y_incl
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_1}^{incl}$ (fb)
XLabel=$y_{j_1}^{incl}$
XMax=5.0
RatioPlotYMin=0.8
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet2_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_2}$ (fb/GeV)
XLabel=$p_{T,j_2}$ (GeV)
XMax=200.0
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/deltay_jj
YLabel=$ \text{d} \sigma/ \text{d}  \Delta y_{j_1j_2}$ (fb)
XLabel=$\Delta y_{j_1j_2}$ 
XMax=9.0
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet2_y_incl
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_2}$ (fb)
XLabel=$y_{j_2}$ 
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet2_y_abs_incl
YLabel=$ \text{d} \sigma/ \text{d}  |y_{j2}|$ (fb)
XLabel=$|y_{j2}|$
XMax=5.0
RatioPlotYMin=0.6
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet3_pT_excl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_3}^{excl}$ (fb/GeV)
XLabel=$p_{T,j_3}^{excl}$ (GeV)
XMax=200.0
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet1_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1}$ (fb/GeV)
XLabel=$m_{j_1}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet4_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_4}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_4}^{incl}$ (GeV)
XMax=150.0
RatioPlotYMin=0.0
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_4}$ (fb/GeV)
XLabel=$m_{j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet3_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_3}$ (fb/GeV)
XLabel=$p_{T,j_3}$ (GeV)
XMax=200.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet3_y
YLabel=$ \text{d} \sigma/ \text{d}  z_{j_3}^{\star}$ (fb)
XLabel=$z_{j_3}^{\star}$ 
RatioPlotYMin=0.5
RatioPlotYMax=1.5
XMin=-4
XMax=4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet3_y_incl
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_3}^{incl}$ (fb)
XLabel=$y_{j_3}^{incl}$ 
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet4_y
YLabel=$ \text{d} \sigma/ \text{d}  z_{j_4}^{\star}$ (fb)
XLabel=$z_{j_4}^{\star}$ 
RatioPlotYMin=0.2
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet4_y_incl
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_4}^{incl}$ (fb)
XLabel=$y_{j_4}^{incl}$ 
RatioPlotYMin=0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet2_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2}$ (fb/GeV)
XLabel=$m_{j_2}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/jet3_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_3}$ (fb/GeV)
XLabel=$m_{j_3}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/deltay_H_jj
YLabel=$ \text{d} \sigma/ \text{d}  \Delta y_{h,j_1j_2}$ (fb)
XLabel=$\Delta y_{h,j_1j_2}$ 
XMax=6.0
RatioPlotYMin=0.6
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/H3_y
YLabel=$ \text{d} \sigma/ \text{d}  y_{h}^{\star}$ (fb)
XLabel=$y_{h}^{\star}$ 
RatioPlotYMin=0.2
RatioPlotYMax=1.8
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/dijet_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2}$ (fb/GeV)
XLabel=$m_{j_1j_2}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/dijet_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2}$ (fb/GeV)
XLabel=$m_{j_1j_2}$ (GeV)
XMax=200.0
RatioPlotYMin=0.6
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/deltaphi_jj_incl
YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{j_1j_2}^{incl}$ (fb)
XLabel=$\Delta \phi_{j_1j_2}^{incl}$ 
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/deltaphi_jj_excl
YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{j_1j_2}^{excl}$ (fb)
XLabel=$\Delta \phi_{j_1j_2}^{excl}$ 
RatioPlotYMin=0.6
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/deltaphi_Hjj_incl
YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{h,j_1j_2}$ (fb)
XLabel=$\Delta \phi_{h,j_1j_2}$ 
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/deltaphi_Hjj_excl
YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{h,j_1j_2}^{excl}$ (fb)
XLabel=$\Delta \phi_{h,j_1j_2}^{excl}$ 
RatioPlotYMin=0.4
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/deltaphi2
YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{2}$ (fb)
XLabel=$\Delta \phi_{2}$ 
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/trijet_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/trijet_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j2j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j2j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j3j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_3j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=1.8
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j3j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_3j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=1.8
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j2j3j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_2j_3j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j2j3j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_2j_3j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j2j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_4}$ (fb/GeV)
XLabel=$m_{j_2j_4}$ (GeV)
XMax=1000
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j2j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_4}$ (fb/GeV)
XLabel=$m_{j_2j_4}$ (GeV)
XMax=200
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j3j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_3j_4}$ (fb/GeV)
XLabel=$m_{j_3j_4}$ (GeV)
XMax=1000
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j3j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_3j_4}$ (fb/GeV)
XLabel=$m_{j_3j_4}$ (GeV)
XMax=200
RatioPlotYMin=0.0
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j2j3_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3}$ (fb/GeV)
XLabel=$m_{j_2j_3}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.0
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j2j3_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3}$ (fb/GeV)
XLabel=$m_{j_2j_3}$ (GeV)
XMax=200.0
RatioPlotYMin=0.6
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_4}$ (fb/GeV)
XLabel=$m_{j_1j_4}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.2
RatioPlotYMax=1.8
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_4}$ (fb/GeV)
XLabel=$m_{j_1j_4}$ (GeV)
XMax=200.0
RatioPlotYMin=0.0
RatioPlotYMax=1.8
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j3_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3}$ (fb/GeV)
XLabel=$m_{j_1j_3}$ (GeV)
XMax=1000
RatioPlotYMin=0.0
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j3_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3}$ (fb/GeV)
XLabel=$m_{j_1j_3}$ (GeV)
XMax=200
RatioPlotYMin=0.0
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/XS
YLabel=$ \sigma_{\text{fid}}$ (fb)
XLabel=
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/NJet_incl
YLabel=$ \sigma_{\text{fid}, > N_{jets}}$ (fb)
XLabel=$>N_{jets}$
XMax=8.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/NJet_excl
YLabel=$ \sigma_{\text{fid}, N_{jets}}$ (fb)
XLabel=$N_{jets}$
XMax=8.0
RatioPlotYMax=2.0
RatioPlotYMin=0.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/log10_R_0
Title=$\log_{10}$(Integrated $0$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{0}$
RatioPlotYMin=0.2
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/log10_R_1
Title=$\log_{10}$(Integrated $0$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{1}$
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/log10_R_2
Title=$\log_{10}$(Integrated $0$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{2}$
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/log10_R_3
Title=$\log_{10}$(Integrated $3$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{3}$
RatioPlotYMin=0.0
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/log10_R_4
Title=$\log_{10}$(Integrated $4$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{\geq4}$
XMax=3.0
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j2j3j4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/j1j2j3j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/HT_all
YLabel=$ \text{d} \sigma/ \text{d}  H_{T}(\text{all})$ (fb/GeV)
XLabel=$H_{T}(\text{all})$ (GeV)
XMax=500.0
RatioPlotYMax=1.6
RatioPlotYMin=0.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/log10_d_01
YLabel=$ \text{d} \sigma / \sqrt{d_{01}}$ (fb/GeV)
XLabel=$\sqrt{d_{01}}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/log10_d_12
YLabel=$ \text{d} \sigma / \sqrt{d_{12}}$ (fb/GeV)
XLabel=$\sqrt{d_{12}}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/log10_d_23
Title=$\log_{10}$($k_\perp$ jet resolution $2 \to 3$ [GeV])
XLabel=$\log_{10}(\sqrt{d_{23}}/\text{GeV})$
YLabel=$\text{d}\sigma/\text{d}\log_{10}(\sqrt{d_{23}}/\text{GeV})$ [fb]
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_INC/log10_d_34
Title=$\log_{10}$($k_\perp$ jet resolution $3 \to 4$ [GeV])
XLabel=$\log_{10}(\sqrt{d_{34}}/\text{GeV})$
YLabel=$\text{d}\sigma/\text{d}\log_{10}(\sqrt{d_{34}}/\text{GeV})$ [fb]
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet3_x
YLabel=$\text{d} \sigma/ \text{d} x_{j_3}^{\star}$ (fb)
XLabel=$x_{j_3}^{\star}$
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet4_x
YLabel=$\text{d} \sigma/ \text{d} x_{j_4}^{\star}$ (fb)
XLabel=$x_{j_4}^{\star}$
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/gapjet1_y_incl
YLabel=$\text{d} \sigma/ \text{d} y_{jets}^{gap}$
XLabel=$y_{jets}^{gap}$
RatioPlotYMin=0.6
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/gapjet1_pt_incl
YLabel=$\text{d} \sigma/ \text{d} P_{T,jets}^{gap}$
XLabel=$P_{T,jets}^{gap}$ (GeV)
XMax=200.0
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j2_pullangle
YLabel=$\text{d} \sigma/ \text{d} \theta_{j1,j2}$ (fb)
XLabel=$\theta_{j1,j2}$ $(rad/\pi)$
RatioPlotYMin=0.6
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j2j3_pullangle
YLabel=$\text{d} \sigma/ \text{d} \theta_{j2,j3}$ (fb)
XLabel=$\theta_{j2,j3}$ $(rad/\pi)$
RatioPlotYMin=0.6
RatioPlotYMax=1.8
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j3_pullangle

YLabel=$\text{d} \sigma/ \text{d} \theta_{j1,j3}$ (fb)
XLabel=$\theta_{j1,j3}$ $(rad/\pi)$
RatioPlotYMin=0.2
RatioPlotYMax=1.8
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/HT_gapjets
YLabel=$\text{d} \sigma/ \text{d} H_{T,jets}^\text{gap}$ (fb/GeV)
XLabel=$H_{T,jets}^\text{gap}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/avgNGapJets_ht
YLabel=$\langle N_{gap} \rangle$
XLabel=$H_{T}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/avgNGapJets_dy
YLabel=$\langle N_{gap} \rangle$
XLabel=$\Delta y_{j_1j_2}$
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/y1j_yj2
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_1}*y_{j_2}$ (fb)
XLabel=$y_{j_1}*y_{j_2}$
RatioPlotYMin=0.7
RatioPlotYMax=1.4
XMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/avgNGapJets_mjj
YLabel=$\langle N_{gap} \rangle$
XLabel=$m_{j_1j_2}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/avgNGapJets_pt
YLabel=$\langle N_{gap} \rangle$ 
XLabel=$\overline{P_{T,j_1j_2}}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/NGapJet_incl
YLabel=$\sigma_{\text{fid}, > N_{jets}}$ 
XLabel=$>N_{jets}^{gap}$
XMax=6.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/NGapJet_excl
YLabel=$\sigma_{\text{fid}, N_{jets}^{gap}}$ 
XLabel=$N_{jets}^{gap}$
XMax=6.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/Hj_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,hj_1}^{incl}$ (fb/GeV)
XLabel=$p_{T,hj_1}^{incl}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/Hjj_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,hj_1j_2}$ (fb/GeV)
XLabel=$p_{T,hj_1j_2}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/Hjj_pT_excl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,hj_1j_2}^{excl}$ (fb/GeV)
XLabel=$p_{T,hj_1j_2}^{excl}$ (GeV)
XMax=150.0
RatioPlotYMin=0.0
RatioPlotYMax=4.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/H_j_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,>Njets}$ (fb/GeV)
XLabel=$p_{T,>Njets}$ (GeV)
RatioPlotYMin=0.6
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/H_jj_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2}^{incl}$ (GeV)
RatioPlotYMin=0.6
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/H_jj_pT_excl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2}^{excl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2}^{excl}$ (GeV)
RatioPlotYMin=0.6
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/H_jjj_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2j_3}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2j_3}^{incl}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/H_jjj_pT_excl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2j_3}^{excl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2j_3}^{excl}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/H_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,h}^{incl}$ (fb/GeV)
XLabel=$p_{T,h}^{incl}$ (GeV)
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/H_y
YLabel=$ \text{d} \sigma/ \text{d}  y_{h}$ (fb)
XLabel=$y_{h}$ 
RatioPlotYMin=0.0
RatioPlotYMax2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/H_y_abs
YLabel=$ \text{d} \sigma/ \text{d}  |y_{h}|$ (fb)
XLabel=$|y_{h}|$
XMax=5.0
RatioPlotYMin=0.2
RatioPlotYMax=1.8
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet1_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_1}^{incl}$ (GeV)
RatioPlotYMin=0.6
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet1_y_abs_incl
YLabel=$ \text{d} \sigma/ \text{d}  |y_{j_1}|$ (fb)
XLabel=$|y_{j_1}|$
XMax=5.0
RatioPlotYMin=0.5
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet1_y_incl
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_1}^{incl}$ (fb)
XLabel=$y_{j_1}^{incl}$
XMax=5.0
RatioPlotYMin=0.5
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet2_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_2}$ (fb/GeV)
XLabel=$p_{T,j_2}$ (GeV)
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/deltay_jj
YLabel=$ \text{d} \sigma/ \text{d}  \Delta y_{j_1j_2}$ (fb)
XLabel=$\Delta y_{j_1j_2}$ 
XMin=4
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet2_y_incl
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_2}$ (fb)
XLabel=$y_{j_2}$ 
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet2_y_abs_incl
YLabel=$ \text{d} \sigma/ \text{d}  |y_{j2}|$ (fb)
XLabel=$|y_{j2}|$
XMax=5.0
RatioPlotYMin=0.8
RatioPlotYMax=1.3
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet3_pT_excl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_3}^{excl}$ (fb/GeV)
XLabel=$p_{T,j_3}^{excl}$ (GeV)
XMax=200.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet1_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1}$ (fb/GeV)
XLabel=$m_{j_1}$ (GeV) 
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet4_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_4}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_4}^{incl}$ (GeV)
XMax=250.0
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_4}$ (fb/GeV)
XLabel=$m_{j_4}$ (GeV)
XMax=60.0
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet3_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_3}$ (fb/GeV)
XLabel=$p_{T,j_3}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet3_y
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_3}^{\star}$ (fb)
XLabel=$y_{j_3}^{\star}$ 
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet3_y_incl
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_3}^{incl}$ (fb)
XLabel=$y_{j_3}^{incl}$ 
RatioPlotYMin=0.6
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet4_y
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_4}^{\star}$ (fb)
XLabel=$y_{j_4}^{\star}$ 
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet4_y_incl
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_4}^{incl}$ (fb)
XLabel=$y_{j_4}^{incl}$ 
RatioPlotYMin=0.6
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/log10_R_0
Title=$\log_{10}$(Integrated $0$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{0}$
RatioPlotYMin=0.7
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/log10_R_1
Title=$\log_{10}$(Integrated $0$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{1}$
RatioPlotYMin=0.7
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/log10_R_2
Title=$\log_{10}$(Integrated $0$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{2}$
RatioPlotYMin=0.6
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/log10_R_3
Title=$\log_{10}$(Integrated $4$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{\geq4}$
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/log10_R_4
Title=$\log_{10}$(Integrated $4$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{\geq4}$
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet2_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2}$ (fb/GeV)
XLabel=$m_{j_2}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/jet3_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_3}$ (fb/GeV)
XLabel=$m_{j_3}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/H_dijet_mass
YLabel=$ \text{d} \sigma/ \text{d}  \Delta m_{h,j_1j_2}$ (fb/GeV)
XLabel=$m_{h,j_1j_2}$ (GeV)
XMin=700.0
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/deltay_H_jj
YLabel=$ \text{d} \sigma/ \text{d}  \Delta y_{h,j_1j_2}$ (fb)
XLabel=$\Delta y_{h,j_1j_2}$ 
XMax=6.0
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/H3_y
YLabel=$ \text{d} \sigma/ \text{d}  y_{h}^{\star}$ (fb)
XLabel=$y_{h}^{\star}$ 
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/dijet_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2}$ (fb/GeV)
XLabel=$m_{j_1j_2}$ (GeV)
RatioPlotYMin=0.6
RatioPlotYMax=1.4
XMax=1000.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/dijet_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2}$ (fb/GeV)
XLabel=$m_{j_1j_2}$ (GeV)
XMax=200.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/deltaphi_jj_incl

YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{j_1j_2}^{incl}$ (fb)
XLabel=$\Delta \phi_{j_1j_2}^{incl}$ 
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/deltaphi_jj_excl

YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{j_1j_2}^{excl}$ (fb)
XLabel=$\Delta \phi_{j_1j_2}^{excl}$ 
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/deltaphi_Hjj_incl

YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{h,j_1j_2}$ (fb)
XLabel=$\Delta \phi_{h,j_1j_2}$ 
RatioPlotYMin=0.6
RatioPlotYMax=1.9
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/deltaphi_Hjj_excl

YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{h,j_1j_2}^{excl}$ (fb)
XLabel=$\Delta \phi_{h,j_1j_2}^{excl}$ 
RatioPlotYMin=0.2
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/deltaphi2

YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{2}$ (fb)
XLabel=$\Delta \phi_{2}$ 
RatioPlotYMin=0.6
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/trijet_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/trijet_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j2j4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j2j4_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_4}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j3j4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_3j_4}$ (GeV)
RatioPlotYMin=0.2
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j3j4_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_3j_4}$ (GeV)
RatioPlotYMin=0.2
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j2j3j4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_2j_3j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j2j3j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_2j_3j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j2j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_4}$ (fb/GeV)
XLabel=$m_{j_2j_4}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j2j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_4}$ (fb/GeV)
XLabel=$m_{j_2j_4}$ (GeV)
XMax=200.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j3j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_3j_4}$ (fb/GeV)
XLabel=$m_{j_3j_4}$ (GeV)
XMax=1000
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j3j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_3j_4}$ (fb/GeV)
XLabel=$m_{j_3j_4}$ (GeV)
XMax=200.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j2j3_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3}$ (fb/GeV)
XLabel=$m_{j_2j_3}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.6
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j2j3_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3}$ (fb/GeV)
XLabel=$m_{j_2j_3}$ (GeV)
RatioPlotYMin=0.6
XMax=200.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_4}$ (fb/GeV)
XLabel=$m_{j_1j_4}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.2
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_4}$ (fb/GeV)
XLabel=$m_{j_1j_4}$ (GeV)
XMax=200.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j3_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3}$ (fb/GeV)
XLabel=$m_{j_1j_3}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.6
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j3_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3}$ (fb/GeV)
XLabel=$m_{j_1j_3}$ (GeV)
RatioPlotYMin=0.6
XMax=200.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/XS
YLabel=$ \sigma_{\text{fid}}$ (fb)
XLabel=
RatioPlotYMin=0.9
RatioPlotYMax=1.1
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/NJet_incl
YLabel=$ \sigma_{\text{fid}, > N_{jets}}$ (fb)
XLabel=$>N_{jets}$
XMax=8.0
RatioPlotYMin=0.2
RatioPlotYMax=3.0
XMax=10.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/NJet_excl
YLabel=$ \sigma_{\text{fid}, N_{jets}}$ (fb)
XLabel=$N_{jets}$
XMax=8.0
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j2j3j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3j_4}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/j1j2j3j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3j_4}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/HT_jets
YLabel=$ \text{d} \sigma/ \text{d}  H_{T}(\text{jets})$ (fb/GeV)
XLabel=$H_{T}(\text{jets})$ (GeV)
XMax=1000
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/HT_all
YLabel=$ \text{d} \sigma/ \text{d}  H_{T}(\text{all})$ (fb/GeV)
XLabel=$H_{T}(\text{all})$ (GeV)
XMax=500.0
RatioPlotYMin=0.9
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/log10_d_01
YLabel=$ \text{d} \sigma / \sqrt{d_{01}}$ (fb/GeV)
XLabel=$\sqrt{d_{01}}$ (GeV)


RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/log10_d_12
YLabel=$ \text{d} \sigma / \sqrt{d_{12}}$ (fb/GeV)
XLabel=$\sqrt{d_{12}}$ (GeV)


RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/log10_d_23
Title=$\log_{10}$($k_\perp$ jet resolution $2 \to 3$ [GeV])
XLabel=$\log_{10}(\sqrt{d_{23}}/\text{GeV})$
YLabel=$\text{d}\sigma/\text{d}\log_{10}(\sqrt{d_{23}}/\text{GeV})$ [fb]

RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_TIGHT/log10_d_34
Title=$\log_{10}$($k_\perp$ jet resolution $3 \to 4$ [GeV])
XLabel=$\log_{10}(\sqrt{d_{34}}/\text{GeV})$

YLabel=$\text{d}\sigma/\text{d}\log_{10}(\sqrt{d_{34}}/\text{GeV})$ [fb]
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet3_x

YLabel=$\text{d} \sigma/ \text{d} x_{j_3}^{\star}$ (fb)
XLabel=$x_{j_3}^{\star}$
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet4_x

YLabel=$\text{d} \sigma/ \text{d} x_{j_4}^{\star}$ (fb)
XLabel=$x_{j_4}^{\star}$
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/gapjet1_y_incl

YLabel=$\text{d} \sigma/ \text{d} y_{jets}^{gap}$
XLabel=$y_{jets}^{gap}$
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/gapjet1_pt_incl

YLabel=$\text{d} \sigma/ \text{d} P_{T,jets}^{gap}$
XLabel=$P_{T,jets}^{gap}$ (GeV)

XMax=200
RatioPlotYMin=0.0
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j2_pullangle

YLabel=$\text{d} \sigma/ \text{d} \theta_{j1,j2}$ (fb)
XLabel=$\theta_{j1,j2}$ $(rad/\pi)$
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/NJet_excl
YLabel=$ \sigma_{\text{fid}, N_{jets}}$ (fb)
XLabel=$N_{jets}$
XMax=8.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j2j3_pullangle

YLabel=$\text{d} \sigma/ \text{d} \theta_{j2,j3}$ (fb)
XLabel=$\theta_{j2,j3}$ $(rad/\pi)$
RatioPlotYMin=0.6
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j3_pullangle

YLabel=$\text{d} \sigma/ \text{d} \theta_{j1,j3}$ (fb)
XLabel=$\theta_{j1,j3}$ $(rad/\pi)$
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/HT_gapjets
YLabel=$\text{d} \sigma/ \text{d} H_{T,jets}^\text{gap}$ (fb/GeV)
XLabel=$H_{T,jets}^\text{gap}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/avgNGapJets_ht

YLabel=$\langle N_{gap} \rangle$
XLabel=$H_{T}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/avgNGapJets_dy

YLabel=$\langle N_{gap} \rangle$
XLabel=$\Delta y_{j_1j_2}$
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/y1j_yj2

YLabel=$ \text{d} \sigma/ \text{d}  y_{j_1}*y_{j_2}$ (fb)
XLabel=$y_{j_1}*y_{j_2}$
RatioPlotYMin=0.5
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/avgNGapJets_mjj

YLabel=$\langle N_{gap} \rangle$
XLabel=$m_{j_1j_2}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/avgNGapJets_pt

YLabel=$\langle N_{gap} \rangle$ 
XLabel=$\overline{P_{T,j_1j_2}}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/NGapJet_incl

YLabel=$\sigma_{\text{fid}, > N_{jets}}$ 
XLabel=$>N_{jets}^{gap}$
XMax=6.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/NGapJet_excl
YLabel=$\sigma_{\text{fid}, N_{jets}^{gap}}$ 
XLabel=$N_{jets}^{gap}$
XMax=6.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/Hj_pT_incl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,hj_1}^{incl}$ (fb/GeV)
XLabel=$p_{T,hj_1}^{incl}$ (GeV)

RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/Hjj_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,hj_1j_2}$ (fb/GeV)
XLabel=$p_{T,hj_1j_2}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/Hjj_pT_excl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,hj_1j_2}^{excl}$ (fb/GeV)
XLabel=$p_{T,hj_1j_2}^{excl}$ (GeV)
XMax=150.0
RatioPlotYMin=0.0
RatioPlotYMax=4.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/H_j_pT_incl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,>Njets}$ (fb/GeV)
XLabel=$p_{T,>Njets}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/H_jj_pT_incl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2}^{incl}$ (GeV)
RatioPlotYMin=0.4
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/H_jj_pT_excl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2}^{excl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2}^{excl}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/H_jjj_pT_incl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2j_3}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2j_3}^{incl}$ (GeV)
RatioPlotYMin=0.4
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/H_jjj_pT_excl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1j_2j_3}^{excl}$ (fb/GeV)
XLabel=$p_{T,j_1j_2j_3}^{excl}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/H_pT_incl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,h}^{incl}$ (fb/GeV)
XLabel=$p_{T,h}^{incl}$ (GeV)
RatioPlotYMin=0.4
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/H_y

YLabel=$ \text{d} \sigma/ \text{d}  y_{h}$ (fb)
XLabel=$y_{h}$ 
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/H_y_abs

YLabel=$ \text{d} \sigma/ \text{d}  |y_{h}|$ (fb)
XLabel=$|y_{h}|$
XMax=5.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet1_pT_incl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_1}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_1}^{incl}$ (GeV)
RatioPlotYMin=0
RatioPlotYMax=1.5
XMax=400
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet1_y_abs_incl

YLabel=$ \text{d} \sigma/ \text{d}  |y_{j_1}|$ (fb)
XLabel=$|y_{j_1}|$
XMax=5.0
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet1_y_incl

YLabel=$ \text{d} \sigma/ \text{d}  y_{j_1}^{incl}$ (fb)
XLabel=$y_{j_1}^{incl}$
XMax=5.0
RatioPlotYMin=0.2
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet2_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_2}$ (fb/GeV)
XLabel=$p_{T,j_2}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/deltay_jj

YLabel=$ \text{d} \sigma/ \text{d}  \Delta y_{j_1j_2}$ (fb)
XLabel=$\Delta y_{j_1j_2}$ 
RatioPlotYMin=0.5
RatioPlotYMax=1.5
XMax=9
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet2_y_incl
YLabel=$ \text{d} \sigma/ \text{d}  y_{j_2}$ (fb)
XLabel=$y_{j_2}$ 
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet2_y_abs_incl
YLabel=$ \text{d} \sigma/ \text{d}  |y_{j2}|$ (fb)
XLabel=$|y_{j2}|$
XMax=5.0
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet3_pT_excl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_3}^{excl}$ (fb/GeV)
XLabel=$p_{T,j_3}^{excl}$ (GeV)
XMax=200.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet1_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1}$ (fb/GeV)
XLabel=$m_{j_1}$ (GeV) 

RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet4_pT_incl

YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_4}^{incl}$ (fb/GeV)
XLabel=$p_{T,j_4}^{incl}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
XMax=150
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_4}$ (fb/GeV)
XLabel=$m_{j_4}$ (GeV)
XMax=60 

RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet3_pT_incl
YLabel=$ \text{d} \sigma/ \text{d}  p_{T,j_3}$ (fb/GeV)
XLabel=$p_{T,j_3}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
XMax=300
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet3_y
YLabel=$ \text{d} \sigma/ \text{d}  z_{j_3}^{\star}$ (fb)
XLabel=$z_{j_3}^{\star}$ 
RatioPlotYMin=0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet3_y_incl

YLabel=$ \text{d} \sigma/ \text{d}  y_{j_3}^{incl}$ (fb)
XLabel=$y_{j_3}^{incl}$ 
RatioPlotYMin=0.2
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet4_y

YLabel=$ \text{d} \sigma/ \text{d}  z_{j_4}^{\star}$ (fb)
XLabel=$z_{j_4}^{\star}$ 
RatioPlotYMin=0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet4_y_incl

YLabel=$ \text{d} \sigma/ \text{d}  y_{j_4}^{incl}$ (fb)
XLabel=$y_{j_4}^{incl}$ 
RatioPlotYMin=0.2
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet2_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2}$ (fb/GeV)
XLabel=$m_{j_2}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/jet3_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_3}$ (fb/GeV)
XLabel=$m_{j_3}$ (GeV)

RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/H_dijet_mass

YLabel=$ \text{d} \sigma/ \text{d}  \Delta m_{h,j_1j_2}$ (fb/GeV)
XLabel=$m_{h,j_1j_2}$ (GeV)
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/deltay_H_jj

YLabel=$ \text{d} \sigma/ \text{d}  \Delta y_{h,j_1j_2}$ (fb)
XLabel=$\Delta y_{h,j_1j_2}$ 
RatioPlotYMin=0.0
RatioPlotYMax=2.5
XMax=6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/H3_y

YLabel=$ \text{d} \sigma/ \text{d}  y_{h}^{\star}$ (fb)
XLabel=$y_{h}^{\star}$ 
RatioPlotYMin=0.5
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/dijet_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2}$ (fb/GeV)
XLabel=$m_{j_1j_2}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.3
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/dijet_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2}$ (fb/GeV)
XLabel=$m_{j_1j_2}$ (GeV)
XMax=200.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/deltaphi_jj_incl

YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{j_1j_2}^{incl}$ (fb)
XLabel=$\Delta \phi_{j_1j_2}^{incl}$ 
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/deltaphi_jj_excl

YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{j_1j_2}^{excl}$ (fb)
XLabel=$\Delta \phi_{j_1j_2}^{excl}$ 
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/deltaphi_Hjj_incl
YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{h,j_1j_2}$ (fb)
XLabel=$\Delta \phi_{h,j_1j_2}$ 
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/deltaphi_Hjj_excl

YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{h,j_1j_2}^{excl}$ (fb)
XLabel=$\Delta \phi_{h,j_1j_2}^{excl}$
RatioPlotYMin=0.5
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/deltaphi2

YLabel=$ \text{d} \sigma/ \text{d}  \Delta \phi_{2}$ (fb)
XLabel=$\Delta \phi_{2}$ 
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/trijet_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/trijet_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3}$ (GeV)
RatioPlotYMin=0.6
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j2j4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j2j4_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_4}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j3j4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_3j_4}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.2
RatioPlotYMax=1.8
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j3j4_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_3j_4}$ (GeV)
XMax=200.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j2j3j4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_2j_3j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j2j3j4_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_2j_3j_4}$ (GeV)

RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j2j4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_4}$ (fb/GeV)
XLabel=$m_{j_2j_4}$ (GeV)
XMax=1000
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j2j4_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_4}$ (fb/GeV)
XLabel=$m_{j_2j_4}$ (GeV)
XMax=200

RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j3j4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_3j_4}$ (fb/GeV)
XLabel=$m_{j_3j_4}$ (GeV)
XMax=1000
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j3j4_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_3j_4}$ (fb/GeV)
XLabel=$m_{j_3j_4}$ (GeV)
XMax=200
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j2j3_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3}$ (fb/GeV)
XLabel=$m_{j_2j_3}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j2j3_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_2j_3}$ (fb/GeV)
XLabel=$m_{j_2j_3}$ (GeV)
XMax=200.0
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j4_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_4}$ (fb/GeV)
XLabel=$m_{j_1j_4}$ (GeV)
XMax=1000.0
RatioPlotYMin=0.4
RatioPlotYMax=1.8
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j4_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_4}$ (fb/GeV)
XLabel=$m_{j_1j_4}$ (GeV)
XMax=200.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j3_mass

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3}$ (fb/GeV)
XLabel=$m_{j_1j_3}$ (GeV)
XMax=1000
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j3_mass_fine

YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_3}$ (fb/GeV)
XLabel=$m_{j_1j_3}$ (GeV)
XMax=200
RatioPlotYMin=0.4
RatioPlotYMax=1.6
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/XS
YLabel=$ \sigma_{\text{fid}}$ (fb)
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/NJet_incl

YLabel=$ \sigma_{\text{fid}, > N_{jets}}$ (fb)
XLabel=$>N_{jets}$
XMax=8.0
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j2j3j4_mass
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3j_4}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/j1j2j3j4_mass_fine
YLabel=$ \text{d} \sigma/ \text{d}  m_{j_1j_2j_3j_4}$ (fb/GeV)
XLabel=$m_{j_1j_2j_3j_4}$ (GeV)
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/HT_jets
YLabel=$ \text{d} \sigma/ \text{d}  H_{T}(\text{jets})$ (fb/GeV)
XLabel=$H_{T}(\text{jets})$ (GeV)
RatioPlotYMin=0.5
RatioPlotYMax=1.5
XMax=1000
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/HT_all
YLabel=$ \text{d} \sigma/ \text{d}  H_{T}(\text{all})$ (fb/GeV)
XLabel=$H_{T}(\text{all})$ (GeV)
XMax=500.0
RatioPlotYMin=0.8
RatioPlotYMax=1.2
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/log10_R_0
Title=$\log_{10}$(Integrated $0$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{0}$
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/log10_d_01
YLabel=$ \text{d} \sigma / \sqrt{d_{01}}$ (fb/GeV)
XLabel=$\sqrt{d_{01}}$ (GeV)
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/log10_R_1
Title=$\log_{10}$(Integrated $0$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{1}$
RatioPlotYMin=0.5
RatioPlotYMax=1.5
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/log10_R_2
Title=$\log_{10}$(Integrated $0$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{2}$
RatioPlotYMin=0.8
RatioPlotYMax=1.4
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/log10_R_3
Title=$\log_{10}$(Integrated $3$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{3}$
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/log10_R_4
Title=$\log_{10}$(Integrated $4$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{\geq4}$
RatioPlotYMin=0.0
RatioPlotYMax=3.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/log10_d_12
YLabel=$ \text{d} \sigma / \sqrt{d_{12}}$ (fb/GeV)
XLabel=$\sqrt{d_{12}}$ (GeV)
RatioPlotYMin=0.2
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H2JETS_04_LOOSE/log10_d_23
Title=$\log_{10}$($k_\perp$ jet resolution $2 \to 3$ [GeV])
XLabel=$\log_{10}(\sqrt{d_{23}}/\text{GeV})$
YLabel=$\text{d}\sigma/\text{d}\log_{10}(\sqrt{d_{23}}/\text{GeV})$ [fb]
RatioPlotYMin=0.0
RatioPlotYMax=2.0
# END PLOT

# BEGIN PLOT /MC_H_KTSPLITTINGS/log10_R_0
Title=$\log_{10}$(Integrated $0$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{0}$
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H_KTSPLITTINGS/log10_R_1
Title=$\log_{10}$(Integrated $1$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{1}$
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H_KTSPLITTINGS/log10_R_2
Title=$\log_{10}$(Integrated $2$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{2}$
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H_KTSPLITTINGS/log10_R_3
Title=$\log_{10}$(Integrated $3$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{3}$
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H_KTSPLITTINGS/log10_R_4
Title=$\log_{10}$(Integrated $4$ jet rate in $k_\perp$ [GeV])
XLabel=$\log_{10}(d_{\text{cut}}/\text{GeV})$
YLabel=$R_{\geq4}$
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H_KTSPLITTINGS/log10_d_01
Title=$\log_{10}$($k_\perp$ jet resolution $0 \to 1$ [GeV])
XLabel=$\log_{10}(d_{01}/\text{GeV})$
YLabel=$\text{d}\sigma/\text{d}\log_{10}(d_{01}/\text{GeV})$ [fb]
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H_KTSPLITTINGS/log10_d_12
Title=$\log_{10}$($k_\perp$ jet resolution $1 \to 2$ [GeV])
XLabel=$\log_{10}(\sqrt{d_{1}}/\text{GeV})$
YLabel=$\text{d}\sigma/\text{d}\log_{10}(\sqrt{d_{1}}/\text{GeV})$ [fb]
RatioPlotYMin=0.0
RatioPlotYMax=2.5
# END PLOT

# BEGIN PLOT /MC_H_KTSPLITTINGS/log10_d_23
#Title=$\log_{10}$($k_\perp$ jet resolution $2 \to 3$ [GeV])
XLabel=$\log_{10}(\sqrt{d_{2}}/\text{GeV})$
YLabel=$\text{d}\sigma/\text{d}\log_{10}(\sqrt{d_{2}}/\text{GeV})$ [fb]
RatioPlotYMin=0.0
RatioPlotYMax=3
XMax=3
# END PLOT

# BEGIN PLOT /MC_H_KTSPLITTINGS/log10_d_34
#Title=$\log_{10}$($k_\perp$ jet resolution $3 \to 4$ [GeV])
XLabel=$\log_{10}(\sqrt{d_{3}}/\text{GeV})$
YLabel=$\text{d}\sigma/\text{d}\log_{10}(\sqrt{d_{3}}/\text{GeV})$ [fb]
RatioPlotYMin=0.0
RatioPlotYMax=3
XMax=3
# END PLOT



