#!/usr/bin/python3
import sys
from fitsimage import _fitsimage
from graphic import _MyCanvas as mcnv
from graphic import _MyImage as mimg
from matplotlib.figure import Figure
#from tkinter import ttk
from tkinter import *

def on_closing():
	if messagebox.askokcancel("Quit", "Voulez vous quitter?"):
		root.quit()     # stops mainloop
		root.destroy()

path = sys.argv[1]
fit = _fitsimage(path)
root = Tk()
notebook = ttk.Notebook(root)


if fit.nchannel == 1:
	rtab =  mcnv(notebook, 'grey')
	rimg = mimg()
	rimg._image(fit.sourcer,  fit.rgb[:, :, 0])
	rtab._add_fig('red', rimg)
	
	valname = 'eccentricity'
	eccmin = -1
	eccmax = 1
	stattab = mcnv(notebook,  valname)
	img1 = mimg()
	img1._stats(fit.rgb,  fit.sourcer,   3, valname,  'grey', lim=[eccmin, eccmax] )
	stattab._add_fig(valname, img1)

	valname = 'elongation'
	elmin = 1
	elmax = 2
	stattab1 = mcnv(notebook, valname)
	img2 = mimg()
	img2._stats(fit.rgb,  fit.sourcer,   3, valname,  'grey',  lim=[elmin,  elmax])
	stattab1._add_fig(valname, img2)	
else:
	rtab =  mcnv(notebook, 'red')
	rimg = mimg()
	rimg._image(fit.sourcer,  fit.rgb[:, :, 0])
	rtab._add_fig('red', rimg)

	gtab =  mcnv(notebook, 'green')
	gimg = mimg()
	gimg._image(fit.sourceg,  fit.rgb[:, :, 1])
	gtab._add_fig('green', gimg)

	btab =  mcnv(notebook, 'blue')
	bimg = mimg()
	bimg._image(fit.sourceb,  fit.rgb[:, :, 2])
	btab._add_fig('blue', bimg)

	valname = 'eccentricity'
	eccmin = -1
	eccmax = 1
	stattab = mcnv(notebook,  valname)
	img1 = mimg()
	img1._stats(fit.rgb,  fit.sourcer,   3, valname,  'red', lim=[eccmin, eccmax])
	img1._stats(fit.rgb,  fit.sourceg,  3, valname,  'green', lim=[eccmin, eccmax])
	img1._stats(fit.rgb,  fit.sourceb,  3, valname,  'blue', lim=[eccmin, eccmax])
	stattab._add_fig(valname, img1)

	valname = 'elongation'
	elmin = 1
	elmax = 2
	stattab1 = mcnv(notebook, valname)
	img2 = mimg()
	img2._stats(fit.rgb,  fit.sourcer,   3, valname,  'red',  lim=[elmin,  elmax])
	img2._stats(fit.rgb,  fit.sourceg,  3, valname,  'green',   lim=[elmin,  elmax])
	img2._stats(fit.rgb,  fit.sourceb,  3, valname,  'blue',  lim=[elmin,  elmax])
	stattab1._add_fig(valname, img2)


root.protocol("WM_DELETE_WINDOW", on_closing)
print(fit.s)
mainloop()
