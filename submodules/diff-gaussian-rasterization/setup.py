#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

from setuptools import setup, find_packages
from torch.utils.cpp_extension import CUDAExtension, BuildExtension
import os
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))


# Trigger CMake to clone and setup glm in the third_party/glm/ directory.
def build_glm_with_cmake():
    build_temp_dir = os.path.join(current_dir, "build")
    if not os.path.exists(build_temp_dir):
        os.makedirs(build_temp_dir)

    subprocess.check_call(["cmake", ".."], cwd=build_temp_dir)
    subprocess.check_call(["make"], cwd=build_temp_dir)


# Run the CMake build.
build_glm_with_cmake()

setup(
    name="diff_gaussian_rasterization",
    packages=find_packages(),
    ext_modules=[
        CUDAExtension(
            name="diff_gaussian_rasterization._C",
            sources=[
                "cuda_rasterizer/rasterizer_impl.cu",
                "cuda_rasterizer/forward.cu",
                "cuda_rasterizer/backward.cu",
                "rasterize_points.cu",
                "ext.cpp",
            ],
            extra_compile_args={"nvcc": ["-I" + os.path.join(current_dir, "third_party/glm/")]},
        )
    ],
    cmdclass={"build_ext": BuildExtension},
)
