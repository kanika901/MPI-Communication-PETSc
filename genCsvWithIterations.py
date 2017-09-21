#!/usr/bin/env python

#to run: 
#python genCsvWithIterations.py /disks/large/shared/soft/lighthouse-data/drivencavity/results2


import glob, os, sys
from allsolvers import *

data = {}
failed = {}
def processData(fname,newlines,perfinfo,kspFinalResNorm):
    global data
    print "Processing",fname
    if newlines and fname and not os.path.exists(fname): 
        with open(fname, "w") as text_file:
            text_file.write(''.join(newlines))
    # Name looks like this: ex19.12321508.p12288.r1.log
    fnameparts = fname.split('.')
    solverid = fnameparts[1]
    nprocs = fnameparts[2].strip('p')
    config = '_'.join(fnameparts[3:-1])

    if kspFinalResNorm >= 0.1:
        if config not in failed.keys(): failed[config] = {}
        if nprocs not in failed[config].keys(): failed[config][nprocs] = {}
        failed[config][nprocs][solverid] = perfinfo
    else:
        if config not in data.keys(): data[config] = {}
        if nprocs not in data[config].keys(): data[config][nprocs] = {}
        data[config][nprocs][solverid] = perfinfo
    pass

def processLine(l):
    #
    #------------------------------------------------------------------------------------------------------------------------
    #Event                Count      Time (sec)     Flops                             --- Global ---  --- Stage ---   Total
    #                   Max Ratio  Max     Ratio   Max  Ratio  Mess   Avg len Reduct  %T %F %M %L %R  %T %F %M %L %R Mflop/s
    #------------------------------------------------------------------------------------------------------------------------
    #KSPSolve               1 1.0 6.2000e+01 1.0 3.77e+10 1.0 3.4e+06 3.3e+03 3.0e+04100100100100100 100100100100100 57852
    f = l.split()

    maxtime = f[3][:f[3].find('e-')+4]

    #return {'name':f[0],'count':f[1],'maxtime':maxtime,'avg time/solve':'%e'%(float(maxtime)/float(f[1])),'maxflops':f[5],'messages':f[7],'avgmsglen':f[8],
    #        'reductions':f[9][:7],'mflop/s':f[-1]}
    return (['name','count','maxtime','avg time/solve',                'maxflops','messages','avgmsglen','reductions','max mflop/s'],
           [f[0],   f[1],   maxtime, '%e'%(float(maxtime)/float(f[1])),f[5],     f[7],      f[8],       f[9][:7],     f[-1]])
    
def getCSV(thedata, noOfIterations, fname):
    csvlines = []
    buf = ''
    configuration = fname.split('.')[3] + '_' + fname.split('.')[4]
    for conf,pdata in thedata.items():
      for nproc,v in pdata.items():
        for solverid,vv in v.items():
            for function in vv.values():
                    if (function[0] == 'KSPSolve' and conf == configuration and nproc == fname.split('.')[2].split('p')[1] and solverid == fname.split('.')[1]):
                        csvlines.append(str(conf) + ',' + str(nproc) + ',' + str(solverid) + ',' + solvers[solverid] + ',' + ','.join(function) + ',' + noOfIterations[fname] + '\n')

    buf += ''.join(csvlines)
    #buf +=  '\n'.join(csvlines)
    return buf

if __name__ == "__main__":
    if len(sys.argv)>1:
        files = glob.glob(sys.argv[1] + "/*.log")
    else:
        files = glob.glob("*.log")
    keys = []
    noOfIterations = {}

    for f in files:
        lines = open(f,'r').readlines()
        newlines = []
        fname = os.path.basename(f)
        getdata = False
        fail = False
        kspFinalResNorm=1000
        tmpdata = {}
        for l in lines:
            newlines.append(l)
            if l.startswith('Number of SNES iterations'):
                noOfIterations[f] = l.split()[-1]
            if l.startswith('KSP final norm of residual'): 
                try: kspFinalResNorm = float(l.split()[-1])
                except: pass 
            if l.startswith('Number of SNES iterations = 0'): fail = True
            if l.startswith('SNESSolve') and not fail: getdata = True
            if getdata: 
                func = l.split()[0]
                keys,tmpdata[func] = processLine(l)
            if l.startswith('PCApply') and getdata: 
                processData(fname,newlines,tmpdata,kspFinalResNorm)
                getdata = False
                kspFinalResNorm=1000
                tmpdata = {}
                break

        #processData(fname,newlines,tmpdata)

    f = open("edison-ex19-kspsolve_v5.csv","w")
    f.write('config,nprocs,solverid,solvername,' + ','.join(keys) + ',' + 'no. of iterations' + '\n') #setting csv header
    for f1 in files:
        #f.write('\n')
        f.write(getCSV(data, noOfIterations, f1))
    f.close()

    # f = open("edison-ex19-kspsolve-bad_v5.csv","w")
    # f.write('config,nprocs,solverid,solvername,' + ','.join(keys) + ',' + 'no. of iterations' + '\n') #setting csv header
    # for f1 in files:
    # f.write(getCSV(failed, noOfIterations))
    # f.close()
    


