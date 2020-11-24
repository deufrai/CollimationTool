from astropy.stats import sigma_clipped_stats
from astropy.stats import SigmaClip
from photutils import Background2D, MedianBackground

from astropy.io import fits
from photutils.segmentation import detect_sources,  source_properties
import numpy as np
from enum import Enum
from photutils import  detect_threshold

import cv2


class BayerOrder(Enum):
	"""
	RGGB:
		RG
		GB
	GBRG:
		GB
		RG
	BGGR:
		BG
		GR
	GRBG:
		GR
		BG
	"""
	RGGB = 'RGGB'
	GBRG = 'GBRG'
	BGGR = 'BGGR'
	GRBG = 'GRBG'


R_CHANNEL_INDEX, G_CHANNEL_INDEX, B_CHANNEL_INDEX = [0, 1, 2]

BAYER_ORDER_TO_RGB_CHANNEL_COORDINATES = {
	# (ry, rx), (gy, gx), (Gy, Gx), (by, bx)
    BayerOrder.RGGB: ((0, 0), (1, 0), (0, 1), (1, 1)),
    BayerOrder.GBRG: ((1, 0), (0, 0), (1, 1), (0, 1)), 
    BayerOrder.BGGR: ((1, 1), (0, 1), (1, 0), (0, 0)),
    BayerOrder.GRBG: ((0, 1), (1, 1), (0, 0), (1, 0))
}

def _guard_attribute_is_a_multiple_of(attribute_name, attribute_value, multiple):
    if not attribute_value % multiple == 0:
        raise ValueError(
            'Incoming data is the wrong shape: {attribute_name} ({attribute_value}) is not a multiple of {multiple}'.format(**locals())
        )

class _fitsimage():
	def __init__(self,  path):
		hdul = fits.open(path)
		self.xsize=hdul[0].header['NAXIS1']
		self.ysize=hdul[0].header['NAXIS2']
		self.data = hdul[0].data
		print(hdul[0].header['BAYERPAT'])
		if hdul[0].header['BAYERPAT'] == 'RGGB':
			dim = 3
		else:
			dim = 1
		self.s = np.shape(self.data)
		print(self.s)
		hdul.close()
		if len(self.s) == 2 and dim == 1:
			self.nchannel = 1
			ored=self.data[ :,:]
			ogreen=self.data[:,:] 
			oblue=self.data[:,:] 
			self.rgb = np.ndarray((self.s[0],  self.s[1], 3),  dtype='float')
			self.rgb[:, :, 0]=ored
			self.rgb[:, :, 1]=ogreen
			self.rgb[:, :, 2]=oblue
		elif self.s[0] == 3:
			self.nchannel = 3
			ored=self.data[0, :,:]
			ogreen=self.data[1, :,:] 
			oblue=self.data[2,:,:] 
			self.rgb = np.ndarray((self.s[1],  self.s[2], 3),  dtype='float')
			self.rgb[:, :, 0]=ored
			self.rgb[:, :, 1]=ogreen
			self.rgb[:, :, 2]=oblue
		else:
			self.nchannel = 3
			self.rgb = cv2.cvtColor(self.data, cv2.COLOR_BAYER_BG2RGB)
			ored     = self.rgb[:,:, 0] 
			ogreen = self.rgb[:,:, 1] 
			oblue   = self.rgb[:,:, 2]

		self.rgb[:, :, 0],  self.sourcer      = self._find_sources(ored)
		if self.nchannel == 3:
			self.rgb[:, :, 1],  self.sourceg     =  self._find_sources(ogreen)
			self.rgb[:, :, 2],  self.sourceb     =  self._find_sources(oblue)

		
	def _find_sources(self,  layer):
		npixels = 8
		sigma_clip = SigmaClip(sigma=3.)
		bkg_estimator = MedianBackground()
		bkg = Background2D(layer, (200,200), filter_size=(3, 3),
				sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)		
		mean, median, std = sigma_clipped_stats(layer)
		layer = layer - bkg.background
		threshold = detect_threshold(layer, nsigma=6.)
		segm = detect_sources(layer,   threshold,  npixels=npixels) #, filter_kernel=kernel)
		columns=['xcentroid', 'ycentroid', 'semimajor_axis_sigma', 'semiminor_axis_sigma', 'orientation', 
			'ellipticity', 'eccentricity',  'elongation']
		sources = source_properties(layer,   segm).to_table(columns=columns)
#		print(len(sources))
		return layer,  sources

