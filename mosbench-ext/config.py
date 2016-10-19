from mparts.configspace import ConfigSpace

import hosts

# If set to True, do as few experiments as quickly as possible to test
# the setup.  This is useful to do before the full benchmark suite
# because it will almost certainly uncover misconfigurations that
# could halt a lengthy full benchmark part way through.
#sanityRun = True
sanityRun = False

# For an explanation of configuration spaces and a description of why
# we use '*' and '+' all over this file, see the module documentation
# for mparts.configspace.  In short, * combines configuration options,
# while + specifies alternate configurations.  Likewise, passing a
# list to mk creates a set of alternate configurations.

mk = ConfigSpace.mk

##################################################################
# Shared configuration
#

shared = ConfigSpace.unit()

# The primary host that will run the benchmark applications.
shared *= mk(primaryHost = hosts.primaryHost)

# benchRoot specifies the directory on the primary host where MOSBENCH
# was checked out or unpacked.
shared *= mk(benchRoot = "~/github/mosbench-ext")

# textRoot specifies the directory on the primary host where the text
# to use for the Psearchy indexing benchmark can be found.  To
# reproduce the results in the paper, this should be a pristine check
# out of Linux 2.6.35-rc5.
shared *= mk(textRoot = "~/github/scalablelinux")

# kernelRoot specifies the directory on the primary host where the
# kernel source to use for the gmake benchmark can be found.  To
# reproduce the results in the paper, this should be a check out of
# Linux 2.6.35-rc5.  This can be the same directory used for textRoot
# above.
shared *= mk(kernelRoot = "~/github/scaleablelinux")

# fs specifies which type of file system to use.  This can be any file
# system type known to mkmounts except hugetlbfs.
shared *= mk(fs = "tmpfs-separate")
#shared *= mk(fs = "tmpfs")

# trials is the number of times to run each benchmark.  The best
# result will be taken.
if sanityRun:
    shared *= mk(trials = 1)
else:
    shared *= mk(trials = 5)

# hotplug specifies whether or not to use CPU hotplug to physically
# disable cores not in use by the benchmark.  All cores should be
# re-enabled when the benchmark exits, even after an error.  Several
# of the benchmarks do not otherwise restrict which cores they use,
# and thus will give bogus results without this.
shared *= mk(hotplug = True)

CORECOUNT = 120
# cores specifies the number of cores to use.  This must be
# non-constant and must be the last variable in the shared
# configuration for the graphing tools to work (which also means it
# generally shouldn't be overridden per benchmark).
if sanityRun:
    shared *= mk(cores = [2], nonConst = True)
else:
    shared *= mk(cores = [CORECOUNT], nonConst = True)

##################################################################
# Exim
#
# eximBuild - The build name of Exim to run.  Corresponds to a
# subdirectory of the exim/ directory that contains an Exim
# installation.
#
# eximPort - The port Exim should listen on.
#
# clients - The number of client load generators to run.

import exim

exim = mk(benchmark = exim.runner, nonConst = True)

exim *= mk(eximBuild = "exim-mod")
exim *= mk(eximPort = 2524)
exim *= mk(clients = 120)

configSpace = exim.merge(shared)

if __name__ == "__main__":
    from mparts.manager import generateManagers
    from mparts.rpc import print_remote_exception
    import sys
    sys.excepthook = print_remote_exception
    for (m, cfg) in generateManagers("sanity" if sanityRun else "results", configSpace):
        cfg.benchmark.run(m, cfg)
