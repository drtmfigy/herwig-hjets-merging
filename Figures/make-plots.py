#! /usr/bin/env python

"""\
Usage: %prog [options] file.dat [file2.dat ...]

TODO
 * Optimise output for e.g. lots of same-height bins in a row
 * Add a RatioFullRange directive to show the full range of error bars + MC envelope in the ratio
 * Tidy LaTeX-writing code -- faster to compile one doc only, then split it?
 * Handle boolean values flexibly (yes, no, true, false, etc. as well as 1, 0)
"""

##
## This program is copyright by Hendrik Hoeth <hoeth@linta.de> and
## the Rivet team https://rivet.hepforge.org. It may be used
## for scientific and private purposes. Patches are welcome, but please don't
## redistribute changed versions yourself.
##

## Check the Python version
import sys
if sys.version_info[:3] < (2,6,0):
    print "make-plots requires Python version >= 2.6.0... exiting"
    sys.exit(1)

## Try to rename the process on Linux
try:
    import ctypes
    libc = ctypes.cdll.LoadLibrary('libc.so.6')
    libc.prctl(15, 'make-plots', 0, 0, 0)
except Exception, e:
    pass


import os, logging, re
import tempfile
import getopt
import string
import ast
from math import *


## Regex patterns
pat_begin_block = re.compile(r'^#+\s*BEGIN ([A-Z0-9_]+) ?(\S+)?')
pat_end_block =   re.compile('^#+\s*END ([A-Z0-9_]+)')
pat_comment = re.compile('^#|^\s*$')
pat_property = re.compile('^(\w+?)=(.*)$')
pat_path_property  = re.compile('^(\S+?)::(\w+?)=(.*)$')


def fuzzyeq(a, b, tolerance=1e-6):
    "Fuzzy equality comparison function for floats, with given fractional tolerance"
    # if type(a) is not float or type(a) is not float:
    #     print a, b
    if (a == 0 and abs(b) < 1e-12) or (b == 0 and abs(a) < 1e-12):
        return True
    return 2.0*abs(a-b)/abs(a+b) < tolerance


def is_end_marker(line, blockname):
    m = pat_end_block.match(line)
    return m and m.group(1) == blockname

def is_comment(line):
    return pat_comment.match(line) is not None



class Inputdata(object):
    def __init__(self, filename):
        self.filename=filename+".dat"
        self.histos = {}
        self.special = {}
        self.functions = {}

        self.description = {}
        self.pathdescriptions = []

        self.description['is2dim'] = False
        f = open(filename+'.dat')
        for line in f:
            m = pat_begin_block.match(line)
            if m:
                name, path = m.group(1,2)
                if path is None and name != 'PLOT':
                    raise Exception('BEGIN sections need a path name.')

                ## Pass the reading of the block to separate functions
                if name == 'PLOT':
                    self.read_input(f);
                elif name == 'SPECIAL':
                    self.special[path] = Special(f)
                elif name == 'HISTOGRAM' or name == 'HISTOGRAM2D':
                    self.histos[path] = Histogram(f)
                    self.histos[path].path = path
                    self.description['is2dim'] = self.histos[path].is2dim
                elif name == 'HISTO1D':
                    self.histos[path] = Histo1D(f)
                elif name == 'HISTO2D':
                    self.histos[path] = Histo2D(f)
                    self.description['is2dim'] = True
                elif name == 'FUNCTION':
                    self.functions[path] = Function(f)
#            elif is_comment(line):
#                continue
#            else:
#                self.read_path_based_input(line)
        f.close()

        self.apply_config_files(opts.CONFIGFILES)

        self.description['PlotSizeX'] = 10.
        if self.description['is2dim']:
            self.description['PlotSizeX'] -= 1.5
        self.description['PlotSizeY'] = 4.
        if self.description.has_key('PlotSize') and self.description['PlotSize']!='':
            plotsizex,plotsizey = self.description['PlotSize'].split(',')
            self.description['PlotSizeX'] = float(plotsizex)
            self.description['PlotSizeY'] = float(plotsizey)
            del self.description['PlotSize']

        self.description['RatioPlotSizeY'] = 0.
        if self.description.has_key('MainPlot') and self.description['MainPlot']=='0':
            self.description['RatioPlot'] = '1'
            self.description['PlotSizeY'] = 0.
        if self.description.has_key('RatioPlot') and self.description['RatioPlot']!='0':
            if self.description.has_key('RatioPlotYSize') and self.description['RatioPlotYSize']!='':
                self.description['RatioPlotSizeY'] = float(self.description['RatioPlotYSize'])
            else:
                if self.description.has_key('MainPlot') and self.description['MainPlot']=='0':
                    self.description['RatioPlotSizeY'] = 6.
                else:
                    self.description['RatioPlotSizeY'] = 2.

        self.description['LogX'] = self.description.has_key('LogX') and self.description['LogX']=='1'
        self.description['LogY'] = self.description.has_key('LogY') and self.description['LogY']=='1'
        self.description['LogZ'] = self.description.has_key('LogZ') and self.description['LogZ']=='1'
        if self.description.has_key('Rebin'):
            for i in self.histos:
                self.histos[i].description['Rebin'] = self.description['Rebin']

        histoordermap = {}
        histolist = self.histos.keys()
        if self.description.has_key('DrawOnly'):
            histolist = filter(self.histos.keys().count, self.description['DrawOnly'].strip().split())
        for histo in histolist:
            order = 0
            if self.histos[histo].description.has_key('PlotOrder'):
                order = int(self.histos[histo].description['PlotOrder'])
            if not order in histoordermap:
                histoordermap[order] = []
            histoordermap[order].append(histo)
        sortedhistolist = []
        for i in sorted(histoordermap.keys()):
            sortedhistolist.extend(histoordermap[i])
        self.description['DrawOnly']=sortedhistolist


        # inherit various values from histograms if not explicitly
        # set.
        for k in ['LogX', 'LogY', 'LogZ',
                'XLabel', 'YLabel', 'ZLabel',
                'XCustomMajorTicks', 'YCustomMajorTicks',
                'ZCustomMajorTicks']:
            self.inherit_from_histos(k)

        return


    def inherit_from_histos(self, k):
        # note: this will inherit the key from a random histogram:
        # only use if you're sure all histograms have this key!
        if not self.description.has_key(k):
            h = list(self.histos.itervalues())[0]
            if h.description.has_key(k):
                self.description[k] = h.description[k]

        return



    def read_input(self, f):
        for line in f:
            if is_end_marker(line, 'PLOT'):
                break
            elif is_comment(line):
                continue
            m = pat_property.match(line)
            if m:
                prop, value = m.group(1,2)
                if prop in self.description:
                    logging.debug("Overwriting property %s = %s -> %s" % (prop, self.description[prop], value))
                ## Use strip here to deal with DOS newlines containing \r
                self.description[prop.strip()] = value.strip()


    def apply_config_files(self, conffiles):
        if conffiles is not None:
            for filename in conffiles:
                cf = open(filename,'r')
                lines = cf.readlines()
                for i in range(0, len(lines)):
                    ## First evaluate PLOT sections
                    m = pat_begin_block.match(lines[i])
                    if m and m.group(1) == 'PLOT' and re.match(m.group(2),self.filename):
                        while i<len(lines)-1:
                            i = i+1
                            if is_end_marker(lines[i], 'PLOT'):
                                break
                            elif is_comment(lines[i]):
                                continue
                            m = pat_property.match(lines[i])
                            if m:
                                prop, value = m.group(1,2)
                                if prop in self.description:
                                    logging.debug("Overwriting from conffile property %s = %s -> %s" % (prop, self.description[prop], value))
                                ## Use strip here to deal with DOS newlines containing \r
                                self.description[prop.strip()] = value.strip()
                    elif is_comment(lines[i]):
                        continue
                    else:
                        ## Then evaluate path-based settings, e.g. for HISTOGRAMs
                        m = pat_path_property.match(lines[i])
                        if m:
                            regex, prop, value=m.group(1,2,3)
                            for obj_dict in [self.special, self.histos, self.functions]:
                                for path, obj in obj_dict.iteritems():
                                    if re.match(regex, path):
                                        ## Use strip here to deal with DOS newlines containing \r
                                        obj.description.update({prop.strip() : value.strip()})
                cf.close()




class Plot(object):
    def __init__(self,inputdata):
        pass

    def set_normalization(self,inputdata):
        for method in ['NormalizeToIntegral', 'NormalizeToSum']:
            if inputdata.description.has_key(method):
                for i in inputdata.description['DrawOnly']:
                    if not inputdata.histos[i].description.has_key(method):
                        inputdata.histos[i].description[method] = inputdata.description[method]
        if inputdata.description.has_key('Scale'):
            for i in inputdata.description['DrawOnly']:
                inputdata.histos[i].description['Scale'] = float(inputdata.description['Scale'])
        for i in inputdata.description['DrawOnly']:
            inputdata.histos[i].mangle_input()

    def stack_histograms(self,inputdata):
        if inputdata.description.has_key('Stack'):
            foo=[]
            for i in inputdata.description['Stack'].strip().split():
                if i in inputdata.histos.keys():
                    foo.append(i)
            previous=''
            for i in foo:
                if previous!='':
                    inputdata.histos[i].add(inputdata.histos[previous])
                previous=i

    def set_histo_options(self,inputdata):
        if inputdata.description.has_key('ConnectGaps'):
            for i in inputdata.histos.keys():
                if not inputdata.histos[i].description.has_key('ConnectGaps'):
                    inputdata.histos[i].description['ConnectGaps']=inputdata.description['ConnectGaps']

    def set_borders(self,inputdata):
        self.set_xmax(inputdata)
        self.set_xmin(inputdata)
        self.set_ymax(inputdata)
        self.set_ymin(inputdata)
        self.set_zmax(inputdata)
        self.set_zmin(inputdata)
        inputdata.description['Borders']=(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)

    def set_xmin(self,inputdata):
        if inputdata.description.has_key('XMin'):
            self.xmin = float(inputdata.description['XMin'])
        else:
            self.xmin = min(inputdata.histos[i].getXMin() for i in inputdata.description['DrawOnly'])

    def set_xmax(self,inputdata):
        #print inputdata.description
        if inputdata.description.has_key('XMax'):
            self.xmax = float(inputdata.description['XMax'])
        else:
            #print inputdata.description['DrawOnly']
            self.xmax = max(inputdata.histos[i].getXMax() for i in inputdata.description['DrawOnly'])

    def set_ymin(self,inputdata):
        if inputdata.description.has_key('YMin'):
            self.ymin = float(inputdata.description['YMin'])
        else:
            foo=[]
            for i in inputdata.description['DrawOnly']:
                foo.append(inputdata.histos[i].getYMin(self.xmin, self.xmax, inputdata.description['LogY']))
            if inputdata.description['is2dim']:
                self.ymin=min(foo)
            else:
                showzero = True
                if inputdata.description.has_key('ShowZero'):
                    if inputdata.description['ShowZero']=='0':
                        showzero = False
                if showzero:
                    if min(foo) > -1e-4:
                        self.ymin = 0
                    else:
                        self.ymin = 1.1*min(foo)
                else:
                    if min(foo) < -1e-4:
                        self.ymin = 1.1*min(foo)
                    elif min(foo) < 1e-4:
                        self.ymin = 0
                    else:
                        self.ymin = 0.9*min(foo)

                if inputdata.description['LogY']:
                    foo=[item for item in foo if item>0.0]
                    if len(foo)==0:
                        if self.ymax==0:
                            self.ymax=1
                        foo.append(2e-7*self.ymax)
                    fullrange = opts.FULL_RANGE
                    if inputdata.description.has_key('FullRange'):
                        if inputdata.description['FullRange']=='1':
                            fullrange = True
                        else:
                            fullrange = False
                    if fullrange:
                        self.ymin = min(foo)/1.7
                    else:
                        self.ymin = max(min(foo)/1.7, 2e-7*self.ymax)
                if self.ymin==self.ymax:
                    self.ymin-=1
                    self.ymax+=1

    def set_ymax(self,inputdata):
        if inputdata.description.has_key('YMax'):
            self.ymax = float(inputdata.description['YMax'])
        else:
            foo=[]
            for i in inputdata.description['DrawOnly']:
                foo.append(inputdata.histos[i].getYMax(self.xmin, self.xmax))
            if inputdata.description['is2dim']:
                self.ymax=max(foo)
            else:
                if inputdata.description['LogY']:
                    self.ymax=1.7*max(foo)
                else:
                    self.ymax=1.1*max(foo)

    def set_zmin(self,inputdata):
        if inputdata.description.has_key('ZMin'):
            self.zmin = float(inputdata.description['ZMin'])
        else:
            foo=[]
            for i in inputdata.description['DrawOnly']:
                foo.append(inputdata.histos[i].getZMin(self.xmin, self.xmax, self.ymin, self.ymax))
            if not foo:
                self.zmin = min(foo)
            else:
                showzero = True
                if inputdata.description.has_key('ShowZero'):
                    if inputdata.description['ShowZero']=='0':
                        showzero = False
                if showzero:
                    if min(foo) > -1e-4:
                        self.zmin = 0
                    else:
                        self.zmin = 1.1*min(foo)
                else:
                    if min(foo) < -1e-4:
                        self.zmin = 1.1*min(foo)
                    elif min(foo) < 1e-4:
                        self.zmin = 0
                    else:
                        self.zmin = 0.9*min(foo)

                if inputdata.description['LogZ']:
                    foo=[item for item in foo if item>0.0]
                    if len(foo)==0:
                        if self.zmax==0:
                            self.zmax=1
                        foo.append(2e-7*self.zmax)
                    fullrange = opts.FULL_RANGE
                    if inputdata.description.has_key('FullRange'):
                        if inputdata.description['FullRange']=='1':
                            fullrange = True
                        else:
                            fullrange = False
                    if fullrange:
                        self.zmin = min(foo)/1.7
                    else:
                        self.zmin = max(min(foo)/1.7, 2e-7*self.zmax)
                if self.zmin==self.zmax:
                    self.zmin-=1
                    self.zmax+=1

    def set_zmax(self,inputdata):
        if inputdata.description.has_key('ZMax'):
            self.zmax = float(inputdata.description['ZMax'])
        else:
            foo=[]
            for i in inputdata.description['DrawOnly']:
                foo.append(inputdata.histos[i].getZMax(self.xmin, self.xmax, self.ymin, self.ymax))
            if foo:
                self.zmax = max(foo)
            else:
                self.zmax = 1


    def draw(self):
        pass

    def write_header(self,inputdata):
        if inputdata.description.has_key('LeftMargin') and inputdata.description['LeftMargin']!='':
            inputdata.description['LeftMargin'] = float(inputdata.description['LeftMargin'])
        else:
            inputdata.description['LeftMargin'] = 1.4
        if inputdata.description.has_key('RightMargin') and inputdata.description['RightMargin']!='':
            inputdata.description['RightMargin'] = float(inputdata.description['RightMargin'])
        else:
            inputdata.description['RightMargin'] = 0.35
        if inputdata.description.has_key('TopMargin') and inputdata.description['TopMargin']!='':
            inputdata.description['TopMargin'] = float(inputdata.description['TopMargin'])
        else:
            inputdata.description['TopMargin'] = 0.65
        if inputdata.description.has_key('BottomMargin') and inputdata.description['BottomMargin']!='':
            inputdata.description['BottomMargin'] = float(inputdata.description['BottomMargin'])
        else:
            inputdata.description['BottomMargin'] = 0.95
        if inputdata.description['is2dim']:
            inputdata.description['RightMargin'] += 1.5
        papersizex = inputdata.description['PlotSizeX'] + 0.1 + \
                     inputdata.description['LeftMargin'] + inputdata.description['RightMargin']
        papersizey = inputdata.description['PlotSizeY'] + inputdata.description['RatioPlotSizeY']*int(inputdata.description['RatioPlot']) + 0.1 + \
                     inputdata.description['TopMargin'] + inputdata.description['BottomMargin']
        #
        out = ""
        out += '\\documentclass{article}\n'
        if opts.OUTPUT_FONT == "MINION":
            out += ('\\usepackage{minion}\n')
        elif opts.OUTPUT_FONT == "PALATINO_OSF":
            out += ('\\usepackage[osf,sc]{mathpazo}\n')
        elif opts.OUTPUT_FONT == "PALATINO":
            out += ('\\usepackage{mathpazo}\n')
        elif opts.OUTPUT_FONT == "TIMES":
            out += ('\\usepackage{mathptmx}\n')
        elif opts.OUTPUT_FONT == "HELVETICA":
            out += ('\\renewcommand{\\familydefault}{\\sfdefault}\n')
            out += ('\\usepackage{sfmath}\n')
            out += ('\\usepackage{helvet}\n')
            out += ('\\usepackage[symbolgreek]{mathastext}\n')
        for pkg in opts.LATEXPKGS:
            out += ('\\usepackage{%s}\n' % pkg)
        out += ('\\usepackage{pst-all}\n')
        out += ('\\selectcolormodel{rgb}\n')
        out += ('\\usepackage{amsmath}\n')
        out += ('\\usepackage{amssymb}\n')
        out += ('\\usepackage{relsize}\n')
        out += ('\\usepackage[dvips,\n')
        out += ('  left=%4.3fcm, right=0cm,\n' %(inputdata.description['LeftMargin']-0.45,))
        out += ('  top=%4.3fcm,  bottom=0cm,\n' %(inputdata.description['TopMargin']-0.30,))
        out += ('  paperwidth=%scm,paperheight=%scm\n' %(papersizex,papersizey))
        out += (']{geometry}\n')
        out += ('\\begin{document}\n')
        out += ('\\pagestyle{empty}\n')
        out += ('\\SpecialCoor\n')
        out += ('\\begin{pspicture}(0,0)(0,0)\n')
        out += ('\\psset{xunit=%scm}\n' %(inputdata.description['PlotSizeX']))
        if inputdata.description['is2dim']:
            if inputdata.description.has_key('ColorSeries') and inputdata.description['ColorSeries']!='':
                colorseries = inputdata.description['ColorSeries']
            else:
                colorseries = '{hsb}{grad}[rgb]{0,0,1}{-.700,0,0}'
            out += ('\\definecolorseries{gradientcolors}%s\n' %colorseries)
            out += ('\\resetcolorseries[130]{gradientcolors}\n')
        return out

    def write_footer(self):
        out = ""
        out += ('\\end{pspicture}\n')
        out += ('\\end{document}\n')
        return out



