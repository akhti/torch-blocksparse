import torch
import torch_blocksparse
from time import time
from collections import OrderedDict
from utils import *
import unittest


def test_permute(N, C, H, W, in_order, out_order):
  dtype = torch.float32
  shape  = (N, C, H, W)
  stride_x = torch_blocksparse._permute.strides(N, C, H, W, in_order)
  stride_y = torch_blocksparse._permute.strides(N, C, H, W, out_order)
  x = torch.rand(N*C*H*W, requires_grad=True).as_strided(shape, stride_x).cuda().type(dtype)
  ry = torch.empty_strided(shape, stride_y, device=x.device, dtype=dtype)
  ry.copy_(x)
  ty = torch_blocksparse._permute.apply(x, in_order, out_order)
  ac_y = torch.allclose(ry, ty, rtol=1e-4, atol=1e-5)
  return ac_y

class TestPermute(unittest.TestCase):

  def test_full_fp32(self):
    dtype = torch.float32
    ac_y = test_permute(32, 32, 4, 4, 'NCHW', 'CHWN')
    self.assertTrue(ac_y)

if __name__ == '__main__':
  unittest.main()