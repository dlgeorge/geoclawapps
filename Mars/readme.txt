run the Martian floods.

Step 1:

place following topography file(s) in ./topo/ directory:

    'mars_500m_XYZ.dat'


Step 2:

from ./topo issue cmd:
>> python maketopo.py

Step 3:

from ./ issue cmd: (this step is normally not necessary...however we are using modules from the library and two locally modified routines...so make twice).
>> make new

Step 4:
from ./ issue cmd:
>> make .output