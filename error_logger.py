from datetime import datetime

def logError(error = '', url = ''):
    print('======> ERROR (' + datetime.now().strftime('%d-%b-%y %T') + ') <====== \n\n')
    print('       >> URL >> ' + url)
    print('\n       >> Error >> ' + error)
    print('\n\n======> ERROR END <======\n')
    
    with open('ERROR_LOGS.log', 'a') as fh:
        fh.write('======> ERROR (' + datetime.now().strftime('%d-%b-%y %T') + ') <====== \n\n')
        fh.write('       >> URL >> ' + url)
        fh.write('\n       >> Error >> ' + error)
        fh.write('\n\n======> ERROR END <======\n')
