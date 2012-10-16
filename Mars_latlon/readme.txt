run the Martian floods.

Steps 1 & 2 are only necessary if you want to save memory. Otherwise, you can use original topo files with XYZ columns (and no header) directly. In setrun.py specify those files instead, and use topotype = 1, rather than topotype =2 in the list in setrun.py:

geodata.topofiles.append([topotype, minlevel,maxlevel,t0,tend,fname])

Step 1:

place topography file(s) in ./topo/ directory:

    'athabasca_lon_lat_z_approx.asc'


Step 2:

from ./topo issue cmd:
>> python maketopo.py

Step 3:

from ./ issue cmd: (this step is normally not necessary...however we are using modules from the library and two locally modified routines...so make twice).
>> make new

Step 4:
from ./ issue cmd:
>> make .output


to adjust the spring source, see line 97 in ./src2_geo.f

to add higher refinement near the flowing water, adjust mxnest = 3 in setrun.py