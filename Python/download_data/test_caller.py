from global_SubX_data import global_SubX_data

url = "http://iridl.ldeo.columbia.edu/SOURCES/.Models/.SubX/"
outdir = '/gpfs/data1/cmongp/pranav/SampleData'
ftype="hindcast"
mod="CCSM4" 
inst="RSMAS"
var="zg" 
plev=500
ens=1.0
fen = 1.0



global_SubX_data(url, outdir, ftype, mod, inst, var, plev, ens, fen)

