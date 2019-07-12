import os
import glob
import xarray as xr
import pandas as pd
import numpy as np


def global_SubX_data(url, outdir, ftype, mod, inst, var, plev, ens, fen):
	inFname = url+'.'+inst+'/.'+mod+'/.'+ftype+'/.'+var+'/dods'

	remote_data = xr.open_dataarray(inFname)
	if len(remote_data.dims) == 6:
		da = remote_data.sel(P=plev, M=ens)
	if len(remote_data.dims) == 5:
		da = remote_data.sel(M=ens)

	# For some models the ensembles start at 0
	esave = ens
	if fen == 0.0:
		esave = esave + 1
		da.M.values = da.M.values + 1

	outdir += ftype+'/'+mod+'/'+var+'/'+str(plev)+'/daily/full/'
	if not os.path.isdir(outdir):
		os.makedirs(outdir)

	# Check if any files have been created so they are not downloaded again
	filescreated = glob.glob(outdir+'*.e'+str(int(esave))+'.nc')
	nfilescreated = len(filescreated)
	if nfilescreated != 0:
		filescreated.sort()
		# Remove last file created incase stopped while saving
		_lastfile = filescreated[-1]
		os.unlink(_lastfile)
		
		# Find the date and index of the last created file
		# Split the string by / and get the first 8 chars
		_lastdate = _lastfile.split('/')[-1][0:8]
		_lastyear = _lastdate[0:4]
		_lastmonth = _lastdate[4:6]
		_lastday = _lastdate[6:8]


		ts = pd.Timestamp(_lastyear+'-'+_lastmonth+'-'+_lastday+' 00:00:00')
		# Find the index of this in da.S
		datesdf = da.S.to_dataframe()
		_icstart = datesdf.index.get_loc(ts)
	else:
		_icstart = 0

	da_S_len = len(da.S.values)
	for ic in range(_icstart, da_S_len):
		# Check if data exists for this start date otherwise skip
		da2 = da.sel(S=da.S.values[ic])
		if not np.all(np.isnan(da2)):
			# Convert to a pandas.Timestamp to get year, month, data
			date = pd.Timestamp(da.S.values[ic])
			year = str(date.year)
			# Use zfill to pad with 0
			month = str(date.month).zfill(2)
			day = str(date.day).zfill(2)

			# Out file name
			ofname = year+month+day+'.e'+str(int(esave))+'.nc'

			# Data often finishes before end of file
			if len(remote_data.dims) == 6:
				try:
					da2 = da2.expand_dims('S').expand_dims('M').expand_dims('P')
				except IndexError:
					exit('All data likely downloaded. You can check '+\
						inFname[:-4]+'#views to see if it can generate an image.')
			else:
				try:
					da2 = da2.expand_dims('S').expand_dims('M')
				except IndexError:
					exit('All data likely downloaded. You can check '+\
						inFname[:-4]+'#views to see if it can generate an image.')
			# Save file
			da2.to_netcdf(outdir+ofname)