import clip_tools as ct
from ipywidgets import interact
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import FloatSlider
from IPython.display import clear_output
import ClipPlot_Functions as fct
import ClipPlot
import os
import itertools
import spectra


file_utr3 = "/Users/DarthRNA/Documents/Robin/genomes/refseq_3utr.bed"
file_refseq = "/Users/DarthRNA/Documents/Robin/genomes/refseq_names.txt"
file_targetscan = "/Users/DarthRNA/Documents/Robin/genomes/Targetscan7_fixed.bed"
file_refgenebed = '/Users/DarthRNA/Documents/Robin/genomes/refGene.bed'

default_track_folder = "/Users/DarthRNA/Documents/Robin/GRAPHY_TEST/"

defaultloc = 'chr5:142,903,034-142,906,867'
defaultgeneid = 'Actb'
defaultrefseqid = 'NM_007393'
defaultstrand = "-"

cPlot = ClipPlot.Graphy()

bd = ct.BetweenDict(file_refgenebed)

####################################
#### WIDGET UPDATE FUNCTIONS ####
####################################


def update_by_type(*args):
    '''Update LOCATION field, after changing LOOKUPTYPE'''
    if lookuptype_widget.value == "location":
        location_widget.value = defaultloc
    if lookuptype_widget.value == "geneid":
        location_widget.value = defaultgeneid


def update_geneid(*args):
    '''Update GENEID field, after changing LOCATION'''
    if lookuptype_widget.value == "location":
        chrom,start,stop = ct.easylocation(location_widget.value)
        strand = strand_widget.value
        genelist =  list(fct.get_gene_id(chrom,start,stop,strand,bd,choice='all'))
        if len(genelist)>0:
            geneid_widget.options = genelist
        else:
            geneid_widget.options = ["None"]
    elif lookuptype_widget.value == "geneid":
        geneid_widget.options = [location_widget.value]
        geneid_widget.value = location_widget.value  

def update_refseqid(*args):
    '''Update REFSEQ field, after changing GENEID'''
    reflist =  fct.get_refseq_id(file_refseq,geneid_widget.value,choice="all")
    print reflist
    if len(reflist)>0:
        refseqid_widget.options = reflist
    else:
        refseqid_widget.options = ["None"]

def update_antisense_check(*args):
    if len(file_widget.value)==0:
        w_as_selectors.layout.display="none"
        w_antisense_check.options = []
    if len(file_widget.value)>0:
        w_as_selectors.layout.display=""
        # Add or remove from antisence_check.options
        options = w_antisense_check.options
        for i in file_widget.value:
            if not i in options:
                options.append(i)
        for i in options:
            if not i in file_widget.value:
                options.remove(i)
        w_antisense_check.options = options


####################################
############ Widgets ############
####################################


### Defaults Widget (accord) ### 
w_default_folder = widgets.Text(
    description='RnaSeq Folder',
    value=default_track_folder,
    )
w_default_folder.width="80%"
w_default_folder_valid = widgets.Valid(value=True)
hboxdefaultfolder = widgets.HBox([w_default_folder,w_default_folder_valid])
page1 = widgets.VBox(children=[hboxdefaultfolder])

accord = widgets.Accordion(children=[page1], width="80%")
accord.set_title(0, 'Defaults')


### Lookup by... Widget (lookuptype_widget) ### 
lookuptype_widget = widgets.RadioButtons(
    options={'By location':'location','By geneid (3\'UTR only)':"geneid"},
    value='location',
    description='Lookup:',
    disabled=False
)

### Location Widget (location_widget) ### 
location_widget = widgets.Text(
    value=defaultloc,
    placeholder='Type something',
    description='Location:',
    disabled=False
)

### Strand Widget (strand_widget) ### 
strand_widget = widgets.RadioButtons(
    options=['+','-'],
    value=defaultstrand,
    description='Strand:',
    disabled=False
)

### GeneID Widget (geneid_widget) ###
geneid_widget = widgets.Dropdown(
        options=[defaultgeneid],
        value=defaultgeneid,
        description='GeneID:',
        disabled=False,
        button_style='' # 'success', 'info', 'warning', 'danger' or ''
    )
### Refseq Widget (refseqid_widget) ###
refseqid_widget = widgets.Dropdown(
        options=[defaultrefseqid],
        value=defaultrefseqid,
        description='RefseqID:',
        disabled=False,
        button_style='' # 'success', 'info', 'warning', 'danger' or ''
    )

