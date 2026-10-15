"""Main-lobe direction and 3 dB beamwidth of the matched design's realized-gain pattern (phi = 0 and 90 deg cuts)."""

import cst.interface

PROJECT = r"C:\Users\asus\btp\btp\power-combining\single_probe_matched.cst"

de = cst.interface.DesignEnvironment.connect_to_any()
m = de.get_open_project(PROJECT).model3d
ff = m.FarfieldPlot
m.SelectTreeItem("Farfields\\farfield (f=33.106) [1]")
for phi in (0, 90):
    ff.Reset()
    ff.Plottype("polar")
    ff.Vary("angle1")
    ff.Phi(phi)
    ff.SetPlotMode("realized gain")
    ff.Plot()
    print(f"cut phi={phi}: max {ff.GetMax():.2f} dBi, main lobe theta {ff.GetMainLobeDirection()}, "
          f"3dB beamwidth {ff.GetAngularWidthXdB()} deg, side lobe level {ff.GetSideLobeLevel()}")
