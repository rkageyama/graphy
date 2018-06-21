# import pandas as pd
# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib import gridspec
# from matplotlib.patches import Rectangle
# from matplotlib import rc
# import matplotlib.patches as mpatches
import itertools
import sys
import spectra
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
import clip_tools as ct
import ClipPlot_Functions as gpfunc
import pandas as pd
import subprocess


class Graphy():
    def __init__(self,track_files=["/Users/DarthRNA/Documents/Robin/GRAPHY_TEST/miR29_WT_Th2.bam"]):
        self.track_files = track_files
        self.color_values = ["#0080ff","#0080ff","#0080ff","#0080ff"]
        self.figwidth = 0.0
        self.figheight = 5
        self.refseqtrack = True
        self.LeftToRight = False
        self.strand = "-"
        self.colors = itertools.cycle([spectra.html(i).darken(20).hexcode for i in self.color_values])
        self.shade = itertools.cycle(self.color_values)
        self.limits = "default"
        self.bedtrack = False
        self.start = 142903034
        self.stop = 142906867
        self.staggerbed = False
        self.bigwignames = []
        self.wig_df_list = {}
        self.shade_by_bed = False
        self.output_folder = "/Users/DarthRNA/Documents/Robin/TrackImages/"
        self.geneid = "Actb"
        self.outputsuffix = ""
        self.outputformat = "pdf"
        self.dpi = 300
        self.track_names = [i.split("/")[-1] for i in self.
                            track_files]
        self.track_type = ['s' for i in track_files]
        self.axis_off = False
        self.legend = True
        self.staticaxes = True
        self.bedfile = None
        self.bedtype = None
        self.name = None
        self.chrom = "chr5"
        self.refseqid = "NM_007393"
        self.annotate_bed = False
        self.fontsize = 12
        self.scaleRPM = False

    def plot(self,**kwargs):
        '''
        Call with 
        graphy.plot(location=["chr1",100,200,"+"])
        or        
        graphy.plot(easylocation="chr3:95,659,551-95,664,280",strand="+")
        '''
        if "location" in kwargs:
            self.chrom = kwargs["location"][0]
            self.start = kwargs["location"][1]
            self.stop = kwargs["location"][2]
            self.strand = kwargs["location"][3]
            self.recall_depths()
        if "easylocation" in kwargs:
            self.chrom,self.start,self.stop = ct.easylocation(kwargs["easylocation"])
            if "strand" in kwargs:
                self.strand = kwargs["strand"]
                self.recall_depths()
            else:
                raise KeyError("Strand Required")

        self.recall_depths()

        if self.scaleRPM:
            # Checks total reads scales depths accordingly
            print "======\nNormalizing to RPM\n======"
            for n,t in enumerate(self.track_files):
                sout,serr = subprocess.Popen(("samtools", "idxstats",t),stderr=subprocess.PIPE,stdout=subprocess.PIPE).communicate()
                read_counts = pd.read_table(StringIO(sout),names=["chrom","bases","readsmapped","readsunmapped"])
                reads_mapped = read_counts.readsmapped.sum()
                factor = 1000000.0/float(reads_mapped)
                print "%s : %s" % (self.track_names[n],factor)
                self.depths[self.track_names[n]] = self.depths[self.track_names[n]]*factor
            print "\n"

        self.wig_df_list = gpfunc.get_wig_data(self.bigwigfiles,self.bigwignames,self.chrom,self.start,self.stop)
        
        gpfunc.plot(self.figwidth,
             self.figheight,
             self.refseqtrack,
             self.LeftToRight,
             self.strand,
             self.depths,
             self.colors,
             self.shade,
             self.limits,
             self.bedtrack,
             self.start,
             self.stop,
             self.staggerbed,
             self.bigwignames,
             self.wig_df_list,
             self.shade_by_bed,
             self.output_folder,
             self.geneid,
             self.outputsuffix,
             self.outputformat,
             self.dpi,
             self.track_names,
             self.axis_off,
             self.legend,
             self.staticaxes,
             self.bedfile,
             self.bedtype,
             self.name,
             self.chrom,
             self.refseqid,
             self.annotate_bed,
             self.fontsize,
             )
    
    def recall_depths(self):
        self.depths = gpfunc.get_depth_data(self.track_files,
                                     self.track_names,
                                     self.chrom,
                                     self.start,
                                     self.stop,
                                     self.strand,
                                     self.track_type)

    def set_location(self,location):
        '''
        set a location in the format chrN:100-500
        '''
        self.chrom, self.start, self.stop = ct.easylocation(location)
