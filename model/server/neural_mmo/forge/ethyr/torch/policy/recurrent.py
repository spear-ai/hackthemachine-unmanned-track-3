from pdb import set_trace as T
import numpy as np

import torch
from torch import nn

class BatchFirstLSTM(nn.LSTM):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, batch_first=True, **kwargs)

   def forward(self, input, hx):
      h, c       = hx
      h          = h.transpose(0, 1)
      c          = c.transpose(0, 1)
      hidden, hx = super().forward(input, [h, c])
      h, c       = hx
      h          = h.transpose(0, 1)
      c          = c.transpose(0, 1)
      return hidden, [h, c]
      
