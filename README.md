# CollimationTool
To help to collimate astronomical instruments
The aim of the project is to provide a tool to help to collimation of RC, Newton or any other reflectors.
The principle is simple and is to analyze elongation and eccentricity of stars on and image splitted in 3x3 grid.

Pre-requisite
 - Python3
 
Modules required
 - matplotlib
 - scipy
 - photutils
 - astropy
 - numpy
 - tkinter
 
 Main program is OptimColim
 
 It will give in a notebook the view of the image channel by channel on separate tabs with ellipses
 around the stars that are retained to make statistical computations on eccentricity and ellipticity that are
 on two more tabs.
 The idea is that on the airy spot of a start the point which is the most brillant can be eccentric if the secondary
 is not well aligned. And the image of the star is not round (ellipsoidal or comet like) when the primary is not well
 aligned
 
 As it is now, the tool required long computations so it  is not well adapted for a live collimation procedure. I am looking
 for people that could help me to improve drastically the speed of the tool in order to be able to use it in live procedure.