class MainPlot(Plot):
    def __init__(self, inputdata):
        self.set_normalization(inputdata)
        self.stack_histograms(inputdata)
        if (inputdata.description.has_key('GofLegend')  and inputdata.description['GofLegend']=='1') or \
           (inputdata.description.has_key('GofFrame')   and inputdata.description['GofFrame']!='') and not \
           (inputdata.description.has_key('TaylorPlot') and inputdata.description['TaylorPlot']=='1'):
            self.calculate_gof(inputdata)
    
    
        self.set_histo_options(inputdata)
        self.set_borders(inputdata)
        self.yoffset = inputdata.description['PlotSizeY']
        self.coors = Coordinates(inputdata)

    def draw(self, inputdata):
        out = ""
        out += ('\n%\n% MainPlot\n%\n')
        out += ('\\psset{yunit=%scm}\n' %(self.yoffset))
        out += ('\\rput(0,-1){%\n')
        out += ('\\psset{yunit=%scm}\n' %(inputdata.description['PlotSizeY']))
        out += self._draw(inputdata)
        out += ('}\n')
        return out

    def _draw(self, inputdata):
        out = ""
        if inputdata.description.has_key('DrawSpecialFirst') and inputdata.description['DrawSpecialFirst']=='1':
            for i in inputdata.special.keys():
                out += inputdata.special[i].draw(self.coors)
            if inputdata.description.has_key('DrawFunctionFirst') and inputdata.description['DrawFunctionFirst']=='1':
                for i in inputdata.functions.keys():
                    out += inputdata.functions[i].draw(self.coors)
                for i in inputdata.description['DrawOnly']:
                    inputdata.histos[i].description['ErrorBands']='0'
                    out += inputdata.histos[i].draw(self.coors)
            else:
              
                print "----------------------------------"
                if inputdata.description.has_key('MainPlotSelection'):
                  s=inputdata.description['MainPlotSelection']
                  selection=ast.literal_eval(s)
                  count=0
                  for i in inputdata.description['DrawOnly']:
                    count+=1
                    print "---------->",count,selection["Selection"]
                    if count in selection["Selection"]:
                       out += inputdata.histos[i].draw(self.coors)
                else:
                  for i in inputdata.description['DrawOnly']:
                    inputdata.histos[i].description['ErrorBands']='0'
                    out += inputdata.histos[i].draw(self.coors)
                for i in inputdata.functions.keys():
                    out += inputdata.functions[i].draw(self.coors)
        else:
            if inputdata.description.has_key('DrawFunctionFirst') and inputdata.description['DrawFunctionFirst']=='1':
                for i in inputdata.functions.keys():
                    out += inputdata.functions[i].draw(self.coors)
                if inputdata.description.has_key('MainPlotSelection'):
                  s=inputdata.description['MainPlotSelection']
                  selection=ast.literal_eval(s)
                  count=0
                  for i in inputdata.description['DrawOnly']:
                    count+=1
                    if count in selection["Selection"]:
                      print "a---------->",count ,selection["Selection"]
                      out += inputdata.histos[i].draw(self.coors)
                else:
                  for i in inputdata.description['DrawOnly']:
                    inputdata.histos[i].description['ErrorBands']='0'
                    out += inputdata.histos[i].draw(self.coors)
            else:
                if inputdata.description.has_key('MainPlotSelection'):
                  s=inputdata.description['MainPlotSelection']
                  selection=ast.literal_eval(s)
                  count=0
                  for i in inputdata.description['DrawOnly']:
                    count+=1
                    if count in selection["Selection"]:
                      print "b---------->",count ,selection["Selection"]
                      print out
                      out += inputdata.histos[i].draw(self.coors)
                      print "::::::::::::::::::::::::"
                      print out
                else:
                  for i in inputdata.description['DrawOnly']:
                    inputdata.histos[i].description['ErrorBands']='0'
                    out += inputdata.histos[i].draw(self.coors)
                for i in inputdata.functions.keys():
                    out += inputdata.functions[i].draw(self.coors)
            for i in inputdata.special.keys():
                out += inputdata.special[i].draw(self.coors)
        if inputdata.description.has_key('Legend') and inputdata.description['Legend']=='1':
            legend = Legend(inputdata.description,inputdata.histos,inputdata.functions)
            out += legend.draw(-2,inputdata)
        if inputdata.description['is2dim']:
            colorscale = Colorscale(inputdata.description,self.coors)
            out += colorscale.draw()
        frame = Frame()
        out += frame.draw(inputdata)

        if inputdata.description.has_key('XMajorTickMarks') and inputdata.description['XMajorTickMarks']!='':
            xcustommajortickmarks=int(inputdata.description['XMajorTickMarks'])
        else:
            xcustommajortickmarks=-1
        if inputdata.description.has_key('XMinorTickMarks') and inputdata.description['XMinorTickMarks']!='':
            xcustomminortickmarks=int(inputdata.description['XMinorTickMarks'])
        else:
            xcustomminortickmarks=-1
        xcustommajorticks=[]
        xcustomminorticks=[]
        # # TODO: remove XCustomTicks after 2011-12-31:
        # if inputdata.description.has_key('XCustomTicks') and inputdata.description['XCustomTicks']!='':
        #     logging.warning('Warning: XCustomTicks is deprecated. Use XCustomMajorTicks instead.')
        #     inputdata.description['XCustomMajorTicks']=inputdata.description['XCustomTicks']
        if inputdata.description.has_key('XCustomMajorTicks') and inputdata.description['XCustomMajorTicks']!='':
            # TODO: Would be nice to have less invisible separation of the custom ticks than split on tabs
            FOO=inputdata.description['XCustomMajorTicks'].strip().split('\t')
            if not len(FOO) % 2:
                for i in range(0,len(FOO),2):
                    xcustommajorticks.append({'Value': float(FOO[i]), 'Label': FOO[i+1]})
        if inputdata.description.has_key('XCustomMinorTicks') and inputdata.description['XCustomMinorTicks']!='':
            # TODO: Would be nice to have less invisible separation of the custom ticks than split on tabs
            FOO=inputdata.description['XCustomMinorTicks'].strip().split('\t')
            for i in range(len(FOO)):
                xcustomminorticks.append({'Value': float(FOO[i])})
        xticks = XTicks(inputdata.description, self.coors)
        if (inputdata.description.has_key('RatioPlot') and inputdata.description['RatioPlot']!='0') or (inputdata.description.has_key('PlotXTickLabels') and inputdata.description['PlotXTickLabels']=='0'):
            drawxlabels=False
        else:
            drawxlabels=True
        out += xticks.draw(custommajortickmarks=xcustommajortickmarks,\
                           customminortickmarks=xcustomminortickmarks,\
                           custommajorticks=xcustommajorticks,\
                           customminorticks=xcustomminorticks,\
                           drawlabels=drawxlabels)

        if inputdata.description.has_key('YMajorTickMarks') and inputdata.description['YMajorTickMarks']!='':
            ycustommajortickmarks=int(inputdata.description['YMajorTickMarks'])
        else:
            ycustommajortickmarks=-1
        if inputdata.description.has_key('YMinorTickMarks') and inputdata.description['YMinorTickMarks']!='':
            ycustomminortickmarks=int(inputdata.description['YMinorTickMarks'])
        else:
            ycustomminortickmarks=-1
        ycustommajorticks=[]
        ycustomminorticks=[]
        # # TODO: remove YCustomTicks after 2011-12-31:
        # if inputdata.description.has_key('YCustomTicks') and inputdata.description['YCustomTicks']!='':
        #     logging.warning('Warning: YCustomTicks is deprecated. Use YCustomMajorTicks instead.')
        #     inputdata.description['YCustomMajorTicks']=inputdata.description['YCustomTicks']
        if inputdata.description.has_key('YCustomMajorTicks') and inputdata.description['YCustomMajorTicks']!='':
            # TODO: Would be nice to have less invisible separation of the custom ticks than split on tabs
            FOO=inputdata.description['YCustomMajorTicks'].strip().split('\t')
            if not len(FOO)%2:
                for i in range(0,len(FOO),2):
                    ycustommajorticks.append({'Value': float(FOO[i]), 'Label': FOO[i+1]})
        if inputdata.description.has_key('YCustomMinorTicks') and inputdata.description['YCustomMinorTicks']!='':
            # TODO: Would be nice to have less invisible separation of the custom ticks than split on tabs
            FOO=inputdata.description['YCustomMinorTicks'].strip().split('\t')
            for i in range(len(FOO)):
                ycustomminorticks.append({'Value': float(FOO[i])})
        yticks = YTicks(inputdata.description, self.coors)
        if (inputdata.description.has_key('PlotYTickLabels') and inputdata.description['PlotYTickLabels']=='0'):
            drawylabels=False
        else:
            drawylabels=True
        out += yticks.draw(custommajortickmarks=ycustommajortickmarks,\
                           customminortickmarks=ycustomminortickmarks,\
                           custommajorticks=ycustommajorticks,\
                           customminorticks=ycustomminorticks,
                           drawlabels=drawylabels)

        labels = Labels(inputdata.description)
        if inputdata.description.has_key('RatioPlot') and inputdata.description['RatioPlot']!='0':
            out += labels.draw(['Title','YLabel'])
        else:
            if not inputdata.description['is2dim']:
                out += labels.draw(['Title','XLabel','YLabel'])
            else:
                out += labels.draw(['Title','XLabel','YLabel','ZLabel'])
        return out

    def calculate_gof(self, inputdata):
        refdata = inputdata.description.get('GofReference')
        if refdata is None:
            refdata = inputdata.description.get('RatioPlotReference')

        if refdata is None:
            inputdata.description['GofLegend'] = '0'
            inputdata.description['GofFrame'] = ''
            return

        def pickcolor(gof):
            color=None
            colordefs = {}
            for i in inputdata.description.setdefault('GofFrameColor', '0:green 3:yellow 6:red!70').strip().split():
                foo = i.split(':')
                if len(foo)!=2: continue
                colordefs[float(foo[0])] = foo[1]
            for i in sorted(colordefs.keys()):
                if gof>=i:
                    color=colordefs[i]
            return color

        inputdata.description.setdefault('GofLegend','0')
        inputdata.description.setdefault('GofFrame','')
        inputdata.description.setdefault('FrameColor',None)

        for i in inputdata.description['DrawOnly']:
            if i==refdata: continue
            if inputdata.description['GofLegend']!='1' and i!=inputdata.description['GofFrame']: continue

            if inputdata.description.has_key('GofType') and inputdata.description['GofType']!='chi2':
                return
            gof = inputdata.histos[i].getChi2(inputdata.histos[refdata])
            if i==inputdata.description['GofFrame'] and inputdata.description['FrameColor']==None:
                inputdata.description['FrameColor']=pickcolor(gof)
            if inputdata.histos[i].description.setdefault('Title', '')!='':
                inputdata.histos[i].description['Title'] += ', '
            inputdata.histos[i].description['Title'] += '$\\chi^2/n={}$%1.2f' %gof



class TaylorPlot(Plot):
    def __init__(self, inputdata):
        self.refdata = inputdata.description['TaylorPlotReference']
        self.calculate_taylorcoordinates(inputdata)

    def calculate_taylorcoordinates(self,inputdata):
        foo=inputdata.description['DrawOnly'].pop(inputdata.description['DrawOnly'].index(self.refdata))
        inputdata.description['DrawOnly'].append(foo)
        for i in inputdata.description['DrawOnly']:
            print i
            print 'meanbinval  = ', inputdata.histos[i].getMeanBinValue()
            print 'sigmabinval = ', inputdata.histos[i].getSigmaBinValue()
            print 'chi2/nbins  = ', inputdata.histos[i].getChi2(inputdata.histos[self.refdata])
            print 'correlation = ', inputdata.histos[i].getCorrelation(inputdata.histos[self.refdata])
            print 'distance    = ', inputdata.histos[i].getRMSdistance(inputdata.histos[self.refdata])