### File Select Widget (file_widget) ###
all_files = os.listdir(w_default_folder.value)
file_types = ["bam","bw"]
file_names = []
for f in all_files:
    if f.split(".")[-1] in file_types:
        file_names.append(f)
file_widget = widgets.SelectMultiple(
    options=file_names,
    disabled=False
)

### Antisense Check Widget (w_aschecktitle, w_antisense_check) ###
w_aschecktitle= widgets.HTML("Are any of these tracks antisense?")
w_antisense_check = widgets.SelectMultiple(
    options=[]
)
w_as_selectors = widgets.VBox([w_aschecktitle,w_antisense_check])
w_as_selectors.layout.display="none"



##############################
### Style Selector Widgets ###
##############################

buttonwidth="15%"
buttonstyle='info'
### w_labels ###
w_labels = widgets.ToggleButton(
    value=False,
    description='BedLabels',
    button_style=buttonstyle, # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Label each element of a bedtrack',
    width=buttonwidth,
)
### w_invert ###
w_invert = widgets.ToggleButton(
    value=False,
    description='Invert(!)',
    button_style=buttonstyle, # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Always display genes from left to right regardless of strand. Not working well",
    width=buttonwidth,

)
### w_legend ###
w_legend = widgets.ToggleButton(
    value=True,
    description='Legend',
    button_style=buttonstyle, # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Show Legend for Seq-Tracks",
    width=buttonwidth,

)
### w_stagger ###
w_stagger = widgets.ToggleButton(
    value=False,
    description='Stagger Bedtracks',
    button_style=buttonstyle, # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Stagger Bedtracks",
    width=buttonwidth,
)
### w_refseq ###
w_refseq = widgets.ToggleButton(
    value=True,
    description='Show Refseq',
    button_style=buttonstyle, # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Refseq track?",
    width=buttonwidth,
)
### w_shadeBed ###
w_shadeBed = widgets.ToggleButton(
    value=False,
    description='Shade Bed',
    button_style=buttonstyle, # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Highlight bedtrack regions",
    width=buttonwidth,
)
### w_staticaxes ###
w_staticaxes = widgets.ToggleButton(
    value=True,
    description='Autoscale',
    button_style=buttonstyle, # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Scale the rnaseq tracks?",
    width=buttonwidth,
)
### w_boundingbox ###
w_boundingbox = widgets.ToggleButton(
    value=True,
    description='Show BoundingBox',
    button_style=buttonstyle, # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Show axes and border box?",
    width=buttonwidth,
)
### w_rpm ###
w_rpm = widgets.ToggleButton(
    value=False,
    description='Scale to RPM',
    button_style=buttonstyle, # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Scales to RPM, can be slow",
    width=buttonwidth,
)
### w_xscale ###
formattingwidth ="20%"
w_xscale = widgets.FloatText(
    description="x scale (inches)",
    placeholder="Int",
    tooltip="can enter 0 to autoscale",
    width=formattingwidth,
)
### w_fontsize ###
w_fontsize = widgets.FloatText(
    description="Font Size",
    placeholder="Int",
    tooltip="can enter 0 to autoscale",
    value=12,
    width=formattingwidth,
)
### w_dpi ###
w_dpi = widgets.FloatText(
    description="DPI",
    placeholder="300",
    value="300",
    width=formattingwidth,
)
### w_fileformat ###
w_fileformat = widgets.Text(
    description="File Format",
    placeholder="Pdf,Svg,PNG",
    value="pdf",
    width=formattingwidth,
)
### w_filesuffix ###
w_filesuffix = widgets.Text(
    description="File Suffix",
    placeholder="None",
    value="",
    width=formattingwidth,
)
### w_outputfolder ###
w_outputfolder = widgets.Text(
    value="/Users/DarthRNA/Documents/Robin/TrackImages/",
    description="Output Folder",
    width="80%",
)
w_outputfolder_valid = widgets.Valid(value=True)
hboxoutputfolder = widgets.HBox([w_outputfolder,w_outputfolder_valid])
def output_folder_check(*args):
    if os.path.isdir(w_outputfolder.value) and w_outputfolder.value[-1] == "/" :
        w_outputfolder_valid.value=True
    else:
        w_outputfolder_valid.value=False
w_outputfolder.observe(output_folder_check,'value')

### Combine Style Selectors)
selectors1 = widgets.HBox([w_labels,
                           w_invert,
                           w_legend,
                           w_stagger,
                           w_refseq,
                           w_shadeBed,
                           w_staticaxes,
                           w_boundingbox,
                           w_rpm,
                          ])
