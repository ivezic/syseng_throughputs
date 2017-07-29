from  eTraveler.clientAPI.connection import Connection
from findCCD import findCCD
import argparse
import os

class find_EOT02_QE():

    def get(self, htype = None, db = None, server = None, appSuffix = None):

        if server == 'Prod': pS = True
        else: pS = False
        connect = Connection(operator='richard', db=db, exp='LSST-CAMERA', prodServer=pS, appSuffix='-'+appSuffix)


        returnData  = connect.getResultsJH(htype=args.htype, stepName = 'qe_offline', travelerName='SR-EOT-02')

        ccd_list = {}


        for ccd in returnData:

            expDict = returnData[ccd]

            try:
                stepDict = expDict['steps']['qe_offline']
                run = expDict['runNumber']
                fCCD = findCCD(FType='fits', testName='qe_offline', sensorId=ccd, run=run, site='SLAC')
                files = fCCD.find()
                ccd_list[ccd] = files

            except:
                pass
        return ccd_list

if __name__ == "__main__":

    ## Command line arguments
    parser = argparse.ArgumentParser(
        description='Find archived data in the LSST  data Catalog. These include CCD test stand and vendor data files.')

    ##   The following are 'convenience options' which could also be specified in the filter string
    parser.add_argument('-t', '--htype', default=None, help="hardware type (default=%(default)s)")
    parser.add_argument('-d', '--db', default='Prod', help="eT database (default=%(default)s)")
    parser.add_argument('-e', '--eTserver', default='Dev', help="eTraveler server (default=%(default)s)")
    parser.add_argument('--appSuffix', '--appSuffix', default='jrb',
                        help="eTraveler server (default=%(default)s)")
    args = parser.parse_args()

    f_QE = find_EOT02_QE()
    ccd_list = f_QE.get(htype=args.htype, db = args.db, server= args.eTserver, appSuffix = args.appSuffix)

    print 'Type ', args.htype,  len(ccd_list), 'total. Found ', len(ccd_list), 'with SR-EOT-02', '\n \n'
    for key in ccd_list:
      print ccd_list[key],'\n \n'
      print 'copying'+ str(ccd_list[key][0])+' /u/ek/ritz','\n'
      os.system('cp '+ str(ccd_list[key][0])+' /u/ek/ritz')    