class RatioPlot(Plot):
    def __init__(self, inputdata,number):

        if inputdata.description.has_key('RatioPlots'):
            s=inputdata.description['RatioPlots'].split(";")[number]
            selection=ast.literal_eval(s)
            #print selection["RatioPlotYLabel"]
            #print selection["Selection"]
            nn=selection["Selection"][0]-1
            #print nn
            #print len(inputdata.description['DrawOnly'])
            count=0
            for i in inputdata.description['DrawOnly']:
                print count,": ",i
                count+=1
                pass
            self.refdata =  inputdata.description['DrawOnly'][nn]
        else:
            self.refdata = inputdata.description['RatioPlotReference']
            pass
        
        add=0
        if number!=0:
          add=1
        self.yoffset = inputdata.description['PlotSizeY'] + inputdata.description['RatioPlotSizeY']*(1+number+add)
        inputdata.description['RatioPlotStage'] = True
        inputdata.description['PlotSizeY'] = inputdata.description['RatioPlotSizeY']
        inputdata.description['LogY'] = False
        if inputdata.description.has_key('RatioPlotMode') and inputdata.description['RatioPlotMode']=='deviation':
            inputdata.description['YLabel']='$(\\text{MC}-\\text{data})$'
            inputdata.description['YMin']=-3.5
            inputdata.description['YMax']=3.5
        elif inputdata.description.has_key('RatioPlotMode') and inputdata.description['RatioPlotMode']=='datamc':
            inputdata.description['YLabel']='Data/MC'
            inputdata.description['YMin']=0.5
            inputdata.description['YMax']=1.5
        else:
            inputdata.description['YLabel']='MC/Data'
            inputdata.description['YMin']=0.5
            inputdata.description['YMax']=1.5
        if inputdata.description.has_key('RatioPlotYLabel'):
            inputdata.description['YLabel']=inputdata.description['RatioPlotYLabel']
        inputdata.description['YLabel']='\\rput(-%s,0){%s}'%(0.5*inputdata.description['PlotSizeY']/inputdata.description['PlotSizeX'],inputdata.description['YLabel'])
        
        if inputdata.description.has_key('RatioPlots'):
           s=inputdata.description['RatioPlots'].split(";")[number]
           selection=ast.literal_eval(s)
           print selection["RatioPlotYLabel"]
           inputdata.description['YLabel']=selection["RatioPlotYLabel"]
           inputdata.histos[self.refdata].description['ErrorBands']='1'
        
        
        if inputdata.description.has_key('RatioPlotYMin'):
            inputdata.description['YMin']=inputdata.description['RatioPlotYMin']
        if inputdata.description.has_key('RatioPlotYMax'):
            inputdata.description['YMax']=inputdata.description['RatioPlotYMax']
        if not inputdata.description.has_key('RatioPlotErrorBandColor'):
            inputdata.description['RatioPlotErrorBandColor']='yellow'
        if not inputdata.description.has_key('RatioPlotSameStyle') or inputdata.description['RatioPlotSameStyle']=='0':
            inputdata.histos[self.refdata].description['ErrorBandColor']=inputdata.description['RatioPlotErrorBandColor']
            inputdata.histos[self.refdata].description['ErrorBands']='0'
            inputdata.histos[self.refdata].description['ErrorBars']='0'
            inputdata.histos[self.refdata].description['LineStyle']='solid'
            # Comment this line to set ratio plots reference lines to use same color
            # as lines in main plot
            inputdata.histos[self.refdata].description['LineColor']='black'
            inputdata.histos[self.refdata].description['LineWidth']='0.3pt'
            inputdata.histos[self.refdata].description['PolyMarker']=''
            inputdata.histos[self.refdata].description['ConnectGaps']='1'
        self.calculate_ratios(inputdata,number)
        self.set_borders(inputdata)
        self.coors = Coordinates(inputdata)

    def draw(self, inputdata,xlabel,number):
        out = ""
        out += ('\n%\n% RatioPlot\n%\n')
        out += ('\\psset{yunit=%scm}\n' %(self.yoffset))
        out += ('\\rput(0,-1){%\n')
        out += ('\\psset{yunit=%scm}\n' %(inputdata.description['PlotSizeY']))
        out += self._draw(inputdata,xlabel,number)
        out += ('}\n')
        return out

    def calculate_ratios(self,inputdata,number):
        tindex=inputdata.description['DrawOnly'].index(self.refdata)
        foo=inputdata.description['DrawOnly'].pop(tindex)
        moved=False
        if inputdata.histos[self.refdata].description.has_key('ErrorBands') and inputdata.histos[self.refdata].description['ErrorBands']=='1':
            inputdata.description['DrawOnly'].insert(0,foo)
            moved=True
        else:
            inputdata.description['DrawOnly'].append(foo)

        for i in inputdata.description['DrawOnly']:
            if i!=self.refdata:
                if inputdata.description.has_key('RatioPlotMode') and inputdata.description['RatioPlotMode']=='deviation':
                    inputdata.histos[i].deviation(inputdata.histos[self.refdata])
                elif inputdata.description.has_key('RatioPlotMode') and inputdata.description['RatioPlotMode']=='datamc':
                    inputdata.histos[i].dividereverse(inputdata.histos[self.refdata])
                    inputdata.histos[i].description['ErrorBars']='1'
                else:
                    inputdata.histos[i].divide(inputdata.histos[self.refdata])
                    
        if inputdata.description.has_key('RatioPlotMode') and inputdata.description['RatioPlotMode']=='deviation':
            inputdata.histos[self.refdata].deviation(inputdata.histos[self.refdata])
        elif inputdata.description.has_key('RatioPlotMode') and inputdata.description['RatioPlotMode']=='datamc':
            inputdata.histos[self.refdata].dividereverse(inputdata.histos[self.refdata])
        else:
            inputdata.histos[self.refdata].divide(inputdata.histos[self.refdata])

        if moved:
            inputdata.description['DrawOnly'].insert(tindex, inputdata.description['DrawOnly'].pop(0) )
        else:
            inputdata.description['DrawOnly'].insert(tindex, inputdata.description['DrawOnly'].pop() )
            
            

    def _draw(self, inputdata,xlabel,number):
        out = ""
        s=inputdata.description['RatioPlots'].split(";")[number]
        selection=ast.literal_eval(s)
        print selection
        count=0
        for i in inputdata.description['DrawOnly']:
          count+=1
          if count in selection["Selection"]:
            print count
            if inputdata.description.has_key('RatioPlotMode') and inputdata.description['RatioPlotMode']=='datamc':
                if i!=self.refdata:
                    inputdata.histos[i].description['ErrorBands']='0'
                    out += inputdata.histos[i].draw(self.coors)
                    
                else:
                    inputdata.histos[i].description['ErrorBands']='1'
                    out += inputdata.histos[i].draw(self.coors)
            else:
                if i!=self.refdata:
                    inputdata.histos[i].description['ErrorBands']='1'
                    out += inputdata.histos[i].draw(self.coors)
                    
                else:
                    inputdata.histos[i].description['ErrorBands']='1'
                    out += inputdata.histos[i].draw(self.coors)

        frame = Frame()
        out += frame.draw(inputdata)

        # TODO: so much duplication with MainPlot... yuck!
        if inputdata.description.has_key('XMajorTickMarks') and inputdata.description['XMajorTickMarks']!='':
            xcustommajortickmarks=int(inputdata.description['XMajorTickMarks'])
        else:
            xcustommajortickmarks=-1
        if inputdata.description.has_key('XMinorTickMarks') and inputdata.description['XMinorTickMarks']!='':
            xcustomminortickmarks=int(inputdata.description['XMinorTickMarks'])
        else:
            xcustomminortickmarks=-1
        xcustommajorticks=[]
        xcustomminorticks=[]
        # # TODO: remove XCustomTicks after 2011-12-31:
        # if inputdata.description.has_key('XCustomTicks') and inputdata.description['XCustomTicks']!='':
        #     logging.warning('Warning: XCustomTicks is deprecated. Use XCustomMajorTicks instead.')
        #     inputdata.description['XCustomMajorTicks']=inputdata.description['XCustomTicks']
        if inputdata.description.has_key('XCustomMajorTicks') and inputdata.description['XCustomMajorTicks']!='':
            # TODO: Would be nice to have less invisible separation of the custom ticks than split on tabs
            FOO=inputdata.description['XCustomMajorTicks'].strip().split('\t')
            if not len(FOO)%2:
                for i in range(0,len(FOO),2):
                    xcustommajorticks.append({'Value': float(FOO[i]), 'Label': FOO[i+1]})
        if inputdata.description.has_key('XCustomMinorTicks') and inputdata.description['XCustomMinorTicks']!='':
            # TODO: Would be nice to have less invisible separation of the custom ticks than split on tabs
            FOO=inputdata.description['XCustomMinorTicks'].strip().split('\t')
            for i in range(len(FOO)):
                xcustomminorticks.append({'Value': float(FOO[i])})
        xticks = XTicks(inputdata.description, self.coors)
        if inputdata.description.has_key('RatioPlotTickLabels') and inputdata.description['RatioPlotTickLabels']=='0':
            drawlabels=False
        else:
            drawlabels=True and xlabel
        out += xticks.draw(custommajortickmarks=xcustommajortickmarks,\
                           customminortickmarks=xcustomminortickmarks,\
                           custommajorticks=xcustommajorticks,\
                           customminorticks=xcustomminorticks,
                           drawlabels=drawlabels)

        if inputdata.description.has_key('YMajorTickMarks') and inputdata.description['YMajorTickMarks']!='':
            ycustommajortickmarks=int(inputdata.description['YMajorTickMarks'])
        else:
            ycustommajortickmarks=-1
        if inputdata.description.has_key('YMinorTickMarks') and inputdata.description['YMinorTickMarks']!='':
            ycustomminortickmarks=int(inputdata.description['YMinorTickMarks'])
        else:
            ycustomminortickmarks=-1
        ycustommajorticks=[]
        ycustomminorticks=[]
        # # TODO: remove YCustomTicks after 2011-12-31:
        # if inputdata.description.has_key('YCustomTicks') and inputdata.description['YCustomTicks']!='':
        #     logging.warning('Warning: YCustomTicks is deprecated. Use YCustomMajorTicks instead.')
        #     inputdata.description['YCustomMajorTicks']=inputdata.description['YCustomTicks']
        if inputdata.description.has_key('YCustomMajorTicks') and inputdata.description['YCustomMajorTicks']!='':
            # TODO: Would be nice to have less invisible separation of the custom ticks than split on tabs
            FOO=inputdata.description['YCustomMajorTicks'].strip().split('\t')
            if not len(FOO)%2:
                for i in range(0,len(FOO),2):
                    ycustommajorticks.append({'Value': float(FOO[i]), 'Label': FOO[i+1]})
        if inputdata.description.has_key('YCustomMinorTicks') and inputdata.description['YCustomMinorTicks']!='':
            # TODO: Would be nice to have less invisible separation of the custom ticks than split on tabs
            FOO=inputdata.description['YCustomMinorTicks'].strip().split('\t')
            for i in range(len(FOO)):
                ycustomminorticks.append({'Value': float(FOO[i])})
        yticks = YTicks(inputdata.description, self.coors,True)
        out += yticks.draw(custommajortickmarks=ycustommajortickmarks,\
                           customminortickmarks=ycustomminortickmarks,\
                           custommajorticks=ycustommajorticks,\
                           customminorticks=ycustomminorticks)

        if inputdata.description.has_key('RatioPlots'):
          legend = Legend(inputdata.description,inputdata.histos,inputdata.functions,False)
          out += legend.draw(number,inputdata)

        if inputdata.description.has_key('MainPlot') and inputdata.description['MainPlot']=='0':
            if inputdata.description.has_key('Legend') and inputdata.description['Legend']=='1':
                legend = Legend(inputdata.description,inputdata.histos,inputdata.functions)
                out += legend.draw(-1,inputdata)

        labels = Labels(inputdata.description)
        if inputdata.description.has_key('MainPlot') and inputdata.description['MainPlot']=='0':
            out += labels.draw(['Title','XLabel','YLabel'])
        else:
          if (int(number+1)==int(inputdata.description['RatioPlot'])):
        
            out += labels.draw(['XLabel','YLabel'])
          else:
            print "8783546756878675654465 ", number,inputdata.description['RatioPlot']
            out += labels.draw(['','YLabel'])
            
        return out



class Legend(object):
    def __init__(self, description, histos, functions,correctpos=True):
        self.histos = histos
        self.functions = functions
        self.description = description
        self.correctpos=correctpos

    def draw(self,number,inputdata):
        out = ""
        out += '\n%\n% Legend\n%\n'
        if self.correctpos:
           out += '\\rput[tr](%s,%s){%%\n' % (self.getLegendXPos(), self.getLegendYPos())
        else:
           out += '\\rput[tr](%s,%s){%%\n' % (0.,0.)
        ypos = -0.05*6/self.description['PlotSizeY']

        legendordermap = {}
        legendlist = self.description['DrawOnly']+self.functions.keys()
        
        
        if number == -2 and inputdata.description.has_key('MainPlotSelection'):
          s=inputdata.description['MainPlotSelection']
          selection=ast.literal_eval(s)
          count=0
          legendlisttmp=legendlist
          legendlist=[]
          for i in legendlisttmp:
            count+=1
            if count in selection["Selection"]:
              legendlist.append(i)
        
        if inputdata.description.has_key('RatioPlots') and number != -1 and number != -2:
          s=inputdata.description['RatioPlots'].split(";")[number]
          selection=ast.literal_eval(s)
          count=0
          legendlisttmp=legendlist
          legendlist=[]
          for i in legendlisttmp:
            count+=1
            if count in selection["Selection"]: ## and count !=1:
              self.histos[i].description['ErrorBands']=True
              legendlist.append(i)
              
        
        
        if self.description.has_key('LegendOnly'):
            legendlist = []
            for legend in self.description['LegendOnly'].strip().split():
                if legend in self.histos.keys() or legend in self.functions.keys():
                    legendlist.append(legend)
        for legend in legendlist:
            order = 0
            if self.histos.has_key(legend) and self.histos[legend].description.has_key('LegendOrder'):
                order = int(self.histos[legend].description['LegendOrder'])
            if self.functions.has_key(legend) and self.functions[legend].description.has_key('LegendOrder'):
                order = int(self.functions[legend].description['LegendOrder'])
            if not order in legendordermap:
                legendordermap[order] = []
            legendordermap[order].append(legend)
        foo=[]
        for i in sorted(legendordermap.keys()):
            foo.extend(legendordermap[i])

        rel_xpos_sign = 1.0
        if self.getLegendAlign()=='r':
            rel_xpos_sign = -1.0
        xpos1 = -0.10*rel_xpos_sign
        xpos2 = -0.02*rel_xpos_sign
        nr=0
        for i in foo:
            nr+=1
            if self.histos.has_key(i):
                drawobject=self.histos[i]
            elif self.functions.has_key(i):
                drawobject=self.functions[i]
            else:
                continue
            title = drawobject.getTitle()
            drawobject.description['ErrorBands']=False
            if title == '':
                continue
            else:
                if self.correctpos:
                  out += ('\\rput[B%s](%s,%s){%s}\n' %(self.getLegendAlign(),rel_xpos_sign*0.1,ypos,title))
                  out += ('\\rput[B%s](%s,%s){%s\n' %(self.getLegendAlign(),rel_xpos_sign*0.1,ypos,'%'))
                else:
                  if nr==1:
                    out += ('\\rput[B%s](%s,%s){%s}\n' %(self.getLegendAlign(),0.15,0.85,title))
                    out += ('\\rput[B%s](%s,%s){%s\n' %(self.getLegendAlign(),0.15,0.85,'%'))
                  if nr==2:
                    out += ('\\rput[B%s](%s,%s){%s}\n' %(self.getLegendAlign(),0.65,0.85,title))
                    out += ('\\rput[B%s](%s,%s){%s\n' %(self.getLegendAlign(),0.65,0.85,'%'))
                  if nr==3:
                    out += ('\\rput[B%s](%s,%s){%s}\n' %(self.getLegendAlign(),0.15,0.15,title))
                    out += ('\\rput[B%s](%s,%s){%s\n' %(self.getLegendAlign(),0.15,0.15,'%'))
                  if nr==4:
                    out += ('\\rput[B%s](%s,%s){%s}\n' %(self.getLegendAlign(),0.65,0.15,title))
                    out += ('\\rput[B%s](%s,%s){%s\n' %(self.getLegendAlign(),0.65,0.15,'%'))
                  if nr>4:
                    print "to many ratio lines"


                if drawobject.getErrorBands():
                  #print i
                  # print "xxx",drawobject.getErrorBandOpacity(),drawobject.getErrorBandColor(),xpos1, xpos2
                    out += ('\\psframe[linewidth=7pt,linestyle=none,fillstyle=%s,hatchcolor=%s,fillcolor=%s,opacity=%s]' %(drawobject.getErrorBandStyle(),drawobject.getErrorBandColor(),drawobject.getErrorBandColor(),drawobject.getErrorBandOpacity()))
                    out += ('(%s, 0.033)(%s, 0.001)\n' %(xpos1, xpos2))
                out += ('\\psline[linestyle=' + drawobject.getLineStyle() \
                            + ', linecolor=' + drawobject.getLineColor() \
                            + ', linewidth=' + drawobject.getLineWidth() \
                            + ', strokeopacity=' + drawobject.getLineOpacity() \
                            + ', opacity=' + drawobject.getFillOpacity())
                if drawobject.getLineDash()!='':
                    out += (', dash=' + drawobject.getLineDash())
                if drawobject.getFillStyle()!='none':
                    out += (', fillstyle=' + drawobject.getFillStyle() \
                                + ', fillcolor='  + drawobject.getFillColor() \
                                + ', hatchcolor=' + drawobject.getHatchColor() \
                                + ']{C-C}(%s, 0.030)(%s, 0.030)(%s, 0.004)(%s, 0.004)(%s, 0.030)\n' \
                                %(xpos1, xpos2, xpos2, xpos1, xpos1))
                else:
                    out += ('](%s, 0.016)(%s, 0.016)\n' %(xpos1, xpos2))
                if drawobject.getPolyMarker() != '':
                    out += ('  \\psdot[dotstyle=' + drawobject.getPolyMarker() \
                                + ', dotsize='    + drawobject.getDotSize()   \
                                + ', dotscale='   + drawobject.getDotScale()  \
                                + ', linecolor='  + drawobject.getLineColor() \
                                + ', linewidth='  + drawobject.getLineWidth() \
                                + ', linestyle='  + drawobject.getLineStyle() \
                                + ', fillstyle='  + drawobject.getFillStyle() \
                                + ', fillcolor='  + drawobject.getFillColor() \
                                + ', strokeopacity=' + drawobject.getLineOpacity() \
                                + ', opacity=' + drawobject.getFillOpacity() \
                                + ', hatchcolor=' + drawobject.getHatchColor())
                    if drawobject.getFillStyle()!='none':
                        out += ('](%s, 0.028)\n' % (rel_xpos_sign*-0.06))
                    else:
                        out += ('](%s, 0.016)\n' % (rel_xpos_sign*-0.06))
                out += ('}\n')
                ypos -= 0.075*6/self.description['PlotSizeY']
        if self.description.has_key('CustomLegend'):
            for i in self.description['CustomLegend'].strip().split('\\\\'):
                out += ('\\rput[B%s](%s,%s){%s}\n' %(self.getLegendAlign(),rel_xpos_sign*0.1,ypos,i))
                ypos -= 0.075*6/self.description['PlotSizeY']
        out += ('}\n')
        return out

    def getLegendXPos(self):
        if self.description.has_key('LegendXPos'):
            return self.description['LegendXPos']
        else:
            if self.getLegendAlign()=='r':
                return '0.95'
            else:
                return '0.53'

    def getLegendYPos(self):
        if self.description.has_key('LegendYPos'):
            return self.description['LegendYPos']
        else:
            return '0.93'

    def getLegendAlign(self):
        if self.description.has_key('LegendAlign'):
            return self.description['LegendAlign']
        else:
            return 'l'


