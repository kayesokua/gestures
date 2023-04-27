import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def plot_spatial_gabors(pyramid, indices):
    vdim = pyramid.definition['vdim']
    size = 0.6
    fig, axs = plt.subplots(
        2, len(indices), figsize=((len(indices) * 4.25 + 0.25) * size, 7.5 * size), squeeze=False,
        sharex=True, sharey=True)
    axs.T[0][0].set_ylabel('spatial Gabor (cos)')
    axs.T[0][1].set_ylabel('spatial Gabor (sin)')
    for ii, axs_ in zip(indices, axs.T):
        spatial_sin, spatial_cos = pyramid.get_filter_spatial_quadrature(ii)
        axs_[0].imshow(spatial_cos, aspect='equal')
        axs_[1].imshow(spatial_sin, aspect='equal')
        axs_[0].set_title('frame %d' % ii)
        gabor = pyramid.filters[ii]
        for ax in axs_:
            ax.scatter(gabor['centerh'] * vdim, gabor['centerv'] * vdim, color='k', marker='+')
            ax.set_xticks([])
            ax.set_yticks([])
    plt.tight_layout()
