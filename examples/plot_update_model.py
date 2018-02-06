# -*- coding: utf-8 -*-
"""
=============================
Create a model from scratch, and then update it with new subject data
=============================

In this example, we will simulate a model and some data, and see if we can
recover the model from the data. First, we'll load in some example locations.
Then, we will simulate correlational structure (a toeplitz matrix) to impose on
our simulated data.  This will allow us to test whether we can recover the
correlational structure in the data, and how that changes as a function of the
number of subjects in the model. Then, we will simulate 10 subjects and create
brain objects with their data.  The left figure shows the model derived from
10 simulated subjects.  Finally, we simulate 10 additional subjects and use the
model.update method to update an existing model with new data. On the right, the
updated model is plotted. As is apparent from the figures, the more data in the
model, the better the true correlational structure can be recovered.

"""

# Code source: Andrew Heusser & Lucy Owen
# License: MIT

# import libraries
from builtins import range
import os
import scipy
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import supereeg as se

# load example model to get locations
locs = se.load('example_locations')

# convert to pandas
locs=pd.DataFrame(locs, columns=['x', 'y', 'z'])

# simulate correlation matrix
R = se.create_cov(cov='toeplitz', n_elecs=len(locs))

# number of timeseries samples
n_samples = 1000

# number of subjects
n_subs = 10

# number of electrodes
n_elecs = 20

# simulate brain objects for the model that subsample n_elecs for each synthetic patient
model_bos = [se.simulate_model_bos(n_samples=1000, sample_rate=1000, locs=locs, sample_locs=n_elecs, cov='toeplitz') for x in
                     range(n_subs)]

# create the model object
model = se.Model(data=model_bos, locs=locs)

# brain object locations subsetted entirely from both model and gray locations - for this n > m (this isn't necessarily true, but this ensures overlap)
sub_locs = locs.sample(n_elecs).sort_values(['x', 'y', 'z'])

# simulate a new brain object using the same covariance matrix
bo = se.simulate_bo(n_samples=1000, sample_rate=1000, locs=sub_locs, cov='toeplitz')

# update the model
new_model = model.update(bo)

# simulate brain objects for the model that subsample n_elecs for each synthetic patient
model_update_bos = [se.simulate_model_bos(n_samples=1000, sample_rate=1000, locs=locs, sample_locs=n_elecs, cov='toeplitz') for y in
                     range(n_subs)]

# update the model
better_model = model.update(model_update_bos)

# initialize subplots
f, (ax1, ax2, ax3) = plt.subplots(1, 3)

# plot it and set the title
model.plot(ax=ax1, yticklabels=False, xticklabels=False, cmap='RdBu_r', cbar=True, vmin=0, vmax=1)
ax1.set_title('Before updating model: 10 subjects total')

# plot it and set the title
new_model.plot(ax=ax2, yticklabels=False, xticklabels=False, cmap='RdBu_r', cbar=True, vmin=0, vmax=1)
ax2.set_title('After updating model: 11 subjects total')

# plot it and set the title
better_model.plot(ax=ax3, yticklabels=False, xticklabels=False, cmap='RdBu_r', cbar=True, vmin=0, vmax=1)
ax3.set_title('After updating model: 20 subjects total')

plt.show()
