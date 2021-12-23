# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% tags=[]
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# %%
print(cv.__version__)

# %%
im = cv.imread('im/rgb.png')
plt.imshow(im)
plt.title("Imagen original")
plt.show()

# %% [markdown]
# Este primer intento no funciona muy bien

# %%
grayscale = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

# %%
plt.imshow(grayscale)
plt.title("Imagen en escala de grises con cvtColor")
plt.show()
cv.imwrite('out/gs-cvt.png', grayscale)

# %% [markdown]
# Escala de grises con un solo canal B,G,R -> 0,1,2

# %%
grayscale = im[:,:,1]
plt.imshow(grayscale)
plt.title("Imagen en escala de grises con un solo canal")
plt.show()
cv.imwrite('out/gs-1c.png', grayscale)

# %% [markdown]
# Promedios que pueden ser:
# - Y= 0.114B + 0.587G + 0.299R
# - Y= 0.33B + 0.33G + 0.33R

# %%
grayscale = 0.33*im[:,:,0] + 0.33*im[:,:,1] + 0.33*im[:,:,2]
grayscale = grayscale.astype(np.uint8)
plt.imshow(grayscale)
plt.title("Imagen en escala de grises con promedios")
plt.show()
cv.imwrite('out/gs-p.png', grayscale)