class Colorscale(object):
    def __init__(self, description, coors):
        self.description = description
        self.coors = coors
    def draw(self):
        out = ''
        out += '\n%\n% Colorscale\n%\n'
        out += '\\rput(1,0){\n'
        out += '  \\psset{xunit=4mm}\n'
        out += '  \\rput(0.5,0){\n'
        out += '    \\psset{yunit=0.0076923, linestyle=none, fillstyle=solid}\n'
        out += '    \\multido{\\ic=0+1,\\id=1+1}{130}{\n'
        out += '      \\psframe[fillcolor={gradientcolors!![\\ic]},dimen=inner,linewidth=0.1pt](0, \\ic)(1, \\id)\n'
        out += '    }\n'
        out += '  }\n'
        out += '  \\rput(0.5,0){\n'
        out += '    \\psframe[linewidth=0.3pt,dimen=middle](0,0)(1,1)\n'

        # TODO: so much parsing duplication with MainPlot... yuck!
        if self.description.has_key('ZMajorTickMarks') and self.description['ZMajorTickMarks']!='':
            zcustommajortickmarks=int(self.description['ZMajorTickMarks'])
        else:
            zcustommajortickmarks=-1
        if self.description.has_key('ZMinorTickMarks') and self.description['ZMinorTickMarks']!='':
            zcustomminortickmarks=int(self.description['ZMinorTickMarks'])
        else:
            zcustomminortickmarks=-1
        zcustommajorticks=[]
        zcustomminorticks=[]
        # # TODO: remove ZCustomTicks after 2011-12-31:
        # if self.description.has_key('ZCustomTicks') and self.description['ZCustomTicks']!='':
        #     logging.warning('Warning: ZCustomTicks is deprecated. Use ZCustomMajorTicks instead.')
        #     self.description['ZCustomMajorTicks']=self.description['ZCustomTicks']
        if self.description.has_key('ZCustomMajorTicks') and self.description['ZCustomMajorTicks']!='':
            # TODO: Would be nice to have less invisible separation of the custom ticks than split on tabs
            FOO=self.description['ZCustomMajorTicks'].strip().split('\t')
            if not len(FOO)%2:
                for i in range(0,len(FOO),2):
                    zcustommajorticks.append({'Value': float(FOO[i]), 'Label': FOO[i+1]})
        if self.description.has_key('ZCustomMinorTicks') and self.description['ZCustomMinorTicks']!='':
            # TODO: Would be nice to have less invisible separation of the custom ticks than split on tabs
            FOO=self.description['ZCustomMinorTicks'].strip().split('\t')
            for i in range(len(FOO)):
                zcustomminorticks.append({'Value': float(FOO[i])})
        if (self.description.has_key('PlotZTickLabels') and self.description['PlotZTickLabels']=='0'):
            drawzlabels=False
        else:
            drawzlabels=True
        zticks = ZTicks(self.description, self.coors)
        out += zticks.draw(custommajortickmarks=zcustommajortickmarks,\
                           customminortickmarks=zcustomminortickmarks,\
                           custommajorticks=zcustommajorticks,\
                           customminorticks=zcustomminorticks,
                           drawlabels=drawzlabels)
        out += '  }\n'
        out += '}\n'
        return out



class Labels(object):
    def __init__(self, description):
        self.description = description

    def draw(self, axis=[]):
        out = ""
        out += ('\n%\n% Labels\n%\n')
        if self.description.has_key('Title') and (axis.count('Title') or axis==[]):
            out += ('\\rput(0,1){\\rput[lB](0, 1.7\\labelsep){\\normalsize '+self.description['Title']+'}}\n')
        if self.description.has_key('XLabel') and (axis.count('XLabel') or axis==[]):
            xlabelsep=4.7
            if self.description.has_key('XLabelSep'):
                xlabelsep=float(self.description['XLabelSep'])
            out += ('\\rput(1,0){\\rput[rB](0,-%4.3f\\labelsep){\\normalsize '%(xlabelsep) +self.description['XLabel']+'}}\n')
        if self.description.has_key('YLabel') and (axis.count('YLabel') or axis==[]):
            ylabelsep=6.5
            if self.description.has_key('YLabelSep'):
                ylabelsep=float(self.description['YLabelSep'])
            out += ('\\rput(0,1){\\rput[rB]{90}(-%4.3f\\labelsep,0){\\normalsize '%(ylabelsep) +self.description['YLabel']+'}}\n')
        if self.description.has_key('ZLabel') and (axis.count('ZLabel') or axis==[]):
            zlabelsep=5.3
            if self.description.has_key('ZLabelSep'):
                zlabelsep=float(self.description['ZLabelSep'])
            out += ('\\rput(1,1){\\rput(%4.3f\\labelsep,0){\\psset{xunit=4mm}\\rput[lB]{270}(1.5,0){\\normalsize '%(zlabelsep) +self.description['ZLabel']+'}}}\n')
        return out



class Special(object):
    def __init__(self, f):
        self.description = {}
        self.data = []
        self.read_input(f)

    def read_input(self, f):
        for line in f:
            if is_end_marker(line, 'SPECIAL'):
                break
            elif is_comment(line):
                continue
            else:
                self.data.append(line)

    def draw(self,coors):
        out = ""
        out += ('\n%\n% Special\n%\n')
        import re
        regex = re.compile(r'^(.*?)(\\physics[xy]?coor)\(\s?([0-9\.eE+-]+)\s?,\s?([0-9\.eE+-]+)\s?\)(.*)')
        # TODO: More precise number string matching, something like this:
        # num = r"-?[0-9]*(?:\.[0-9]*)(?:[eE][+-]?\d+]"
        # regex = re.compile(r'^(.*?)(\\physics[xy]?coor)\(\s?(' + num + ')\s?,\s?(' + num + ')\s?\)(.*)')
        for i in xrange(len(self.data)):
            while regex.search(self.data[i]):
                match = regex.search(self.data[i])
                xcoor, ycoor = float(match.group(3)), float(match.group(4))
                if match.group(2)[1:] in ["physicscoor", "physicsxcoor"]:
                    xcoor = coors.phys2frameX(xcoor)
                if match.group(2)[1:] in ["physicscoor", "physicsycoor"]:
                    ycoor = coors.phys2frameY(ycoor)
                line = "%s(%f, %f)%s" % (match.group(1), xcoor, ycoor, match.group(5))
                self.data[i] = line
            out += self.data[i]+'\n'
        return out



class DrawableObject(object):
    def __init__(self, f):
        pass

    def getTitle(self):
        if self.description.has_key('Title'):
            return self.description['Title']
        else:
            return ''

    def getLineStyle(self):
        if self.description.has_key('LineStyle'):
            ## I normally like there to be "only one way to do it", but providing
            ## this dashdotted/dotdashed synonym just seems humane ;-)
            if self.description['LineStyle'] in ('dashdotted', 'dotdashed'):
                self.description['LineStyle']='dashed'
                self.description['LineDash']='3pt 3pt .8pt 3pt'
            return self.description['LineStyle']
        else:
            return 'solid'

    def getLineDash(self):
        if self.description.has_key('LineDash'):
            # Check if LineStyle=='dashdotted' before returning something
            self.getLineStyle()
            return self.description['LineDash']
        else:
            return ''

    def getLineWidth(self):
        if self.description.has_key('LineWidth'):
            return self.description['LineWidth']
        else:
            return '0.8pt'

    def getLineColor(self):
        if self.description.has_key('LineColor'):
            return self.description['LineColor']
        else:
            return 'black'

    def getLineOpacity(self):
        if self.description.has_key('LineOpacity'):
            return self.description['LineOpacity']
        else:
            return '1.0'

    def getFillColor(self):
        if self.description.has_key('FillColor'):
            return self.description['FillColor']
        else:
            return 'white'

    def getFillOpacity(self):
        if self.description.has_key('FillOpacity'):
            return self.description['FillOpacity']
        else:
            return '1.0'

    def getHatchColor(self):
        if self.description.has_key('HatchColor'):
            return self.description['HatchColor']
        else:
            return 'black'

    def getFillStyle(self):
        if self.description.has_key('FillStyle'):
            return self.description['FillStyle']
        else:
            return 'none'

    def getPolyMarker(self):
        if self.description.has_key('PolyMarker'):
            return self.description['PolyMarker']
        else:
            return ''

    def getDotSize(self):
        if self.description.has_key('DotSize'):
            return self.description['DotSize']
        else:
            return '2pt 2'

    def getDotScale(self):
        if self.description.has_key('DotScale'):
            return self.description['DotScale']
        else:
            return '1'

    def getErrorBars(self):
        if self.description.has_key('ErrorBars'):
            return bool(int(self.description['ErrorBars']))
        else:
            return False

    def getErrorBands(self):
        if self.description.has_key('ErrorBands'):
            return bool(int(self.description['ErrorBands']))
        else:
            return False

    def getErrorBandColor(self):
        if self.description.has_key('ErrorBandColor'):
            return self.description['ErrorBandColor']
        else:
            return 'yellow'

    def getErrorBandStyle(self):
        if self.description.has_key('ErrorBandStyle'):
          return self.description['ErrorBandStyle']
        else:
          return 'solid'


    def getErrorBandOpacity(self):
        if self.description.has_key('ErrorBandOpacity'):
            return self.description['ErrorBandOpacity']
        else:
            return '1.0'

    def getSmoothLine(self):
        if self.description.has_key('SmoothLine'):
            return bool(int(self.description['SmoothLine']))
        else:
            return False

    def startclip(self):
        return '\\psclip{\\psframe[linewidth=0, linestyle=none](0,0)(1,1)}\n'

    def stopclip(self):
        return '\\endpsclip\n'

    def startpsset(self):
        out = ""
        out += ('\\psset{linecolor='+self.getLineColor()+'}\n')
        out += ('\\psset{linewidth='+self.getLineWidth()+'}\n')
        out += ('\\psset{linestyle='+self.getLineStyle()+'}\n')
        out += ('\\psset{fillstyle='+self.getFillStyle()+'}\n')
        out += ('\\psset{fillcolor='+self.getFillColor()+'}\n')
        out += ('\\psset{hatchcolor='+self.getHatchColor()+'}\n')
        out += ('\\psset{strokeopacity='+self.getLineOpacity()+'}\n')
        out += ('\\psset{opacity='+self.getFillOpacity()+'}\n')
        if self.getLineDash()!='':
            out += ('\\psset{dash='+self.getLineDash()+'}\n')
        return out

    def stoppsset(self):
        out = ""
        out += ('\\psset{linecolor=black}\n')
        out += ('\\psset{linewidth=0.8pt}\n')
        out += ('\\psset{linestyle=solid}\n')
        out += ('\\psset{fillstyle=none}\n')
        out += ('\\psset{fillcolor=white}\n')
        out += ('\\psset{hatchcolor=black}\n')
        out += ('\\psset{strokeopacity=1.0}\n')
        out += ('\\psset{opacity=1.0}\n')
        return out



