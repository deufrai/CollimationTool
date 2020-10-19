from MyCanvas import MyCanvas as mcnv
from scipy.stats import norm
from astropy.visualization.mpl_normalize import ImageNormalize
from astropy.visualization import SqrtStretch
import astropy.units as u
import numpy as np
from photutils import EllipticalAperture
import tkinter as tk
from tkinter import ttk
from tkinter import *
#import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.cm import get_cmap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,  NavigationToolbar2Tk
#import matplotlib.backends.backend_tkagg as tkagg

class _MyCanvas(Frame):
	
	def __init__(self,  parent,  name, **kwargs):
		self.parent = parent
		ttk.Frame.__init__(self, parent)
		self.parent.pack(fill='both', expand=True)
		self.fig = None
		self.canvas = None

	def _add_fig(self, title='Empty', fig=None):
		self.parent.add(self, text=title)
		if fig is None:
			self.fig = Figure((8, 8), dpi=100)
			a = self.fig.add_subplot(111)
			a.plot(np.arange(0, 10), np.random.random(10))
		else:
			self.fig = fig
		self.canvas = FigureCanvasTkAgg(self.fig, self)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
		toolbar = NavigationToolbar2Tk(self.canvas, self)
		toolbar.update()
		self.canvas._tkcanvas.pack()
		
	def _refresh(self):
		print('refresh')

class _MyImage(Figure):
	def __init__(self, **kwargs):
		Figure.__init__(self,  **kwargs)
		
	def _image(self,  cat,  rgbimg):
		self.axe = self.add_subplot(111)
		norme = ImageNormalize(stretch=SqrtStretch())
		a = np.array(cat['semimajor_axis_sigma'], dtype='float')
		b = np.array(cat['semiminor_axis_sigma'], dtype='float')
		elongation = np.array(cat['elongation'], dtype='float')
		mz = np.mean(elongation)
		std = np.std(elongation)
		zmin= mz-std
		zmax = mz + std
		print('zmin ='+str(zmin))
		print('zmax ='+str(zmax))
		r = 3.
		apertures = []
		for obj in cat:
			if obj['elongation'].value >= zmin and obj['elongation'].value <= zmax:
				position = np.transpose((obj['xcentroid'].value, obj['ycentroid'].value))
				a = obj['semimajor_axis_sigma'].value * r
				b = obj['semiminor_axis_sigma'].value* r
				theta = (obj['orientation']).to(u.rad).value
				apertures.append(EllipticalAperture(position, a, b, theta=theta))
		print(len(apertures))
		self.axe.imshow(rgbimg, origin='lower',   norm=norme,  cmap=get_cmap('Greys_r'), interpolation='nearest')
		for aperture in apertures:
			aperture.plot(self.axe,  color='red', lw=1.5)

	def _test_include(self,  y, x, ya, yb, xa, xb):
		if (x >= xa and x <= xb) and (y >= ya and y <= yb):
			return True
		else:
			return False
	
	def _stats(self,  data, tbl,  n, valname, color,  lim=None):
		if not hasattr(self,  'axe'):
			self.axe=self.subplots(n, n)
		x = np.array(tbl['xcentroid'], dtype='float')
		y = np.array(tbl['ycentroid'], dtype='float')
		z = np.array(tbl[valname], dtype='float')
		s = np.shape(data)
		s = np.floor_divide(s, n)
		for i in range(0,n):
			ya = i*s[0]
			yb = ya + s[0]
			for j in range(0,n):
				xa = j*s[1]
				xb = xa+s[1]
				ech=[]
				for k in range(len(z)):
					if self._test_include(y[k], x[k], ya, yb, xa, xb):
						ech.append(z[k])
				if len(ech) > 0:
#					ech = ech / np.max(ech)
					if lim is None:
						xmin, xmax = (0,  2)
					else:
						xmin = lim[0]
						xmax = lim[1]
					self.axe[i,j].hist(ech, color=color,  bins='auto',  range = (xmin, xmax),  alpha=0.6, density=1)
					mean,std=norm.fit(ech)
					xi = np.linspace(xmin, xmax, 100)
					yi = norm.pdf(xi, mean, std)
					self.axe[i,j].plot(xi, yi, color=color)
		
#root = Tk()
#root.wm_title('test')
#
#notebook = ttk.Notebook(root)
#tab1 = MyCanvas(notebook, 'tab1')
#fig = MyImage(figsize=(8, 8), dpi=100)
#print(fig)
#
#tab1._add_fig(fig)
#
#
#
#tk.mainloop()
