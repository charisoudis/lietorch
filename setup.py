import os
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os.path as osp

# Set CUDA_HOME only if it's not already set (useful for Docker where this might be preset)
if 'CUDA_HOME' not in os.environ:
    os.environ['CUDA_HOME'] = '/usr/local/cuda'

ROOT = osp.dirname(osp.abspath(__file__))

setup(
    name='lietorch',
    version='0.2',
    description='Lie Groups for PyTorch',
    author='teedrz',
    packages=['lietorch'],
    ext_modules=[
        CUDAExtension(
            'lietorch_backends',
            include_dirs=[
                osp.join(ROOT, 'lietorch/include'),
                osp.join(ROOT, 'eigen'),
            ],
            sources=[
                'lietorch/src/lietorch.cpp',
                'lietorch/src/lietorch_gpu.cu',
                'lietorch/src/lietorch_cpu.cpp'
            ],
            extra_compile_args={
                'cxx': ['-O2'],
                'nvcc': ['-O2']
            }
        ),
        CUDAExtension(
            'lietorch_extras',
            sources=[
                'lietorch/extras/altcorr_kernel.cu',
                'lietorch/extras/corr_index_kernel.cu',
                'lietorch/extras/se3_builder.cu',
                'lietorch/extras/se3_inplace_builder.cu',
                'lietorch/extras/se3_solver.cu',
                'lietorch/extras/extras.cpp',
            ],
            extra_compile_args={
                'cxx': ['-O2'],
                'nvcc': ['-O2']
            }
        ),
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)