class Function(DrawableObject):
    def __init__(self, f):
        self.description = {}
        self.read_input(f)

    def read_input(self, f):
        self.code='def plotfunction(x):\n'
        iscode=False
        for line in f:
            if is_end_marker(line, 'FUNCTION'):
                break
            elif is_comment(line):
                continue
            else:
                m = pat_property.match(line)
                if iscode:
                    self.code+='    '+line
                elif m:
                    prop, value = m.group(1,2)
                    if prop=='Code':
                        iscode=True
                    else:
                        self.description[prop] = value
        if not iscode:
            print '++++++++++ ERROR: No code in function'
        else:
            foo = compile(self.code, '<string>', 'exec')
            exec(foo)
            self.plotfunction = plotfunction


    def draw(self,coors):
        out = ""
        out += self.startclip()
        out += self.startpsset()
        xmin = coors.xmin()
        if self.description.has_key('XMin') and self.description['XMin']:
            xmin = float(self.description['XMin'])
        xmax=coors.xmax()
        if self.description.has_key('XMax') and self.description['XMax']:
            xmax=float(self.description['XMax'])
        # TODO: Space sample points logarithmically if LogX=1
        dx = (xmax-xmin)/500.
        x = xmin-dx
        out += '\\pscurve'
        if self.description.has_key('FillStyle') and self.description['FillStyle']!='none':
            out += '(%s,%s)\n' % (coors.strphys2frameX(xmin),coors.strphys2frameY(coors.ymin()))
        while x < (xmax+2*dx):
            y = self.plotfunction(x)
            out += ('(%s,%s)\n' % (coors.strphys2frameX(x), coors.strphys2frameY(y)))
            x += dx
        if self.description.has_key('FillStyle') and self.description['FillStyle']!='none':
            out += '(%s,%s)\n' % (coors.strphys2frameX(xmax),coors.strphys2frameY(coors.ymin()))
        out += self.stoppsset()
        out += self.stopclip()
        return out




class Histogram(DrawableObject):
    def __init__(self, f, p=None):
        self.description = {}
        self.is2dim = False
        self.data = []
        self.read_input_data(f)
        self.sigmabinvalue = None
        self.meanbinvalue = None
        self.path = p

    def read_input_data(self, f):
        for line in f:
            if is_end_marker(line, 'HISTOGRAM'):
                break
            elif is_comment(line):
                continue
            else:
                line = line.rstrip()
                m = pat_property.match(line)
                if m:
                    prop, value = m.group(1,2)
                    self.description[prop] = value
                else:
                    ## Detect symm errs
                    linearray = line.split()
                    if len(linearray) == 4:
                        self.data.append({'LowEdge': float(linearray[0]),
                                          'UpEdge':  float(linearray[1]),
                                          'Content': float(linearray[2]),
                                          'Error':   [float(linearray[3]),float(linearray[3])]})
                    ## Detect asymm errs
                    elif len(linearray) == 5:
                        self.data.append({'LowEdge': float(linearray[0]),
                                          'UpEdge':  float(linearray[1]),
                                          'Content': float(linearray[2]),
                                          'Error':   [float(linearray[3]),float(linearray[4])]})
                    ## Detect two-dimensionality
                    elif len(linearray) in [6,7]:
                        self.is2dim = True
                        # If asymm z error, use the max or average of +- error
                        err = float(linearray[5])
                        if len(linearray) == 7:
                            if self.description.get("ShowMaxZErr", 1):
                                err = max(err, float(linearray[6]))
                            else:
                                err = 0.5 * (err + float(linearray[6]))
                        self.data.append({'LowEdge': [float(linearray[0]), float(linearray[2])],
                                          'UpEdge':  [float(linearray[1]), float(linearray[3])],
                                          'Content': float(linearray[4]),
                                          'Error':   err})
                    ## Unknown histo format
                    else:
                        raise RuntimeError("Unknown HISTOGRAM data line format with %d entries" % len(linearray))


    def mangle_input(self):
        if (self.description.has_key('NormalizeToIntegral') and self.description['NormalizeToIntegral']=='1') or \
           (self.description.has_key('NormalizeToSum') and self.description['NormalizeToSum']=='1'):
            if (self.description.has_key('NormalizeToIntegral') and self.description['NormalizeToIntegral']=='1') and \
               (self.description.has_key('NormalizeToSum') and self.description['NormalizeToSum']=='1'):
                print 'Can\'t normalize to Integral and to Sum at the same time. Will normalize to the Sum.'
            foo = 0
            for i in range(len(self.data)):
                if self.description.has_key('NormalizeToSum') and self.description['NormalizeToSum']=='1':
                    foo += self.data[i]['Content']
                else:
                    foo += self.data[i]['Content']*(self.data[i]['UpEdge']-self.data[i]['LowEdge'])
            for i in range(len(self.data)):
                self.data[i]['Content']  /= foo
                self.data[i]['Error'][0] /= foo
                self.data[i]['Error'][1] /= foo
        if self.description.has_key('Scale') and self.description['Scale']!='':
            scale = float(self.description['Scale'])
            for i in range(len(self.data)):
                self.data[i]['Content']  *= scale
                self.data[i]['Error'][0] *= scale
                self.data[i]['Error'][1] *= scale
        if self.description.has_key('Rebin') and self.description['Rebin']!='':
            rebin=int(self.description['Rebin'])
            errortype = "stat"
            if self.description.has_key('ErrorType') and self.description['ErrorType']!='':
                errortype = self.description['ErrorType']
            newdata=[]
            if rebin>=2:
                for i in range(0,(len(self.data)/rebin)*rebin,rebin):
                    foo=0.
                    barl=0.
                    baru=0.
                    for j in range(rebin):
                        binwidth=self.data[i+j]['UpEdge']-self.data[i+j]['LowEdge']
                        foo +=self.data[i+j]['Content']*binwidth
                        if errortype=="stat":
                            barl+=(binwidth*self.data[i+j]['Error'][0])**2
                            baru+=(binwidth*self.data[i+j]['Error'][1])**2
                        elif errortype=="env":
                            barl+=(self.data[i+j]['Content']-self.data[i+j]['Error'][0])*binwidth
                            baru+=(self.data[i+j]['Content']+self.data[i+j]['Error'][1])*binwidth
                        else:
                            logging.error("Rebinning for ErrorType not implemented.")
                            sys.exit(1)
                    newbinwidth=self.data[i+rebin-1]['UpEdge']-self.data[i]['LowEdge']
                    newcentral=foo/newbinwidth
                    if errortype=="stat":
                        newerror=[sqrt(barl)/newbinwidth,sqrt(baru)/newbinwidth]
                    elif errortype=="env":
                        newerror=[(foo-barl)/newbinwidth,(baru-foo)/newbinwidth]
                    newdata.append({'LowEdge': self.data[i]['LowEdge'],
                                    'UpEdge':  self.data[i+rebin-1]['UpEdge'],
                                    'Content': newcentral,
                                    'Error':   newerror})
                self.data=newdata

    def add(self, name):
        if len(self.data) != len(name.data):
            print '+++ Error in Histogram.add() for %s: different numbers of bins' % self.path
        for i in range(len(self.data)):
            if fuzzyeq(self.data[i]['LowEdge'], name.data[i]['LowEdge']) and \
               fuzzyeq(self.data[i]['UpEdge'], name.data[i]['UpEdge']):
                self.data[i]['Content'] += name.data[i]['Content']
                self.data[i]['Error'][0] = sqrt(self.data[i]['Error'][0]**2 + name.data[i]['Error'][0]**2)
                self.data[i]['Error'][1] = sqrt(self.data[i]['Error'][1]**2 + name.data[i]['Error'][1]**2)
            else:
                print '+++ Error in Histogram.add() for %s: binning of histograms differs' % self.path

    def divide(self, name):
        if len(self.data) != len(name.data):
            print '+++ Error in Histogram.divide() for %s: different numbers of bins' % self.path
        for i in range(len(self.data)):
            if fuzzyeq(self.data[i]['LowEdge'], name.data[i]['LowEdge']) and \
               fuzzyeq(self.data[i]['UpEdge'], name.data[i]['UpEdge']):
                try:
                    self.data[i]['Error'][0] /= name.data[i]['Content']
                except ZeroDivisionError:
                    self.data[i]['Error'][0]=0.
                try:
                    self.data[i]['Error'][1] /= name.data[i]['Content']
                except ZeroDivisionError:
                    self.data[i]['Error'][1]=0.
                try:
                    self.data[i]['Content'] /= name.data[i]['Content']
                except ZeroDivisionError:
                    self.data[i]['Content']=1.
