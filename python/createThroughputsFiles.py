# Create a set of files to replace the "baseline" files in the THROUGHPUTS repository.
# Add header information that tracks the files here and also adds cutoff wavelength information.
import os
import shutil
import subprocess
import numpy as np
from lsst.sims.photUtils import Bandpass, Sed
import bandpassUtils as bu

# throughput files:
# atmos_std.dat, atmos_10.dat
# darksky.dat
# detector.dat
# filter_[ugrizy].dat
# lens[123].dat
# m[123].dat
# total_[ugrizy].dat
# hardware_[ugrizy].dat

# Read the data needed from the syseng_throughput repo.
defaultDirs = bu.setDefaultDirs()
addLosses = True

detector = bu.buildDetector(defaultDirs['detector'], addLosses)
filters = bu.buildFilters(defaultDirs['filters'], addLosses)
lens1 = bu.buildLens(defaultDirs['lens1'], addLosses)
lens2 = bu.buildLens(defaultDirs['lens2'], addLosses)
lens3 = bu.buildLens(defaultDirs['lens3'], addLosses)
m1 = bu.buildMirror(defaultDirs['mirror1'], addLosses)
m2 = bu.buildMirror(defaultDirs['mirror2'], addLosses)
m3 = bu.buildMirror(defaultDirs['mirror3'], addLosses)
atmos_std = bu.readAtmosphere(defaultDirs['atmosphere'], atmosFile='pachonModtranAtm_12_aerosol.dat')
atmos_10 = bu.readAtmosphere(defaultDirs['atmosphere'], atmosFile='atmos_10_aerosol.dat')
darksky = Sed()
darksky.readSED_flambda(os.path.join(defaultDirs['atmosphere'], 'darksky.dat'))
hardware, system = bu.buildHardwareAndSystem(defaultDirs, addLosses=addLosses, atmosphereOverride=atmos_std)

# Write the data to disk.
outDir = 'baseline'
if not os.path.isdir(outDir):
    os.makedirs(outDir)

shutil.copy('../README.md', os.path.join(outDir, 'README.md'))

version = subprocess.check_output(['git', 'describe']).strip()
sha1 = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()
print "version", version, "sha1", sha1
versioninfo = '# Version %s\n'%(version)
versioninfo += '# sha1 %s\n' %(sha1)

header = '# LSST Throughputs files created from syseng_throughputs repo\n'
header += versioninfo

atmosheader = header + '# Aerosols added to atmosphere\n'
systemheader = header + '# Aerosols added to atmosphere\n'

skyheader = '# LSST dark sky SED from syseng_throughputs repo\n'
skyheader += versioninfo

perfilterheader = {}
for f in filters:
    good = np.where(filters[f].sb > 0)[0]
    wavelen_blue = filters[f].wavelen[good[0]-1]
    wavelen_red = filters[f].wavelen[good[-1]+1]
    perfilterheader[f] = '# Wavelen_cutoff_BLUE %.2f\n' % (wavelen_blue)
    perfilterheader[f] += '# Wavelen_cutoff_RED %.2f\n' % (wavelen_red)


detector.writeThroughput(os.path.join(outDir, 'detector.dat'), print_header=header)
lens1.writeThroughput(os.path.join(outDir, 'lens1.dat'), print_header=header)
lens2.writeThroughput(os.path.join(outDir, 'lens2.dat'), print_header=header)
lens3.writeThroughput(os.path.join(outDir, 'lens3.dat'), print_header=header)
m1.writeThroughput(os.path.join(outDir, 'm1.dat'), print_header=header)
m2.writeThroughput(os.path.join(outDir, 'm2.dat'), print_header=header)
m3.writeThroughput(os.path.join(outDir, 'm3.dat'), print_header=header)
atmos_std.writeThroughput(os.path.join(outDir, 'atmos_std.dat'), print_header=atmosheader)
atmos_10.writeThroughput(os.path.join(outDir, 'atmos_10.dat'), print_header=atmosheader)
darksky.writeSED(os.path.join(outDir, 'darksky.dat'), print_header=skyheader)

for f in filters:
    filters[f].writeThroughput(os.path.join(outDir, 'filter_%s.dat' %(f)), print_header=header+perfilterheader[f])
    hardware[f].writeThroughput(os.path.join(outDir, 'hardware_%s.dat' %(f)), print_header=header+perfilterheader[f])
    system[f].writeThroughput(os.path.join(outDir, 'total_%s.dat' %(f)), print_header=systemheader+perfilterheader[f])




