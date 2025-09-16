# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------

from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *

class Flups(MakefilePackage, CudaPackage):
    """FLUPS - A Fourier-based Library of Unbounded Poisson Solvers"""

    # GitLab repository
    # You need to authenticate using an access token...
    git="https://git.immc.ucl.ac.be/examples/flups.git"

    # Versions
    version("gpu", branch="dev-gpu")

    # Dependencies
    depends_on("mpi")
    depends_on("hdf5")
    depends_on("h3lpr")
    depends_on("fftw", when="~cuda")

    def edit(self, spec, prefix):
        # Use MPI's compiler
        env["CC"] = spec["mpi"].mpicc
        env["CXX"] = spec["mpi"].mpicxx
        env["F77"] = spec["mpi"].mpif77
        env["FC"] = spec["mpi"].mpifc

        # Set the install prefix
        env["PREFIX"] = prefix

        # Set the arch file
        env["ARCH_FILE"] = "make_arch/make.spack"

        # Write out said arch file
        arch_file = {
            "OPTS": "-DNDEBUG",
            "CC": spec["mpi"].mpicc,
            "CXX": spec["mpi"].mpicxx,
            "CCFLAGS": "-O3 -DNDEBUG -DNO_PROF",
            "CXXFLAGS": "-O3 -DNDEBUG -DNO_PROF",
            # HDF5
            "HDF5_LIB": f"{spec['hdf5'].home}/lib",
            "HDF5_INC": f"{spec['hdf5'].home}/include",
            # H3LPR
            "H3LPR_LIB": f"{spec['h3lpr'].home}/lib",
            "H3LPR_INC": f"{spec['h3lpr'].home}/include",
        }

        if spec.satisfies("+cuda"):
            # Use NVCC for CUDA
            env["MPICH_CC"] = "nvcc"
            env["MPICH_CXX"] = "nvcc"
            # Set backend
            arch_file["OPTS"] += " -DBACKEND_CUDA"
            arch_file["CCFLAGS"] += " -DBACKEND_CUDA"
            arch_file["CXXFLAGS"] += " -DBACKEND_CUDA"
        else:
            # Set backend
            arch_file["OPTS"] += " -DBACKEND_FFTW"
            arch_file["CCFLAGS"] += " -DBACKEND_FFTW"
            arch_file["CXXFLAGS"] += " -DBACKEND_FFTW"
            # FFTW
            arch_file["FFTW_LIB"] = f"{spec['fftw'].home}/lib"
            arch_file["FFTW_INC"] = f"{spec['fftw'].home}/include"

        with open(env["ARCH_FILE"], "w") as f:
            for key in arch_file:
                f.write(f"{key}:={arch_file[key]}\n")