#                self.data[i]['Error'][0] = sqrt(self.data[i]['Error'][0]**2 + name.data[i]['Error'][0]**2)
#                self.data[i]['Error'][1] = sqrt(self.data[i]['Error'][1]**2 + name.data[i]['Error'][1]**2)
            else:
                print '+++ Error in Histogram.divide() for %s: binning of histograms differs' % self.path

    def dividereverse(self, name):
        if len(self.data) != len(name.data):
            print '+++ Error in Histogram.dividereverse() for %s: different numbers of bins' % self.path
        for i in range(len(self.data)):
            if fuzzyeq(self.data[i]['LowEdge'], name.data[i]['LowEdge']) and \
               fuzzyeq(self.data[i]['UpEdge'], name.data[i]['UpEdge']):
                try:
                    self.data[i]['Error'][0] = name.data[i]['Error'][0]/self.data[i]['Content']
                except ZeroDivisionError:
                    self.data[i]['Error'][0]=0.
                try:
                    self.data[i]['Error'][1] = name.data[i]['Error'][1]/self.data[i]['Content']
                except ZeroDivisionError:
                    self.data[i]['Error'][1]=0.
                try:
                    self.data[i]['Content'] = name.data[i]['Content']/self.data[i]['Content']
                except ZeroDivisionError:
                    self.data[i]['Content']=1.
            else:
                print '+++ Error in Histogram.dividereverse(): binning of histograms differs'

    def deviation(self, name):
        if len(self.data) != len(name.data):
            print '+++ Error in Histogram.deviation() for %s: different numbers of bins' % self.path
        for i in range(len(self.data)):
            if fuzzyeq(self.data[i]['LowEdge'], name.data[i]['LowEdge']) and \
               fuzzyeq(self.data[i]['UpEdge'], name.data[i]['UpEdge']):
                self.data[i]['Content'] -= name.data[i]['Content']
                try:
                    self.data[i]['Content'] /= 0.5*sqrt((name.data[i]['Error'][0] + name.data[i]['Error'][1])**2 + \
                                                        (self.data[i]['Error'][0] + self.data[i]['Error'][1])**2)
                except ZeroDivisionError:
                    self.data[i]['Content'] = 0.0
                try:
                    self.data[i]['Error'][0] /= name.data[i]['Error'][0]
                except ZeroDivisionError:
                    self.data[i]['Error'][0] = 0.0
                try:
                    self.data[i]['Error'][1] /= name.data[i]['Error'][1]
                except ZeroDivisionError:
                    self.data[i]['Error'][1] = 0.0
            else:
                print '+++ Error in Histogram.deviation() for %s: binning of histograms differs' % self.path

    def getChi2(self, name):
        chi2 = 0.
        for i in range(len(self.data)):
            if fuzzyeq(self.data[i]['LowEdge'], name.data[i]['LowEdge']) and \
               fuzzyeq(self.data[i]['UpEdge'], name.data[i]['UpEdge']):
                try:
                    chi2 += (self.data[i]['Content']-name.data[i]['Content'])**2/((0.5*self.data[i]['Error'][0]+0.5*self.data[i]['Error'][1])**2 + (0.5*name.data[i]['Error'][0]+0.5*name.data[i]['Error'][1])**2)
                except ZeroDivisionError:
                    pass
            else:
                print '+++ Error in Histogram.getChi2() for %s: binning of histograms differs' % self.path
        return chi2/len(self.data)

    def getSigmaBinValue(self):
        if self.sigmabinvalue==None:
            self.sigmabinvalue = 0.
            sumofweights = 0.
            for i in range(len(self.data)):
                if self.is2dim:
                    binwidth = abs( (self.data[i]['UpEdge'][0] - self.data[i]['LowEdge'][0])
                                   *(self.data[i]['UpEdge'][1] - self.data[i]['LowEdge'][1]))
                else:
                    binwidth = abs(self.data[i]['UpEdge'] - self.data[i]['LowEdge'])
                self.sigmabinvalue += binwidth*(self.data[i]['Content']-self.getMeanBinValue())**2
                sumofweights += binwidth
            self.sigmabinvalue = sqrt(self.sigmabinvalue/sumofweights)
        return self.sigmabinvalue

    def getMeanBinValue(self):
        if self.meanbinvalue==None:
            self.meanbinvalue = 0.
            sumofweights = 0.
            for i in range(len(self.data)):
                if self.is2dim:
                    binwidth = abs( (self.data[i]['UpEdge'][0] - self.data[i]['LowEdge'][0])
                                   *(self.data[i]['UpEdge'][1] - self.data[i]['LowEdge'][1]))
                else:
                    binwidth = abs(self.data[i]['UpEdge'] - self.data[i]['LowEdge'])
                self.meanbinvalue += binwidth*self.data[i]['Content']
                sumofweights += binwidth
            self.meanbinvalue /= sumofweights
        return self.meanbinvalue

    def getCorrelation(self, name):
        correlation = 0.
        sumofweights = 0.
        for i in range(len(self.data)):
            if fuzzyeq(self.data[i]['LowEdge'], name.data[i]['LowEdge']) and \
               fuzzyeq(self.data[i]['UpEdge'], name.data[i]['UpEdge']):
                if self.is2dim:
                    binwidth = abs( (self.data[i]['UpEdge'][0] - self.data[i]['LowEdge'][0])
                                  * (self.data[i]['UpEdge'][1] - self.data[i]['LowEdge'][1]) )
                else:
                    binwidth = abs(self.data[i]['UpEdge'] - self.data[i]['LowEdge'])
                correlation += binwidth * ( self.data[i]['Content'] - self.getMeanBinValue() ) \
                                        * ( name.data[i]['Content'] - name.getMeanBinValue() )
                sumofweights += binwidth
            else:
                print '+++ Error in Histogram.getCorrelation(): binning of histograms differs' % self.path
        correlation /= sumofweights
        try:
            correlation /= self.getSigmaBinValue()*name.getSigmaBinValue()
        except ZeroDivisionError:
            correlation = 0
        return correlation

    def getRMSdistance(self,name):
        distance = 0.
        sumofweights = 0.
        for i in range(len(self.data)):
            if fuzzyeq(self.data[i]['LowEdge'], name.data[i]['LowEdge']) and \
               fuzzyeq(self.data[i]['UpEdge'], name.data[i]['UpEdge']):
                if self.is2dim:
                    binwidth = abs( (self.data[i]['UpEdge'][0] - self.data[i]['LowEdge'][0])
                                  * (self.data[i]['UpEdge'][1] - self.data[i]['LowEdge'][1]) )
                else:
                    binwidth = abs(self.data[i]['UpEdge'] - self.data[i]['LowEdge'])
                distance += binwidth * ( (self.data[i]['Content'] - self.getMeanBinValue())
                                        -(name.data[i]['Content'] - name.getMeanBinValue()))**2
                sumofweights += binwidth
            else:
                print '+++ Error in Histogram.getRMSdistance() for %s: binning of histograms differs' % self.path
        distance = sqrt(distance/sumofweights)
        return distance

    def draw(self,coors):
        seen_nan = False
        out = ""
        out += self.startclip()
        out += self.startpsset()
        #
        if self.is2dim:
            for i in range(len(self.data)):
                out += ('\\psframe')
                color=int(129*coors.phys2frameZ(self.data[i]['Content']))
                if self.data[i]['Content']>coors.zmax():
                    color=129
                if self.data[i]['Content']<coors.zmin():
                    color=0
                if self.data[i]['Content']<=coors.zmin():
                    out += ('[linewidth=0pt, linestyle=none, fillstyle=solid, fillcolor=white]')
                else:
                    out += ('[linewidth=0pt, linestyle=none, fillstyle=solid, fillcolor={gradientcolors!!['+str(color)+']}]')
                out += ('(' + coors.strphys2frameX(self.data[i]['LowEdge'][0]) + ', ' \
                            + coors.strphys2frameY(self.data[i]['LowEdge'][1]) + ')(' \
                            + coors.strphys2frameX(self.data[i]['UpEdge'][0])  + ', ' \
                            + coors.strphys2frameY(self.data[i]['UpEdge'][1])  + ')\n')
        else:
            if self.getErrorBands():
                self.description['SmoothLine']=0
                for i in range(len(self.data)):
                    out += ('\\psframe[dimen=inner,linewidth=0pt,linestyle=none,fillstyle=%s,hatchcolor=%s,fillcolor=%s,opacity=%s]' %(self.getErrorBandStyle(),self.getErrorBandColor(),self.getErrorBandColor(),self.getErrorBandOpacity()))
                    out += ('(' + coors.strphys2frameX(self.data[i]['LowEdge']) + ', ' \
                                + coors.strphys2frameY(self.data[i]['Content']-self.data[i]['Error'][0]) + ')(' \
                                + coors.strphys2frameX(self.data[i]['UpEdge'])  + ', ' \
                                + coors.strphys2frameY(self.data[i]['Content']+self.data[i]['Error'][1]) + ')\n')
            if self.getErrorBars():
                for i in range(len(self.data)):
                    if isnan(self.data[i]['Content']) or isnan(self.data[i]['Error'][0]) or isnan(self.data[i]['Error'][1]):
                        seen_nan = True
                        continue
                    if self.data[i]['Content']==0. and self.data[i]['Error']==[0.,0.]:
                        continue
                    out += ('\psline')
                    out += ('(' + coors.strphys2frameX(self.data[i]['LowEdge']) + ', ' \
                                + coors.strphys2frameY(self.data[i]['Content']) + ')(' \
                                + coors.strphys2frameX(self.data[i]['UpEdge'])  + ', ' \
                                + coors.strphys2frameY(self.data[i]['Content']) + ')\n')
                    out += ('\psline')
                    bincenter = coors.strphys2frameX(.5*(self.data[i]['LowEdge']+self.data[i]['UpEdge']))
                    out += ('(' + bincenter + ', ' \
                                + coors.strphys2frameY(self.data[i]['Content']-self.data[i]['Error'][0]) + ')(' \
                                + bincenter + ', ' \
                                + coors.strphys2frameY(self.data[i]['Content']+self.data[i]['Error'][1]) + ')\n')
            if self.getSmoothLine():
                out += ('\psbezier')
            else:
                out += ('\psline')
            if (self.getFillStyle() != 'none'):   # make sure that filled areas go all the way down to the x-axis
                if (coors.phys2frameX(self.data[0]['LowEdge']) > 1e-4):
                    out += '(' + coors.strphys2frameX(self.data[0]['LowEdge']) + ', -0.1)\n'
                else:
                    out += '(-0.1, -0.1)\n'
            for i in range(len(self.data)):
                if isnan(self.data[i]['Content']):
                    seen_nan = True
                    continue
                if self.getSmoothLine():
                    out += ('(' + coors.strphys2frameX(0.5*(self.data[i]['LowEdge']+self.data[i]['UpEdge'])) + ', ' \
                                + coors.strphys2frameY(self.data[i]['Content']) + ')\n')
                else:
                    out += ('(' + coors.strphys2frameX(self.data[i]['LowEdge']) + ', ' \
                                + coors.strphys2frameY(self.data[i]['Content']) + ')(' \
                                + coors.strphys2frameX(self.data[i]['UpEdge'])  + ', ' \
                                + coors.strphys2frameY(self.data[i]['Content']) + ')\n')
                    ## Join/separate data points, with vertical/diagonal lines
                    if (i+1 < len(self.data)): #< If this is not the last point
                        if self.description.get('ConnectBins', '1') != '1':
                            out += ('\\psline')
                        else:
                            ## If bins are joined, but there is a gap in binning, choose whether to fill the gap
                            if (abs(coors.phys2frameX(self.data[i]['UpEdge']) - coors.phys2frameX(self.data[i+1]['LowEdge'])) > 1e-4):
                                if self.description.get('ConnectGaps', '0') != '1':
                                    out += ('\\psline')
                                    # TODO: Perhaps use a new dashed line to fill the gap?
            if (self.getFillStyle() != 'none'):   # make sure that filled areas go all the way down to the x-axis
                if (coors.phys2frameX(self.data[-1]['UpEdge']) < 1-1e-4):
                    out += '(' + coors.strphys2frameX(self.data[-1]['UpEdge']) + ', -0.1)\n'
                else:
                    out += '(1.1, -0.1)\n'
        #
        if self.getPolyMarker() != '':
            for i in range(len(self.data)):
                if isnan(self.data[i]['Content']):
                    seen_nan = True
                    continue
                if self.data[i]['Content']==0. and self.data[i]['Error']==[0.,0.]:
                    continue
                out += ('\\psdot[dotstyle=%s,dotsize=%s,dotscale=%s](' %(self.getPolyMarker(),self.getDotSize(),self.getDotScale()) \
                            + coors.strphys2frameX(.5*(self.data[i]['LowEdge']+self.data[i]['UpEdge'])) + ', ' \
                            + coors.strphys2frameY(self.data[i]['Content']) + ')\n')
        out += self.stoppsset()
        out += self.stopclip()
        if seen_nan:
            print "WARNING: NaN-valued value or error bar!"
        return out

    # def is2dimensional(self):
    #     return self.is2dim

    def getXMin(self):
        if self.is2dim:
            return min([self.data[i]['LowEdge'][0] for i in range(len(self.data))])
        else:
            return min([self.data[i]['LowEdge'] for i in range(len(self.data))])

    def getXMax(self):
        if self.is2dim:
            return max([self.data[i]['UpEdge'][0] for i in range(len(self.data))])
        else:
            return max([self.data[i]['UpEdge'] for i in range(len(self.data))])

    def getYMin(self, xmin, xmax, logy):
        if self.is2dim:
            return min([self.data[i]['LowEdge'][1] for i in range(len(self.data))])
        else:
            yvalues = []
            for i in range(len(self.data)):
                if ((self.data[i]['UpEdge'] > xmin or self.data[i]['LowEdge'] >= xmin) and \
                    (self.data[i]['LowEdge'] < xmax or self.data[i]['UpEdge'] <= xmax)):
                    foo = 0
                    if self.getErrorBars() or self.getErrorBands():
                        foo = self.data[i]['Content']-self.data[i]['Error'][0]
                    else:
                        foo = self.data[i]['Content']
                    if logy:
                        if foo>0: yvalues.append(foo)
                    else:
                        yvalues.append(foo)
            if len(yvalues) > 0:
                return min(yvalues)
            else:
                return self.data[0]['Content']

    def getYMax(self, xmin, xmax):
        if self.is2dim:
            return max([self.data[i]['UpEdge'][1] for i in range(len(self.data))])
        else:
            yvalues = []
            for i in range(len(self.data)):
                if ((self.data[i]['UpEdge'] > xmin or self.data[i]['LowEdge'] >= xmin) and \
                    (self.data[i]['LowEdge'] < xmax or self.data[i]['UpEdge'] <= xmax)):
                    if self.getErrorBars() or self.getErrorBands():
                        yvalues.append(self.data[i]['Content']+self.data[i]['Error'][1])
                    else:
                        yvalues.append(self.data[i]['Content'])
            if len(yvalues) > 0:
                return max(yvalues)
            else:
                return self.data[0]['Content']

    def getZMin(self, xmin, xmax, ymin, ymax):
        if not self.is2dim:
            return 0
        zvalues = []
        for i in range(len(self.data)):
            if (self.data[i]['UpEdge'][0] > xmin and self.data[i]['LowEdge'][0] < xmax) and \
               (self.data[i]['UpEdge'][1] > ymin and self.data[i]['LowEdge'][1] < ymax):
                zvalues.append(self.data[i]['Content'])
        return min(zvalues)

    def getZMax(self, xmin, xmax, ymin, ymax):
        if not self.is2dim:
            return 0
        zvalues = []
        for i in range(len(self.data)):
            if (self.data[i]['UpEdge'][0] > xmin and self.data[i]['LowEdge'][0] < xmax) and \
               (self.data[i]['UpEdge'][1] > ymin and self.data[i]['LowEdge'][1] < ymax):
                zvalues.append(self.data[i]['Content'])
        return max(zvalues)



class Histo1D(Histogram):
    def read_input_data(self, f):
        for line in f:
            if is_end_marker(line, 'HISTO1D'):
                break
            elif is_comment(line):
                continue
            else:
                line = line.rstrip()
                m = pat_property.match(line)
                if m:
                    prop, value = m.group(1,2)
                    self.description[prop] = value
                else:
                    linearray = line.split()
                    ## Detect symm errs
                    if len(linearray) == 4:
                        self.data.append({'LowEdge': float(linearray[0]),
                                          'UpEdge':  float(linearray[1]),
                                          'Content': float(linearray[2]),
                                          'Error':   [float(linearray[3]),float(linearray[3])]})
                    ## Detect asymm errs
                    elif len(linearray) == 5:
                        self.data.append({'LowEdge': float(linearray[0]),
                                          'UpEdge':  float(linearray[1]),
                                          'Content': float(linearray[2]),
                                          'Error':   [float(linearray[3]),float(linearray[4])]})
                    ## Not sure what this is for... auto-compatibility with YODA format? Urgh
                    elif len(linearray) == 8:
                        self.data.append({'LowEdge': float(linearray[0]),
                                          'UpEdge':  float(linearray[1]),
                                          'Content': float(linearray[2]),
                                          'Error':   [float(linearray[3]),float(linearray[3])]})
                    else:
                        raise Exception('Histo1D does not have 8 columns.'+line)


class Histo2D(Histogram):
    def read_input_data(self, f):
        self.is2dim = True #< Should really be done in a constructor, but this is easier for now...

        for line in f:
            if is_end_marker(line, 'HISTO2D'):
                break
            elif is_comment(line):
                continue
            else:
                line = line.rstrip()
                m = pat_property.match(line)
                if m:
                    prop, value = m.group(1,2)
                    self.description[prop] = value
                else:
                    linearray = line.split()
                    if len(linearray) in [6,7]:
                        # If asymm z error, use the max or average of +- error
                        err = float(linearray[5])
                        if len(linearray) == 7:
                            if self.description.get("ShowMaxZErr", 1):
                                err = max(err, float(linearray[6]))
                            else:
                                err = 0.5 * (err + float(linearray[6]))
                        self.data.append({'LowEdge': [float(linearray[0]), float(linearray[2])],
                                          'UpEdge':  [float(linearray[1]), float(linearray[3])],
                                          'Content': float(linearray[4]),
                                          'Error':   err})
                    else:
                        raise Exception('Histo1D does not have 6 or 7 columns.'+line)




class Frame(object):
    def __init__(self):
        self.framelinewidth = '0.3pt'

    def draw(self,inputdata):
        out = ('\n%\n% Frame\n%\n')
        if inputdata.description.has_key('FrameColor') and inputdata.description['FrameColor']!=None:
            color = inputdata.description['FrameColor']
            # We want to draw this frame only once, so set it to False for next time:
            inputdata.description['FrameColor']=None

            # Calculate how high and wide the overall plot is
            height = [0,0]
            width  = inputdata.description['PlotSizeX']
            print "aaaa" ,inputdata.description['RatioPlot']
            if inputdata.description.has_key('RatioPlot') and inputdata.description['RatioPlot']!='0':
                print int(inputdata.description['RatioPlot'])
                height[1] = -(inputdata.description['RatioPlotSizeY']*int(inputdata.description['RatioPlot']))
            if not (inputdata.description.has_key('MainPlot') and inputdata.description['MainPlot']=='0'):
                print "aaaas" ,inputdata.description['RatioPlot']
                height[0] = inputdata.description['PlotSizeY']
            else:
                print "aaaaw" ,inputdata.description['RatioPlot']
                height[0] = -height[1]
                height[1] = 0

            # Get the margin widths
            left = inputdata.description['LeftMargin']+0.1
            right = inputdata.description['RightMargin']+0.1
            top = inputdata.description['TopMargin']+0.1
            bottom = inputdata.description['BottomMargin']+0.1

            #
            out += ('\\rput(0,1){\\psline[linewidth=%scm,linecolor=%s](%scm,%scm)(%scm,%scm)}\n' %(top, color, -left, top/2, width+right, top/2))
            out += ('\\rput(0,%scm){\\psline[linewidth=%scm,linecolor=%s](%scm,%scm)(%scm,%scm)}\n' %(height[1], bottom, color, -left, -bottom/2, width+right, -bottom/2))
            out += ('\\rput(0,0){\\psline[linewidth=%scm,linecolor=%s](%scm,%scm)(%scm,%scm)}\n' %(left, color, -left/2, height[1]-0.05, -left/2, height[0]+0.05))
            out += ('\\rput(1,0){\\psline[linewidth=%scm,linecolor=%s](%scm,%scm)(%scm,%scm)}\n' %(right, color, right/2, height[1]-0.05, right/2, height[0]+0.05))


        out += ('\\psframe[linewidth='+self.framelinewidth+',dimen=middle](0,0)(1,1)\n')
        return out



