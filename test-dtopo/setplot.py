
"""
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.

"""


from pyclaw.geotools import topotools
from pyclaw.data import Data
import pylab
import glob, os
from numpy import loadtxt
from matplotlib import image

WAdir = os.environ['WA']
LongBeachBermGE = image.imread(WAdir + '/maps/LongBeachBermGE.png')
extent = (235.93, 235.96, 46.3428, 46.3536)


# --------------------------
def setplot(plotdata):
# --------------------------

    """
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.

    """


    from pyclaw.plotters import colormaps, geoplot

    plotdata.clearfigures()  # clear any old figures,axes,items dat
#   plotdata.format = "netcdf"

    try:
        tsudata = open(plotdata.outdir+'/settsunami.data').readlines()
        for line in tsudata:
            if 'sealevel' in line:
                sealevel = float(line.split()[0])
                print "sealevel = ",sealevel
    except:
        print "Could not read sealevel, setting to 0."
        sealevel = 0.

    #clim_ocean = 2.0
    #clim_CC = 2.0
    clim_ocean = 5.0
    clim_CC = 5.0

    cmax_ocean = clim_ocean + sealevel
    cmin_ocean = -clim_ocean + sealevel
    cmax_CC = clim_CC + sealevel
    cmin_CC = -clim_CC + sealevel


    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        from pyclaw.plotters import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos=[0], format_string='ko', add_labels=True)

    def timeformat(t):
        from numpy import mod
        hours = int(t/3600.)
        tmin = mod(t,3600.)
        min = int(tmin/60.)
        sec = int(mod(tmin,60.))
        timestr = '%s:%s:%s' % (hours,str(min).zfill(2),str(sec).zfill(2))
        return timestr

    def title_hours(current_data):
        from pylab import title
        t = current_data.t
        timestr = timeformat(t)
        title('%s after earthquake' % timestr)

    def aframe(current_data):
        from pylab import figure, savefig

        if 0:
            tminutes = int(current_data.t / 60.)

            figure(0)
            fname = 'Pacific%s.png' % tminutes
            savefig(fname)
            print "Saved ",fname

            figure(11)
            fname = 'GraysHarbor%s.png' % tminutes
            savefig(fname)
            print "Saved ",fname

            figure(12)
            fname = 'Westport%s.png' % tminutes
            savefig(fname)
            print "Saved ",fname

            figure(13)
            fname = 'Ocosta%s.png' % tminutes
            savefig(fname)
            print "Saved ",fname

    plotdata.afterframe = aframe

    #-----------------------------------------
    # Figure for big area
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Pacific', figno=0)
    plotfigure.kwargs = {'figsize': (10,6)}
    #plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.cmd = 'subplot(121)'
    plotaxes.title = 'Pacific'
    plotaxes.scaled = False
    # modified for debug:
    #plotaxes.xlimits = [231.5,236.5]
    #plotaxes.ylimits = [45,49]
    #plotaxes.xlimits = [235.8,236.2]
    #plotaxes.ylimits = [46.1,46.9]

    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, savefig
        title_hours(current_data)
        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        a = gca()
        a.set_aspect(1./cos(46.349*pi/180.))
    plotaxes.afteraxes = aa

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                     -0.5: [0.5,0.5,1.0], \
                                      0.0: [1.0,1.0,1.0], \
                                      0.5: [1.0,0.5,0.5], \
                                      1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = cmin_ocean
    plotitem.imshow_cmax = cmax_ocean
    plotitem.add_colorbar = True
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [1]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [1]
    #plotaxes.afteraxes = addgauges

    # Add contour lines of bathymetry:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    from numpy import arange, linspace
    plotitem.contour_levels = linspace(-6000,0,7)
    plotitem.amr_contour_colors = ['g']  # color on each level
    plotitem.kwargs = {'linestyles':'solid'}
    plotitem.amr_contour_show = [0,0,1,0]  # show contours only on finest level
    plotitem.gridlines_show = 0
    plotitem.gridedges_show = 0

    # Add contour lines of topography:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    from numpy import arange, linspace
    plotitem.contour_levels = arange(0., 11., 1.)
    plotitem.amr_contour_colors = ['g']  # color on each level
    plotitem.kwargs = {'linestyles':'solid'}
    plotitem.amr_contour_show = [0,0,0,1]  # show contours only on finest level
    plotitem.gridlines_show = 0
    plotitem.gridedges_show = 0

    #-----------------------------------------
    # Figure for line plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='line', figno=2)
    #plotfigure.show = False

    def eta_slice(current_data):
        from pylab import find, nan, array
        x = current_data.x
        y = current_data.y
        q = current_data.q
        j1 = find(y[0,:] > 47.5)
        if len(j1)==0:
            x = eta = array([nan])
        else:
            j = min(j1)
            x = x[:,j]
            eta = q[:,j,3]
        return x,eta

    def B_slice(current_data):
        from pylab import find, nan, array
        x = current_data.x
        y = current_data.y
        q = current_data.q
        j1 = find(y[0,:] > 47.5)
        if len(j1)==0:
            x = B = array([nan])
        else:
            j = min(j1)
            x = x[:,j]
            eta = q[:,j,3]
            h = q[:,j,0]
            B = eta - h
        return x,B


    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('line')
    plotaxes.axescmd = 'subplot(212)'
    plotaxes.title = 'Bathymetry'


    # Water
    plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    plotitem.show = False
    plotitem.map_2d_to_1d = eta_slice
    plotitem.color = 'b'
    plotitem.kwargs = {'linewidth':2}


    # Topography
    plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    #plotitem.show = False
    plotitem.map_2d_to_1d = B_slice
    plotitem.color = 'k'
    plotitem.plotstyle = 'o-'
    def aa(current_data):
        from pylab import ticklabel_format
        ticklabel_format(format='plain',useOffset=False)
    plotaxes.afteraxes = aa


    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('linezoom')
    #plotaxes.show = False
    plotaxes.axescmd = 'subplot(211)'
    plotaxes.title = 'Surface'
    #plotaxes.xlimits = [-0.1,0.1]
    plotaxes.ylimits = [-4, 6]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    plotitem.map_2d_to_1d = eta_slice
    plotitem.color = 'b'
    plotitem.plotstyle = 'o-'
    plotitem.kwargs = {'linewidth':2}



    #-----------------------------------------
    # Figure for zoom2
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name="Gray's Harbor", figno=11)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize': (10,9)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.cmd = 'subplot(122)'
    plotaxes.title = "Gray's Harbor"
    plotaxes.scaled = False

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                      -0.5: [0.5,0.5,1.0], \
                                       0.0: [1.0,1.0,1.0], \
                                       0.5: [1.0,0.5,0.5], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = cmin_CC
    plotitem.imshow_cmax = cmax_CC
    plotitem.add_colorbar = True
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [0]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [0]
    plotaxes.xlimits = [235.8,236.2]
    plotaxes.ylimits = [46.75, 47.1]
    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, savefig
        #addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
    plotaxes.afteraxes = aa

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0.]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,0,1,0]
    plotitem.gridlines_show = 0
    plotitem.gridedges_show = 0

    #-----------------------------------------
    # Figure for zoom
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Washington', figno=10)
    plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Washington'
    plotaxes.scaled = False
    plotaxes.afteraxes = aa

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                      -0.1: [0.5,0.5,1.0], \
                                       0.0: [1.0,1.0,1.0], \
                                       0.1: [1.0,0.5,0.5], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = cmin_ocean
    plotitem.imshow_cmax = cmax_ocean
    plotitem.add_colorbar = True
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [1]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [1]
    plotaxes.xlimits = [235,236.5]
    plotaxes.ylimits = [46,49]
    plotaxes.afteraxes = aa



    #-----------------------------------------
    # Figure for zoom3
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Long Beach', figno=12)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize': (8,7)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Long Beach'
    plotaxes.scaled = False

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show = False
    plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                      -0.5: [0.5,0.5,1.0], \
                                       0.0: [1.0,1.0,1.0], \
                                       0.5: [1.0,0.5,0.5], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = cmin_ocean
    plotitem.imshow_cmax = cmax_ocean
    plotitem.add_colorbar = True
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [0]


    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    #plotitem.plot_var = 3
    land_cmap = colormaps.make_colormap({0.0: [0.0,0.0,1.0], \
                                       0.5: [1.0,0.0,0.0], \
                                       1.0: [0.0,1.0,0.0]})
    plotitem.imshow_cmap = geoplot.land_colors
    #plotitem.imshow_cmap = land_cmap
    plotitem.imshow_cmin = 0.
    plotitem.imshow_cmax = 10.
    plotitem.add_colorbar = False
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [0]
    plotaxes.xlimits = [235.90,235.98]
    plotaxes.ylimits = [46.30,46.39]
    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, imshow, \
                    savefig, plot
        from pyclaw.plotters.plottools import plotbox
        #addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        a = gca()
        #a.set_aspect(1./cos(46.86*pi/180.))
        a.set_aspect(1./cos(46.349*pi/180.))
        plot([235.9499],[46.3490],'wo')
        #extent = (235.8756, 235.9116, 46.854, 46.8756)
        #plotbox(extent)
        #imshow(OcostaGE,extent=extent, alpha=0.5)
        #extent = (235.81, 235.95, 46.85, 46.95)
        #imshow(WestportGE,extent=extent, alpha=0.8)
    plotaxes.afteraxes = aa

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0.0]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,0,1,0]
    plotitem.gridlines_show = 0
    plotitem.gridedges_show = 0

    #-----------------------------------------
    # Figure for zoom4
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Berm', figno=13)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize': (12,8)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Berm location'
    plotaxes.scaled = False

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show=False
    plotitem.plot_var = geoplot.depth
    #plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({0.0: [1.0,1.0,1.0], \
                                       0.5: [1.0,0.8,0.0], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = 0.
    plotitem.imshow_cmax = 3.
    plotitem.add_colorbar = True
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [1]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show=False
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 20.0
    plotitem.add_colorbar = False
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [1]

    #plotaxes.xlimits = [235.88, 235.905]
    #plotaxes.ylimits = [46.855, 46.87]
    plotaxes.xlimits = [235.947,235.951]
    plotaxes.ylimits = [46.347,46.35]
    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, imshow, \
                    savefig, plot
        addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        plot([235.9499],[46.3490],'wo')
        #extent = (235.8756, 235.9116, 46.854, 46.8756)
        #imshow(OcostaGE,extent=extent, alpha=0.5)
        a = gca()
        a.set_aspect(1./cos(46.349*pi/180.))
        #extent = (235.81, 235.95, 46.85, 46.95)
        #imshow(WestportGE,extent=extent, alpha=0.8)
    plotaxes.afteraxes = aa

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0.]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,0,1,0]
    plotitem.gridlines_show = 0
    plotitem.gridedges_show = 0



    #-----------------------------------------
    # Figure for zoom4 speed
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Ocosta speed', figno=14)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize': (12,8)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Ocosta'
    plotaxes.scaled = False

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show=False
    def speed(current_data):
        from numpy import sqrt,where
        q = current_data.q
        h = q[:,:,0]
        hu = q[:,:,1]
        hv = q[:,:,2]
        u = where(h>0.01, hu/h, 0.)
        v = where(h>0.01, hv/h, 0.)
        speed = sqrt(u**2 + v**2)
        return v

    plotitem.plot_var = speed
    #plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({0.0: [0.0,0.0,1.0], \
                                       0.5: [1.0,1.0,1.0], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = -3.
    plotitem.imshow_cmax = 3.
    plotitem.add_colorbar = True
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [1]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show=False
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 20.0
    plotitem.add_colorbar = False
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.amr_gridedges_show = [1]

    #plotaxes.xlimits = [235.88, 235.905]
    #plotaxes.ylimits = [46.855, 46.87]
    plotaxes.xlimits = [235.88, 235.935]
    plotaxes.ylimits = [46.845, 46.875]
    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, imshow, savefig
        addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        #extent = (235.8756, 235.9116, 46.854, 46.8756)
        #imshow(OcostaGE,extent=extent, alpha=0.5)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
        #extent = (235.81, 235.95, 46.85, 46.95)
        #imshow(WestportGE,extent=extent, alpha=0.8)
    plotaxes.afteraxes = aa

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0.]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,0,1,0]
    plotitem.gridlines_show = 0
    plotitem.gridedges_show = 0



    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='gauge plot', figno=300, \
                    type='each_gauge')
    #plotfigure.clf_each_gauge = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.ylimits = [-1,10]
    plotaxes.xlimits = [-1,10]
    plotaxes.title = 'Surface'

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 4
    plotitem.plotstyle = 'b-'


    def axes_gauge(current_data):
        from pylab import plot, legend, xticks, floor,\
            yticks,xlabel,savefig,xlim,ylim,xlabel,ylabel
        t = current_data.t
        gaugeno = current_data.gaugeno
        xticks(linspace(0,1,7),[str(i) for i in range(0,7,10)])
        xlabel('time (minutes) after quake',fontsize=15)
        ylabel('meters',fontsize=15)
        ylim(-1,10)


    plotaxes.afteraxes = axes_gauge




    #-----------------------------------------

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata


