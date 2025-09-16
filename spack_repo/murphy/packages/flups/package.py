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
            "CCFLAGS": "-03 -DNDEBUG -DNO_PROF",
            "CXXFLAGS": "-03 -DNDEBUG -DNO_PROF",
            "LDFLAGS": "-fopenmp",
            # HDF5
            "HDF5_DIR": prefix,
            "HDF5_LIB": prefix.lib,
            "HDF5_DIR": prefix.dir,
            # H3LPR
            "H3LPR_DIR": prefix,
            "H3LPR_LIB": prefix.lib,
            "H3LPR_DIR": prefix.dir,
        }

        if spec.satisfies("+cuda"):
            # Use NVCC for CUDA
            env["OMPI_CC"] = "nvcc"
            env["OMPI_CXX"] = "nvcc"
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
            arch_file["FFTW_DIR"] = prefix,
            arch_file["FFTW_LIB"] = prefix.lib,
            arch_file["FFTW_DIR"] = prefix.dir,

        with open(env["ARCH_FILE"], "w") as f:
            for key in arch_file:
                f.write(f"{key}:={arch_file[key]}")