class Ticks(object):
    def __init__(self, description, coors,ratio=False):
        self.majorticklinewidth = '0.3pt'
        self.minorticklinewidth = '0.3pt'
        self.majorticklength    = '9pt'
        self.minorticklength    = '4pt'
        self.description = description
        self.coors = coors
        self.ratio=ratio

    def draw_ticks(self, min, max, plotlog=False, custommajorticks=[], customminorticks=[], custommajortickmarks=-1, customminortickmarks=-1, drawlabels=True, twosided=False):
        out = ""
        if plotlog:
            if min <= 0 or max <= 0:
                raise Exception("Cannot place log axis min or max tick <= 0")
            if len(custommajorticks) ==0:
                x=int(log10(min))
                n_labels=0
                while (x<log10(max)+1):
                    if 10**x>=min:
                        ticklabel=10**x
                        if ticklabel>min and ticklabel<max:
                            out += self.draw_majortick(ticklabel,twosided)
                            if drawlabels:
                                out += self.draw_majorticklabel(ticklabel)
                                n_labels+=1
                        if ticklabel==min or ticklabel==max:
                            if drawlabels:
                                out += self.draw_majorticklabel(ticklabel)
                                n_labels+=1
                        for i in range(2,10):
                            ticklabel=i*10**(x-1)
                            if ticklabel>min and ticklabel<max:
                                out += self.draw_minortick(ticklabel,twosided)
                                if drawlabels and n_labels==0:
                                    if (i+1)*10**(x-1)<max: # some special care for the last minor tick
                                        out += self.draw_minorticklabel(ticklabel)
                                    else:
                                        out += self.draw_minorticklabel(ticklabel, last=True)
                    x+=1
        elif (custommajorticks!=[] or customminorticks!=[]):
            for i in range(len(custommajorticks)):
                value=custommajorticks[i]['Value']
                label=custommajorticks[i]['Label']
                if value>=min and value<=max:
                    out += self.draw_majortick(value,twosided)
                if drawlabels:
                    out += self.draw_majorticklabel(value, label=label)
            for i in range(len(customminorticks)):
                value=customminorticks[i]['Value']
                if value>=min and value<=max:
                    out += self.draw_minortick(value,twosided)
        else:
            xrange = max-min
            
            if self.ratio:
              max=max-0.00001
            
            digits = int(log10(xrange))+1
            if (xrange < 1):
                digits -= 1
            foo = int(xrange/(10**(digits-1)))
            if (foo/9. > 0.5):
                tickmarks = 10
            elif (foo/9. > 0.2):
                tickmarks = 5
            elif (foo/9. > 0.1):
                tickmarks = 2

            if (custommajortickmarks>-1):
                if custommajortickmarks not in [1, 2, 5, 10, 20]:
                    print '+++ Error in Ticks.draw_ticks(): MajorTickMarks must be in [1, 2, 5, 10, 20]'
                else:
                    #if custommajortickmarks==1: custommajortickmarks=10
                    tickmarks = custommajortickmarks

            if (tickmarks == 2 or tickmarks == 20):
                minortickmarks = 3
            else:
                minortickmarks = 4
            if (customminortickmarks>-1):
                minortickmarks = customminortickmarks
            #
            x = 0
            while (x > min*10**digits):
                x -= tickmarks*100**(digits-1)
            while (x <= max*10**digits):
                if (x >= min*10**digits-tickmarks*100**(digits-1)):
                    ticklabel = 1.*x/10**digits
                    if (int(ticklabel) == ticklabel):
                        ticklabel = int(ticklabel)
                    if (float(ticklabel-min)/xrange >= -1e-5):
                        if (fabs(ticklabel-min)/xrange > 1e-5 and fabs(ticklabel-max)/xrange > 1e-5):
                            out += self.draw_majortick(ticklabel,twosided)
                        if drawlabels:
                            out += self.draw_majorticklabel(ticklabel)

                    xminor = x
                    for i in range(minortickmarks):
                        xminor += 1.*tickmarks*100**(digits-1)/(minortickmarks+1)
                        ticklabel = 1.*xminor/10**digits
                        if (ticklabel > min and ticklabel < max):
                            if (fabs(ticklabel-min)/xrange > 1e-5 and fabs(ticklabel-max)/xrange > 1e-5):
                                out += self.draw_minortick(ticklabel,twosided)
                x += tickmarks*100**(digits-1)
        return out

    def draw(self):
        pass

    def draw_minortick(self, ticklabel, twosided):
        pass

    def draw_majortick(self, ticklabel, twosided):
        pass

    def draw_majorticklabel(self, ticklabel):
        pass

    def draw_minorticklabel(self, value, label='', last=False):
        return ''

    def get_ticklabel(self, value, plotlog=False, minor=False, lastminor=False):
        label=''
        prefix = ""
        if plotlog:
            bar = int(log10(value))
	    if bar<0:
	        sign='-'
	    else:
	        sign='\\,'
            if minor: # The power of ten is only to be added to the last minor tick label
                if lastminor:
                    label = str(int(value/(10**bar))) + "\cdot" + '10$^{'+sign+'\\text{'+str(abs(bar))+'}}$'
                else:
                    label = str(int(value/(10**bar))) # The naked prefactor
            else:
                if bar==0:
                    label = '1'
                else:
                    label = '10$^{'+sign+'\\text{'+str(abs(bar))+'}}$'
        else:
            if fabs(value) < 1e-10: value=0
            label=str(value)
        return label



class XTicks(Ticks):
    def draw(self, custommajorticks=[], customminorticks=[], custommajortickmarks=-1, customminortickmarks=-1,drawlabels=True):
        twosided = False
        if self.description.has_key('XTwosidedTicks') and self.description['XTwosidedTicks']=='1':
            twosided = True
        out = ""
        out += ('\n%\n% X-Ticks\n%\n')
        out += ('\\def\\majortickmarkx{\\psline[linewidth='+self.majorticklinewidth+'](0,0)(0,'+self.majorticklength+')}%\n')
        out += ('\\def\\minortickmarkx{\\psline[linewidth='+self.minorticklinewidth+'](0,0)(0,'+self.minorticklength+')}%\n')
        uselog = self.description['LogX'] and (self.coors.xmin() > 0 and self.coors.xmax() > 0)
        out += self.draw_ticks(self.coors.xmin(), self.coors.xmax(),\
                                   plotlog=uselog,\
                                   custommajorticks=custommajorticks,\
                                   customminorticks=customminorticks,\
                                   custommajortickmarks=custommajortickmarks,\
                                   customminortickmarks=customminortickmarks,\
                                   drawlabels=drawlabels,\
                                   twosided=twosided)
        return out

    def draw_minortick(self, ticklabel, twosided):
        out = ''
        out += '\\rput('+self.coors.strphys2frameX(ticklabel)+', 0){\\minortickmarkx}\n'
        if twosided:
            out += '\\rput{180}('+self.coors.strphys2frameX(ticklabel)+', 1){\\minortickmarkx}\n'
        return out

    def draw_minorticklabel(self, value, label='', last=False):
        if label=='':
            label=self.get_ticklabel(value,self.description['LogX'], minor=True, lastminor=last)
        if last: # Some more indentation for the last minor label
            return ('\\rput('+self.coors.strphys2frameX(value)+', 0){\\rput[B](1.9\\labelsep,-2.3\\labelsep){\\strut{}'+label+'}}\n')
        else:
            return ('\\rput('+self.coors.strphys2frameX(value)+', 0){\\rput[B](0,-2.3\\labelsep){\\strut{}'+label+'}}\n')

    def draw_majortick(self, ticklabel, twosided):
        out = ''
        out += '\\rput('+self.coors.strphys2frameX(ticklabel)+', 0){\\majortickmarkx}\n'
        if twosided:
            out += '\\rput{180}('+self.coors.strphys2frameX(ticklabel)+', 1){\\majortickmarkx}\n'
        return out

    def draw_majorticklabel(self, value, label=''):
        if label=='':
            label=self.get_ticklabel(value, self.description['LogX'] and (self.coors.xmin() > 0 and self.coors.xmax() > 0))
        return ('\\rput('+self.coors.strphys2frameX(value)+', 0){\\rput[B](0,-2.3\\labelsep){\\strut{}'+label+'}}\n')



class YTicks(Ticks):
    def draw(self, custommajorticks=[], customminorticks=[], custommajortickmarks=-1, customminortickmarks=-1,drawlabels=True):
        twosided = False
        if self.description.has_key('YTwosidedTicks') and self.description['YTwosidedTicks']=='1':
            twosided = True
        out = ""
        out += ('\n%\n% Y-Ticks\n%\n')
        out += ('\\def\\majortickmarky{\\psline[linewidth='+self.majorticklinewidth+'](0,0)('+self.majorticklength+',0)}%\n')
        out += ('\\def\\minortickmarky{\\psline[linewidth='+self.minorticklinewidth+'](0,0)('+self.minorticklength+',0)}%\n')
        uselog = self.description['LogY'] and (self.coors.ymin() > 0 and self.coors.ymax() > 0)
        out += self.draw_ticks(self.coors.ymin(), self.coors.ymax(),\
                                   plotlog=uselog,\
                                   custommajorticks=custommajorticks,\
                                   customminorticks=customminorticks,\
                                   custommajortickmarks=custommajortickmarks,\
                                   customminortickmarks=customminortickmarks,\
                                   twosided=twosided,
                                   drawlabels=drawlabels)
        return out

    def draw_minortick(self, ticklabel, twosided):
        out = ''
        out += '\\rput(0, '+self.coors.strphys2frameY(ticklabel)+'){\\minortickmarky}\n'
        if twosided:
            out += '\\rput{180}(1, '+self.coors.strphys2frameY(ticklabel)+'){\\minortickmarky}\n'
        return out

    def draw_majortick(self, ticklabel, twosided):
        out = ''
        out += '\\rput(0, '+self.coors.strphys2frameY(ticklabel)+'){\\majortickmarky}\n'
        if twosided:
            out += '\\rput{180}(1, '+self.coors.strphys2frameY(ticklabel)+'){\\majortickmarky}\n'
        return out

    def draw_majorticklabel(self, value, label=''):
        if label=='':
            label=self.get_ticklabel(value, self.description['LogY'] and (self.coors.ymin() > 0 and self.coors.ymax() > 0))
        if self.description.has_key('RatioPlotMode') and self.description['RatioPlotMode']=='deviation' \
                and self.description.has_key('RatioPlotStage') and self.description['RatioPlotStage']:
            return ('\\uput[180]{0}(0, '+self.coors.strphys2frameY(value)+'){\\strut{}'+label+'\\,$\\sigma$}\n')
        else:
            return ('\\uput[180]{0}(0, '+self.coors.strphys2frameY(value)+'){\\strut{}'+label+'}\n')



class ZTicks(Ticks):
    def __init__(self, description, coors):
        self.majorticklinewidth = '0.3pt'
        self.minorticklinewidth = '0.3pt'
        self.majorticklength    = '6pt'
        self.minorticklength    = '2.6pt'
        self.description = description
        self.coors = coors
    def draw(self, custommajorticks=[], customminorticks=[],
            custommajortickmarks=-1, customminortickmarks=-1,
            drawlabels=True):
        out = ""
        out += ('\n%\n% Z-Ticks\n%\n')
        out += ('\\def\\majortickmarkz{\\psline[linewidth='+self.majorticklinewidth+'](0,0)('+self.majorticklength+',0)}%\n')
        out += ('\\def\\minortickmarkz{\\psline[linewidth='+self.minorticklinewidth+'](0,0)('+self.minorticklength+',0)}%\n')
        out += self.draw_ticks(self.coors.zmin(), self.coors.zmax(),\
                                   plotlog=self.description['LogZ'],\
                                   custommajorticks=custommajorticks,\
                                   customminorticks=customminorticks,\
                                   custommajortickmarks=custommajortickmarks,\
                                   customminortickmarks=customminortickmarks,\
                                   twosided=False,\
                                   drawlabels=drawlabels)
        return out

    def draw_minortick(self, ticklabel, twosided):
        return '\\rput{180}(1, '+self.coors.strphys2frameZ(ticklabel)+'){\\minortickmarkz}\n'

    def draw_majortick(self, ticklabel, twosided):
        return '\\rput{180}(1, '+self.coors.strphys2frameZ(ticklabel)+'){\\majortickmarkz}\n'

    def draw_majorticklabel(self, value, label=''):
        if label=='':
            label=self.get_ticklabel(value,self.description['LogZ'])
        if self.description.has_key('RatioPlotMode') and self.description['RatioPlotMode']=='deviation' \
                and self.description.has_key('RatioPlotStage') and self.description['RatioPlotStage']:
            return ('\\uput[0]{0}(1, '+self.coors.strphys2frameZ(value)+'){\\strut{}'+label+'\\,$\\sigma$}\n')
        else:
            return ('\\uput[0]{0}(1, '+self.coors.strphys2frameZ(value)+'){\\strut{}'+label+'}\n')



class Coordinates(object):
    def __init__(self, inputdata):
        self.description = inputdata.description

    def phys2frameX(self, x):
        if self.description['LogX']:
            if x>0:
                result = 1.*(log10(x)-log10(self.xmin()))/(log10(self.xmax())-log10(self.xmin()))
            else:
                return -10
        else:
            result = 1.*(x-self.xmin())/(self.xmax()-self.xmin())
        if (fabs(result) < 1e-4):
            return 0
        else:
            return min(max(result,-10),10)

    def phys2frameY(self, y):
        if self.description['LogY']:
            if y > 0 and self.ymin() > 0 and self.ymax() > 0:
                result = 1.*(log10(y)-log10(self.ymin()))/(log10(self.ymax())-log10(self.ymin()))
            else:
                return -10
        else:
            result = 1.*(y-self.ymin())/(self.ymax()-self.ymin())
        if (fabs(result) < 1e-4):
            return 0
        else:
            return min(max(result,-10),10)

    def phys2frameZ(self, z):
        if self.description['LogZ']:
            if z>0:
                result = 1.*(log10(z)-log10(self.zmin()))/(log10(self.zmax())-log10(self.zmin()))
            else:
                return -10
        else:
            result = 1.*(z-self.zmin())/(self.zmax()-self.zmin())
        if (fabs(result) < 1e-4):
            return 0
        else:
            return min(max(result,-10),10)

    # TODO: Add frame2phys functions (to allow linear function sampling in the frame space rather than the physical space)

    def strphys2frameX(self, x):
        return str(self.phys2frameX(x))

    def strphys2frameY(self, y):
        return str(self.phys2frameY(y))

    def strphys2frameZ(self, z):
        return str(self.phys2frameZ(z))

    def xmin(self):
        return self.description['Borders'][0]

    def xmax(self):
        return self.description['Borders'][1]

    def ymin(self):
        return self.description['Borders'][2]

    def ymax(self):
        return self.description['Borders'][3]

    def zmin(self):
        return self.description['Borders'][4]

    def zmax(self):
        return self.description['Borders'][5]


####################


def try_cmd(args):
    "Run the given command + args and return True/False if it succeeds or not"
    import subprocess
    try:
        subprocess.check_output(args, stderr=subprocess.STDOUT)
        return True
    except AttributeError:
        # Python <=2.6 does not provide check_output
        return True
    except:
        return False

def have_cmd(cmd):
    return try_cmd(["which", cmd])