selectors2 = widgets.HBox([w_xscale,
                           w_fontsize,
                           w_dpi,
                           w_fileformat,
                           w_filesuffix,
                          ])


### Color Selectors (selectors_color) ###
w_cp1=widgets.ColorPicker(value="#0080ff",width="100px",concise=False)
w_cp2=widgets.ColorPicker(value="#ff0000",width="100px",concise=False)
w_cp3=widgets.ColorPicker(value="#00ff00",width="100px",concise=False)
w_cp4=widgets.ColorPicker(value="#800080",width="100px",concise=False)

selectors_color = widgets.HBox([w_cp1,w_cp2,w_cp3,w_cp4])



### THE BUTTON ###
button = widgets.Button(description="Graph!")



lookuptype_widget.observe(update_by_type,'value')
location_widget.observe(update_geneid, 'value')
strand_widget.observe(update_geneid, 'value')
geneid_widget.observe(update_refseqid,'value')
file_widget.observe(update_antisense_check,'value')


display(accord)
display(widgets.HTML(value="<h3>Select Region</h3>"))
display(lookuptype_widget)
display(location_widget)
display(strand_widget)
display(geneid_widget)
display(refseqid_widget)
display(widgets.HTML(value="Alignments to Use"))
display(file_widget)
display(w_as_selectors)
display(widgets.HTML(value="<h3>Formatting</h3>"))
display(selectors1)
display(widgets.HTML(value="<h4>Color Picker</h4>"))
display(selectors_color)
display(widgets.HTML(value="<h4>Output Format</h4>"))
display(selectors2)
display(hboxoutputfolder)
display(widgets.HTML(value="<br><br>"))
accord.selected_index=1 #starts the accordian closed.
display(button)



def on_button_clicked(b):
    clear_output()

    ## SANITY CHECKS ###
    if not len(file_widget.value)>0:
        print "ERROR: It's required to pick a .bam alignment!"
        return
    #####################

    if lookuptype_widget.value=="location":
        cPlot.chrom,cPlot.start,cPlot.stop = ct.easylocation(location_widget.value)
        cPlot.strand = strand_widget.value
    elif lookuptype_widget.value=="geneid":
        df_refseq_3utr = pd.read_table("/Users/DarthRNA/Documents/Robin/genomes/mm10_refseq_3utr.bed",names=['chrom','start','stop','name','score','strand'])
        df_refseq_3utr.name = ["_".join(x.split("_")[0:2]) for x in df_refseq_3utr.name]
        df_refseq_3utr = df_refseq_3utr.drop_duplicates("name")
        df_refseq_3utr = df_refseq_3utr.set_index("name")
        cPlot.chrom, cPlot.start, cPlot.stop, foo, cPlot.strand = df_refseq_3utr.loc[refseqid_widget.value]

    track_type=[]
    for t in w_antisense_check.options:
        if t in w_antisense_check.value:
            track_type.append("as")
        else:
            track_type.append("s")
    cPlot.geneid= geneid_widget.value
    cPlot.refseqid = refseqid_widget.value
    cPlot.track_names = [f for f in w_antisense_check.options if f.split(".")[-1]=="bam"]
    cPlot.bigwignames = [f for f in w_antisense_check.options if f.split(".")[-1]=="bw"]
    cPlot.track_files = [w_default_folder.value + f for f in cPlot.track_names]
    cPlot.bigwigfiles = [w_default_folder.value + f for f in cPlot.bigwignames]
    cPlot.track_type = track_type
    
    cPlot.outputformat = w_fileformat.value
    cPlot.figwidth = w_xscale.value
    cPlot.dpi = w_dpi.value
    cPlot.LeftToRight = w_invert.value
    cPlot.annotate_bed = w_labels.value
    cPlot.staggerbed = w_stagger.value
    cPlot.refseqtrack = w_refseq.value
    cPlot.shade_by_bed = w_shadeBed.value
    cPlot.outputsuffix = w_filesuffix.value
    cPlot.staticaxes = w_staticaxes.value
    cPlot.axis_off= not w_boundingbox.value
    cPlot.fontsize = w_fontsize.value
    cPlot.legend = w_legend.value
    cPlot.figheight = 2.5*len(w_antisense_check.options)
    cPlot.output_folder = w_outputfolder.value
    cPlot.scaleRPM = w_rpm.value

    color_values = [w_cp1.value,w_cp2.value,w_cp3.value]
    cPlot.shade = itertools.cycle(color_values)
    cPlot.colors = itertools.cycle([spectra.html(i).darken(20).hexcode for i in color_values])
    cPlot.plot()

button.on_click(on_button_clicked)
