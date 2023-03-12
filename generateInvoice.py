import argparse
import calendar
import datetime
import invoicecreator
import os
import pickle

versionString = '0.1'
dataFile = 'data.txt'

class InvoiceData:
    def __init__(self, invoiceDate, fileData):
        self.id = fileData['id']
        self.date = invoiceDate
        self.client = fileData['client']
        self.company = fileData['company']
        self.value = fileData['value']

def getInvoiceDate(month):
    currentDate = datetime.datetime.now()
    if month:
        currentDate.setMonth(month)
    return currentDate
    
def lastDayOfCurrentMonth():
    currentDate = datetime.datetime.now()
    lastDay = calendar.monthrange(currentDate.year, currentDate.month)[1]
    targetDate = datetime.datetime(currentDate.year, currentDate.month, lastDay)
    return targetDate.strftime('%d %b %Y')
    
def defaultFileData():
    defaultData = {
        'id' : '0001',
        'date' : lastDayOfCurrentMonth(),
        'client' : 'Mega',
        'company' : 'Guimarães Tecnologia',
        'value' : 4166
        }
    return defaultData
    
def getDataFromFile(dataFile):
    if os.path.isfile(dataFile):
        with open(dataFile, 'rb') as fp:
            fileData = pickle.load(fp)
            print(fileData)
            return fileData
    return defaultFileData()

def createCli():
    parser = argparse.ArgumentParser(prog = 'InvoiceCreator',
                    description = 'Creates and manages Invoices with prefilled data',
                    epilog = 'Copyright @ 2023 Guimarães Tecnologia')
    parser.add_argument('-v', '--version', dest='version')
    parser.add_argument('--month', dest='month', help='Month to generate Invoice for. If not specified, uses current month.')
    return parser.parse_args()
    
def printVersionInformation():
    print('InvoiceAutoGenerator v{}'.format(versionString))
    
if __name__ == "__main__":
    cliArgs = createCli()
    if cliArgs.version:
        printVersionInformation()
    else:
        invoiceDate = getInvoiceDate(cliArgs.month)
        fileData = getDataFromFile(dataFile)
        invoiceData = InvoiceData(invoiceDate, fileData)
        proceed = askForUserConfirmation(invoiceData)
        if proceed:
            invoiceFile = createInvoice(invoiceData)
            copyToMegaFolder(invoiceFile)
            prepareEmail(invoiceFile, invoiceData.date)
