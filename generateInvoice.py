import argparse
import calendar
import datetime
import invoicecreator
import os
import pickle

versionString = '0.1'
dataFile = 'data.txt'

class InvoiceData:
    def __init__(self, fileData):
        self.id = fileData['id']
        self.date = fileData['date']
        self.client = fileData['client']
        self.company = fileData['company']
        self.value = fileData['value']

def getInvoiceDate(month):
    currentDate = datetime.datetime.now()    
    monthToUse = month if month else currentDate.month
    return lastDayOfMonth(monthToUse)

def lastDayOfMonth(month):
    currentDate = datetime.datetime.now()
    lastDay = calendar.monthrange(currentDate.year, month)[1]
    targetDate = datetime.datetime(currentDate.year, month, lastDay)
    return targetDate
  
def invoiceDisplay(date):
    return date.strftime('%d %b %Y')

def lastDayOfCurrentMonth():
    currentDate = datetime.datetime.now()
    return lastDayOfMonth(currentDate.month)
    
def defaultFileData():
    defaultData = {
        'id' : '0001',
        'date' : lastDayOfCurrentMonth(),
        'client' : 'Mega',
        'company' : 'Guimarães Tecnologia',
        'value' : '4166.00'
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
    
def askForUserConfirmation(invoiceData):
    print('An invoice will be generated using the following data :')
    print('ID :', invoiceData.id)
    print('Date :', invoiceDisplay(invoiceData.date))
    print('Client :', invoiceData.client)
    print('Company :', invoiceData.company)
    print('Value :', invoiceData.value)
    print('')
    userAnswer = input('Do you want to proceed ? (y or n)')
    return userAnswer == 'y'
    
def generateFilename(date):
    return date.strftime('%Y-%m') + ' Consulting Invoice.pdf'
    
def createInvoice(invoiceData):
    pdfFilename = generateFilename(invoiceData.date)
    data = {'invoiceId' : invoiceData.id,
            'date' : invoiceDisplay(invoiceData.date),
            'value' : invoiceData.value}
    invoicecreator.createInvoicePdf('template.html', pdfFilename, data)
    return pdfFilename
    
if __name__ == "__main__":
    cliArgs = createCli()
    if cliArgs.version:
        printVersionInformation()
    else:
        fileData = getDataFromFile(dataFile)
        fileData['date'] = getInvoiceDate(cliArgs.month)
        invoiceData = InvoiceData(fileData)
        proceed = askForUserConfirmation(invoiceData)
        if proceed:
            invoiceFile = createInvoice(invoiceData)
            copyToMegaFolder(invoiceFile)
            prepareEmail(invoiceFile, invoiceData.date)
