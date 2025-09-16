# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class H3lpr(MakefilePackage):
    """Helper library for profiling, logging, and parsing."""

    # GitHub repository
    # You need to have a SSH key linked to your GitHub account
    git="ssh://git@github.com/van-Rees-Lab/h3lpr.git"

    # Versions
    version("develop", branch="develop")

    # Dependencies
    depends_on("mpi")

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
            "CC": spec["mpi"].mpicc,
            "CXX": spec["mpi"].mpicxx,
            "CXXFLAGS": "-03 -fopenmp",
            "LDFLAGS": "-fopenmp -lstdc++ -lm",
        }
        with open(env["ARCH_FILE"], "w") as f:
            for key in arch_file:
                f.write(f"{key}={arch_file[key]}")

