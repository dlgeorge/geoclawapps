
% This routine is called after setplot2.m by plotclaw2.
%
% Set some additional things for ploting GeoClaw output.
%

%PlotType = 11;     % = 11 for colored surface plot
                   % = 12 for contour plot

PlotFlow = 1;      % plot the surface of the flow
PlotTopo = 1;      % plot the topography
ContourValues = linspace(0.001,1.0,10);
topoContourValues = 30;   % Contour levels for topo. 
                          % Set to either a scalar or vector
                        


geo_setzcolormaps;    % set up some useful default colormaps for land, water

zWaterColorsMalpasset = [0  DarkBlue;
                          50 Blue;
                         100 LightBlue];
                     
zWaterColorsMalpasset = [98  LightBlue;
                          100 Blue;
                         102 DarkBlue];
                     
zWaterColorsMalpasset = [98  0 1 1;
                          100 Blue;
                         102 DarkBlue];

zLandColorsMalpasset = [   0  DarkGreen;
                           25  Green;
                           50  LightGreen;
                           100  Tan;
                           150 Brown;
                           200 White];
                       
zLandColorsMalpassetZoom = [   0  DarkGreen;
                           10  Green;
                           15  LightGreen;
                           25  Brown;
                           35 Tan;
                           ];
                       
zLandColorsMissoula = [   0  DarkGreen;
                           250  Green;
                           500  LightGreen;
                           1000  Tan;
                           1500 Brown;
                           2000 White];
                       
zFlume = [ 1.117 Tan;
            1.115 Gray8];
        
zRedWhiteBlue = [-10 Green
            -1 Red;
            0  White;
            1  Blue];
        
z_flumedepth = [.5 DarkBlue;
                .1 White;
                0.0 Red];

z_velocity = [-1.0e-1 DarkBlue;
                0 Blue;
                1.0e-1 Red];
            
z_depth = [0. White
            20. LightBlue
            100 Blue
            250 DarkBlue];
        
        
z_m = [0.0 Red;
        0.42-1.0e-5 Blue;
        0.42 White
        0.42+1.e-5 Green;
            1.0 Red];
        
 zDigPressure = [0  White;
                10/18.5  LightGreen;
                1  Blue];
        
%flow_colormap = z_velocity;
%flow_colormap =zDigPressure;
flow_colormap = z_depth;
%flow_colormap = z_m;
%flow_colormap = zWaterColorsMalpasset;
topo_colormap =zLandColorsMissoula;



% or for non default colormaps for the water 
% set flowcolormatrix to any colormap desired (ie any m by 3 rgb matrix) 
%[flowcolormatrix,ncolors]=deacolor; 
%[ncolors,n]=size(flowcolormatrix);
%flow_colormap=[linspace(-TsAmp,TsAmp,ncolors)',flowcolormatrix];

