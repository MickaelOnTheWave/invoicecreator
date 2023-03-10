import argparse
import calendar
import datetime
import invoicecreator
import os
import pickle

versionString = '0.2'
dataFile = 'data.txt'

def invoiceDateDisplay(date):
    return date.strftime('%d %b %Y')

def invoiceIdDisplay(id):
    return "{:04d}".format(id)
    
def invoiceValueDisplay(value):
    return "{0:.2f}".format(value)
    
def getInvoiceDate(month):
    currentDate = datetime.datetime.now()    
    monthToUse = month if month else currentDate.month
    return lastDayOfMonth(monthToUse)

def lastDayOfMonth(month):
    currentDate = datetime.datetime.now()
    lastDay = calendar.monthrange(currentDate.year, month)[1]
    targetDate = datetime.datetime(currentDate.year, month, lastDay)
    return targetDate
 

def lastDayOfCurrentMonth():
    currentDate = datetime.datetime.now()
    return lastDayOfMonth(currentDate.month)
    
def defaultFileData():
    defaultData = {
        'invoiceId' : 1,
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
    
def askForUserConfirmation(invoiceData):
    print('An invoice will be generated using the following data :')
    print('ID :', invoiceIdDisplay(invoiceData['invoiceId']))
    print('Date :', invoiceDateDisplay(invoiceData['date']))
    print('Client :', invoiceData['client'])
    print('Company :', invoiceData['company'])
    print('Value :', invoiceValueDisplay(invoiceData['value']))
    print('')
    userAnswer = input('Do you want to proceed ? (y or n)')
    return userAnswer == 'y'
    
def generateFilename(date):
    return date.strftime('%Y-%m') + ' Consulting Invoice.pdf'
    
def createInvoice(invoiceData):
    pdfFilename = generateFilename(invoiceData['date'])
    data = {'invoiceId' : invoiceIdDisplay(invoiceData['invoiceId']),
            'date' : invoiceDateDisplay(invoiceData['date']),
            'value' : invoiceValueDisplay(invoiceData['value'])
            }
    invoicecreator.createInvoicePdf('template.html', pdfFilename, data)
    return pdfFilename
    
def updateDatafile(data):
    data['invoiceId'] += 1
    print(data)
    with open(dataFile, 'wb') as fp:
        pickle.dump(data, fp)
    
def copyToMegaFolder(invoiceFile):
    print('TODO : copy file', invoiceFile, 'to MEGA folder')

def prepareEmail(invoiceFile, date):
    print('TODO : Create email to Mega with', invoiceFile, 'attached')
    
if __name__ == "__main__":
    cliArgs = createCli()
    if cliArgs.version:
        printVersionInformation()
    else:
        invoiceData = getDataFromFile(dataFile)
        invoiceData['date'] = getInvoiceDate(cliArgs.month)
        proceed = askForUserConfirmation(invoiceData)
        if proceed:
            invoiceFile = createInvoice(invoiceData)
            updateDatafile(invoiceData)
            copyToMegaFolder(invoiceFile)
            prepareEmail(invoiceFile, invoiceData['date'])