import shutil, subprocess
def process_datfile(datfile):
    global opts
    if not os.access(datfile, os.R_OK):
        raise Exception("Could not read data file '%s'" % datfile)

    dirname = os.path.dirname(datfile)
    datfile = os.path.basename(datfile)
    filename = datfile.replace('.dat','')

    ## Create a temporary directory
    cwd = os.getcwd()
    datpath = os.path.join(cwd, dirname, datfile)
    tempdir = tempfile.mkdtemp('.make-plots')
    tempdatpath = os.path.join(tempdir, datfile)
    shutil.copy(datpath, tempdir)

    ## Make TeX file
    inputdata = Inputdata(os.path.join(dirname,filename))
    texpath = os.path.join(tempdir, '%s.tex' % filename)
    texfile = open(texpath, 'w')
    p = Plot(inputdata)
    texfile.write(p.write_header(inputdata))
    if inputdata.description.get('MainPlot', '1') == '1':
        mp = MainPlot(inputdata)
        texfile.write(mp.draw(inputdata))
    if not inputdata.description.get('is2dim', False) and \
           inputdata.description.get('RatioPlot', '1') != '0' and \
           inputdata.description.get('RatioPlotReference') is not None:
      rpheight=inputdata.description['RatioPlotSizeY']
      for i in range(int(inputdata.description.get('RatioPlot', '1'))):
        print i,int(inputdata.description.get('RatioPlot', '1'))
        rp = RatioPlot(inputdata,i)
        #print "xxx",rp.yoffset,i*rpheight
        #rp.yoffset=rp.yoffset+float(i*rpheight)
        print "xxx",rp.yoffset,i*rpheight
        texfile.write(rp.draw(inputdata,((i+1)==int(inputdata.description.get('RatioPlot', '1'))),i))
        
        print "aa"
    texfile.write(p.write_footer())
    texfile.close()

    if opts.OUTPUT_FORMAT != "TEX":

        ## Check for the required programs
        latexavailable = have_cmd("latex")
        dvipsavailable = have_cmd("dvips")
        convertavailable = have_cmd("convert")
        ps2pnmavailable = have_cmd("ps2pnm")
        pnm2pngavailable = have_cmd("pnm2png")

        # TODO: It'd be nice to be able to control the size of the PNG between thumb and full-size...
        #   currently defaults (and is used below) to a size suitable for thumbnails
        def mkpng(infile, outfile, density=100):
            if convertavailable:
                pngcmd = ["convert", "-flatten", "-density", str(density), infile, "-quality", "100", "-sharpen", "0x1.0", outfile]
                logging.debug(" ".join(pngcmd))
                pngproc = subprocess.Popen(pngcmd, stdout=subprocess.PIPE, cwd=tempdir)
                pngproc.wait()
            else:
                raise Exception("Required PNG maker program (convert) not found")
            # elif ps2pnmavailable and pnm2pngavailable:
            #     pstopnm = "pstopnm -stdout -xsize=461 -ysize=422 -xborder=0.01 -yborder=0.01 -portrait " + infile
            #     p1 = subprocess.Popen(pstopnm.split(), stdout=subprocess.PIPE, stderr=open("/dev/null", "w"), cwd=tempdir)
            #     p2 = subprocess.Popen(["pnmtopng"], stdin=p1.stdout, stdout=open("%s/%s.png" % (tempdir, outfile), "w"), stderr=open("/dev/null", "w"), cwd=tempdir)
            #     p2.wait()
            # else:
            #     raise Exception("Required PNG maker programs (convert, or ps2pnm and pnm2png) not found")

        ## Run LaTeX (in no-stop mode)
        logging.debug(os.listdir(tempdir))
        texcmd = ["latex", "\scrollmode\input", texpath]
        logging.debug("TeX command: " + " ".join(texcmd))
        texproc = subprocess.Popen(texcmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=tempdir)
        logging.debug(texproc.communicate()[0])
        logging.debug(os.listdir(tempdir))

        ## Run dvips
        dvcmd = ["dvips", filename]
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            dvcmd.append("-q")
        ## Handle Minion Font
        if opts.OUTPUT_FONT == "MINION":
            dvcmd.append('-Pminion')

        ## Choose format
        # TODO: Rationalise... this is a mess! Maybe we can use tex2pix?
        if opts.OUTPUT_FORMAT == "PS":
            dvcmd += ["-o", "%s.ps" % filename]
            logging.debug(" ".join(dvcmd))
            dvproc = subprocess.Popen(dvcmd, stdout=subprocess.PIPE, cwd=tempdir)
            dvproc.wait()
        elif opts.OUTPUT_FORMAT == "PDF":
            dvcmd.append("-f")
            logging.debug(" ".join(dvcmd))
            dvproc = subprocess.Popen(dvcmd, stdout=subprocess.PIPE, cwd=tempdir)
            cnvproc = subprocess.Popen(["ps2pdf", "-"], stdin=dvproc.stdout, stdout=subprocess.PIPE, cwd=tempdir)
            f = open(os.path.join(tempdir, "%s.pdf" % filename), "w")
            f.write(cnvproc.communicate()[0])
            f.close()
        elif opts.OUTPUT_FORMAT == "EPS":
            dvcmd.append("-f")
            logging.debug(" ".join(dvcmd))
            dvproc = subprocess.Popen(dvcmd, stdout=subprocess.PIPE, cwd=tempdir)
            cnvproc = subprocess.Popen(["ps2eps"], stdin=dvproc.stdout, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=tempdir)
            f = open(os.path.join(tempdir, "%s.eps" % filename), "w")
            f.write(cnvproc.communicate()[0])
            f.close()
        elif opts.OUTPUT_FORMAT == "PNG":
            dvcmd.append("-f")
            logging.debug(" ".join(dvcmd))
            dvproc = subprocess.Popen(dvcmd, stdout=subprocess.PIPE, cwd=tempdir)
            pngcmd = ["convert", "-flatten", "-density", "100", "-", "-quality", "100", "-sharpen", "0x1.0", "%s.png" % filename]
            logging.debug(" ".join(pngcmd))
            pngproc = subprocess.Popen(pngcmd, stdin=dvproc.stdout, stdout=subprocess.PIPE, cwd=tempdir)
            pngproc.wait()
        elif opts.OUTPUT_FORMAT == "PSPNG":
            dvcmd += ["-o", "%s.ps" % filename]
            logging.debug(" ".join(dvcmd))
            dvproc = subprocess.Popen(dvcmd, stdout=subprocess.PIPE, cwd=tempdir)
            dvproc.wait()
            mkpng("%s.ps" % filename, "%s.png" % filename)
        elif opts.OUTPUT_FORMAT == "PDFPNG":
            dvcmd.append("-f")
            logging.debug(" ".join(dvcmd))
            dvproc = subprocess.Popen(dvcmd, stdout=subprocess.PIPE, cwd=tempdir)
            cnvproc = subprocess.Popen(["ps2pdf", "-"], stdin=dvproc.stdout, stdout=subprocess.PIPE, cwd=tempdir)
            f = open(os.path.join(tempdir, "%s.pdf" % filename), "w")
            f.write(cnvproc.communicate()[0])
            f.close()
            logging.debug(os.listdir(tempdir))
            mkpng("%s.pdf" % filename, "%s.png" % filename)
        elif opts.OUTPUT_FORMAT == "EPSPNG":
            dvcmd.append("-f")
            logging.debug(" ".join(dvcmd))
            dvproc = subprocess.Popen(dvcmd, stdout=subprocess.PIPE, cwd=tempdir)
            cnvproc = subprocess.Popen(["ps2eps"], stdin=dvproc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tempdir)
            f = open(os.path.join(tempdir, "%s.eps" % filename), "w")
            f.write(cnvproc.communicate()[0])
            f.close()
            mkpng("%s.eps" % filename, "%s.png" % filename)
        else:
            logging.error("Unknown format: %s" % opts.OUTPUT_FORMAT)
            sys.exit(1)
        logging.debug(os.listdir(tempdir))

    ## Copy results back to main dir
    outbasename = filename
    outname = outbasename + "." + opts.OUTPUT_FORMAT.lower()
    ## TODO: Make this neater: if "PNG" in opts.OUTPUT_FORMAT: ...
    if opts.OUTPUT_FORMAT == "PSPNG":
        outpath = os.path.join(tempdir, outbasename+".ps")
        shutil.copy(outpath, os.path.join(cwd,dirname))
        outpath = os.path.join(tempdir, outbasename+".png")
        shutil.copy(outpath, os.path.join(cwd,dirname))
    elif opts.OUTPUT_FORMAT == "PDFPNG":
        outpath = os.path.join(tempdir, outbasename+".pdf")
        shutil.copy(outpath, os.path.join(cwd,dirname))
        outpath = os.path.join(tempdir, outbasename+".png")
        shutil.copy(outpath, os.path.join(cwd,dirname))
    elif opts.OUTPUT_FORMAT == "EPSPNG":
        outpath = os.path.join(tempdir, outbasename+".eps")
        shutil.copy(outpath, os.path.join(cwd,dirname))
        outpath = os.path.join(tempdir, outbasename+".png")
        shutil.copy(outpath, os.path.join(cwd,dirname))
    else:
        outpath = os.path.join(tempdir, outname)
        if os.path.exists(outpath):
            shutil.copy(outpath, os.path.join(cwd,dirname))
        else:
            logging.error("No output file '%s' from processing %s" % (outname, datfile))

    ## Clean up
    if opts.NO_CLEANUP:
        logging.info('Keeping temp-files in %s' % tempdir)
    else:
        shutil.rmtree(tempdir, ignore_errors=True)


## Wrapper for a process thread which attempts to process datfiles until empty
import threading, Queue
class MkPlotThread( threading.Thread ):
    def run(self):
        global opts
        global datfiles
        global RECVD_KILL_SIGNAL
        while True:
            if RECVD_KILL_SIGNAL is not None:
                ## Empty the queue
                while not datfiles.empty():
                    dummy = datfiles.get_nowait()
                break
            try:
                datfile = datfiles.get_nowait()
                rem = datfiles.qsize()
                logging.info("Plotting %s (%d remaining)" % (datfile, rem))
                process_datfile(datfile)
            except Queue.Empty, e:
                #print "%s ending." % self.getName()
                break
            # except Exception, e:
            #     print "Error: %s" % str(e)
            #     import traceback
            #     logging.debug(traceback.format_exc())
            #     #exit(1)


####################


if __name__ == '__main__':

    ## Try to rename the process on Linux
    try:
        import ctypes
        libc = ctypes.cdll.LoadLibrary('libc.so.6')
        libc.prctl(15, 'make-plots', 0, 0, 0)
    except Exception:
        pass

    ## Try to use Psyco optimiser
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    ## Find number of (virtual) processing units
    numcores = os.sysconf('SC_NPROCESSORS_ONLN')
    if numcores is None:
        numcores = 1

    ## Parse command line options
    from optparse import OptionParser, OptionGroup
    parser = OptionParser(usage=__doc__)
    parser.add_option("-n", "-j", "--num-threads", dest="NUM_THREADS", type="int",
                      default=numcores, help="max number of threads to be used [%s]" % numcores)
    parser.add_option("--palatino", dest="OUTPUT_FONT", action="store_const", const="PALATINO", default="PALATINO",
                      help="Use Palatino as font (default).")
    parser.add_option("--cm", dest="OUTPUT_FONT", action="store_const", const="CM", default="PALATINO",
                      help="Use Computer Modern as font.")
    parser.add_option("--times", dest="OUTPUT_FONT", action="store_const", const="TIMES", default="PALATINO",
                      help="Use Times as font.")
    parser.add_option("--minion", dest="OUTPUT_FONT", action="store_const", const="MINION", default="PALATINO",
                      help="Use Adobe Minion Pro as font. Note: You need to set TEXMFHOME first.")
    parser.add_option("--helvetica", dest="OUTPUT_FONT", action="store_const", const="HELVETICA", default="PALATINO",
                      help="Use Helvetica as font.")
    parser.add_option("--ps", dest="OUTPUT_FORMAT", action="store_const", const="PS", default="PDF",
                      help="Create PostScript output (default).")
    parser.add_option("--pdf", dest="OUTPUT_FORMAT", action="store_const", const="PDF", default="PDF",
                      help="Create PDF output.")
    parser.add_option("--eps", dest="OUTPUT_FORMAT", action="store_const", const="EPS", default="PDF",
                      help="Create Encapsulated PostScript output.")
    parser.add_option("--png", dest="OUTPUT_FORMAT", action="store_const", const="PNG", default="PDF",
                     help="Create PNG output.")
    parser.add_option("--pspng", dest="OUTPUT_FORMAT", action="store_const", const="PSPNG", default="PDF",
                     help="Create PS and PNG output.")
    parser.add_option("--pdfpng", dest="OUTPUT_FORMAT", action="store_const", const="PDFPNG", default="PDF",
                     help="Create PDF and PNG output.")
    parser.add_option("--epspng", dest="OUTPUT_FORMAT", action="store_const", const="EPSPNG", default="PDF",
                     help="Create EPS and PNG output.")
    parser.add_option("--tex", dest="OUTPUT_FORMAT", action="store_const", const="TEX", default="PDF",
                      help="Create TeX/LaTeX output.")
    parser.add_option("--no-cleanup", dest="NO_CLEANUP", action="store_true", default=False,
                      help="Keep temporary directory and print its filename.")
    parser.add_option("--full-range", dest="FULL_RANGE", action="store_true", default=False,
                      help="Plot full y range in LogY plots.")
    parser.add_option("-c", "--config", dest="CONFIGFILES", action="append", default=None,
                      help="Plot config file to be used. Overrides internal config blocks.")
    verbgroup = OptionGroup(parser, "Verbosity control")
    verbgroup.add_option("-v", "--verbose", action="store_const", const=logging.DEBUG, dest="LOGLEVEL",
                         default=logging.INFO, help="print debug (very verbose) messages")
    verbgroup.add_option("-q", "--quiet", action="store_const", const=logging.WARNING, dest="LOGLEVEL",
                         default=logging.INFO, help="be very quiet")
    parser.add_option_group(verbgroup)

    opts, args = parser.parse_args()
    logging.basicConfig(level=opts.LOGLEVEL, format="%(message)s")


    ## Check for no args
    if len(args) == 0:
        logging.error(parser.get_usage())
        sys.exit(2)


    ## Test for external programs (kpsewhich, latex, dvips, ps2pdf/ps2eps, and convert)
    opts.LATEXPKGS = []
    if opts.OUTPUT_FORMAT != "TEX":
        try:
            ## latex
            if not have_cmd("latex"):
                logging.error("ERROR: required program 'latex' could not be found. Exiting...")
                sys.exit(1)
            ## dvips
            if not have_cmd("dvips"):
                logging.error("ERROR: required program 'dvips' could not be found. Exiting...")
                sys.exit(1)

            ## ps2pdf / ps2eps
            if "PDF" in opts.OUTPUT_FORMAT:
                if not have_cmd("ps2pdf"):
                    logging.error("ERROR: required program 'ps2pdf' (for PDF output) could not be found. Exiting...")
                    sys.exit(1)
            elif "EPS" in opts.OUTPUT_FORMAT:
                if not have_cmd("ps2eps"):
                    logging.error("ERROR: required program 'ps2eps' (for EPS output) could not be found. Exiting...")
                    sys.exit(1)
            ## PNG output converter
            if "PNG" in opts.OUTPUT_FORMAT:
                if not have_cmd("convert"):
                    logging.error("ERROR: required program 'convert' (for PNG output) could not be found. Exiting...")
                    sys.exit(1)

            ## kpsewhich: required for LaTeX package testing
            if not have_cmd("kpsewhich"):
                logging.warning("WARNING: required program 'kpsewhich' (for LaTeX package checks) could not be found")
            else:
                ## Check minion font
                if opts.OUTPUT_FONT == "MINION":
                    p = subprocess.Popen(["kpsewhich", "minion.sty"], stdout=subprocess.PIPE)
                    p.wait()
                    if p.returncode != 0:
                        logging.warning('Warning: Using "--minion" requires minion.sty to be installed. Ignoring it.')
                        opts.OUTPUT_FONT = "PALATINO"

                ## Check for HEP LaTeX packages
                # TODO: remove HEP-specifics/non-standards?
                for pkg in ["hepnicenames", "hepunits", "underscore"]:
                    p = subprocess.Popen(["kpsewhich", "%s.sty" % pkg], stdout=subprocess.PIPE)
                    p.wait()
                    if p.returncode == 0:
                        opts.LATEXPKGS.append(pkg)

                ## Check for Palatino old style figures and small caps
                if opts.OUTPUT_FONT == "PALATINO":
                    p = subprocess.Popen(["kpsewhich", "ot1pplx.fd"], stdout=subprocess.PIPE)
                    p.wait()
                    if p.returncode == 0:
                        opts.OUTPUT_FONT = "PALATINO_OSF"
        except Exception, e:
            logging.warning("Problem while testing for external packages. I'm going to try and continue without testing, but don't hold your breath...")


    ## Fill queue
    datfiles = Queue.Queue(maxsize=-1)
    plotword = "plot"
    if len(args) > 1:
        plotword = "plots"
    logging.info("Making %d %s" % (len(args), plotword))
    for d in args:
        datfiles.put(d)

    ## Set up signal handling
    import signal
    RECVD_KILL_SIGNAL = None
    def handleKillSignal(signum, frame):
        "Declare us as having been signalled, and return to default handling behaviour"
        global RECVD_KILL_SIGNAL
        logging.critical("Signal handler called with signal " + str(signum))
        RECVD_KILL_SIGNAL = signum
        signal.signal(signum, signal.SIG_DFL)
    ## Signals to handle
    signal.signal(signal.SIGINT,  handleKillSignal)
    signal.signal(signal.SIGTERM, handleKillSignal)
    signal.signal(signal.SIGHUP,  handleKillSignal)
    signal.signal(signal.SIGUSR2, handleKillSignal)

    ## Run threads
    for threadnum in range(opts.NUM_THREADS):
        procthread = MkPlotThread()
        #procthread.daemon = True
        procthread.start()

    import time
    while not datfiles.empty() and not RECVD_KILL_SIGNAL:
        time.sleep(0.25)
