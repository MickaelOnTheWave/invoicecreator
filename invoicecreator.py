import argparse
from xml.etree import ElementTree as ET

versionString = '0.1.0'
outputFilename = 'invoice.txt'

def createCli():
    parser = argparse.ArgumentParser(prog = 'InvoiceCreator',
                    description = 'Creates and manages Invoices',
                    epilog = 'Copyright @ 2023 Guimarães Tecnologia')
    parser.add_argument('-v', '--version', dest='version')
    parser.add_argument('-d', '--date', dest='date', help='Date of the invoice')
    parser.add_argument('--value', dest='invoiceValue', help='Value of the invoice')
    return parser.parse_args()
    
def printVersionInformation():
    print('InvoiceCreator v{}'.format(versionString))
    
def generateInvoiceContent(date, value):
    html = ET.html('html')
    body = ET.body('body')
    html.append(body)
    return html

if __name__ == "__main__":
    cliArgs = createCli()
    if cliArgs.version:
        printVersionInformation()
        
    invoiceXml = generateInvoiceContent(cliArgs.date, cliArgs.invoiceValue)
    ET.ElementTree(invoiceXml).write(outputFilename, method='html')
  