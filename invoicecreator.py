import argparse
import os
from pyhtml2pdf import converter

versionString = '0.2.1'
inputFilename = 'template.html'
outputFilename = 'output.pdf'

def createCli():
    parser = argparse.ArgumentParser(prog = 'InvoiceCreator',
                    description = 'Creates and manages Invoices',
                    epilog = 'Copyright @ 2023 Guimarães Tecnologia')
    parser.add_argument('-v', '--version', dest='version')
    parser.add_argument('-d', '--date', dest='date', help='Date of the invoice')
    parser.add_argument('--value', dest='invoiceValue', help='Value of the invoice')
    parser.add_argument('-i', '--id', dest='id', help='Id of the invoice')
    return parser.parse_args()
    
def printVersionInformation():
    print('InvoiceCreator v{}'.format(versionString))
    
def createFilledTemplate(inFile, outFile, data):
    inputF = open(inFile, 'r')
    inputContents = inputF.read()
    inputF.close()
    
    outputContents = inputContents.format(data['invoiceId'], data['date'], data['value'])
    
    outputF = open(outFile, 'w')
    outputF.write(outputContents)
    outputF.close()
    
def createData(cliArgs):
    data = {}
    data['invoiceId'] = cliArgs.id if cliArgs.id else 'undef'
    data['date'] = cliArgs.date if cliArgs.date else 'undef'
    data['value'] = cliArgs.invoiceValue if cliArgs.invoiceValue else '4166.00'
    return data
    
def createInvoicePdf(templateFile, outputFilename, invoiceData):
    intermediateFilename = 'template-filled.html'
    createFilledTemplate(templateFile, intermediateFilename, invoiceData)
    path = os.path.abspath(intermediateFilename)
    converter.convert(f'file:///{path}', outputFilename)
    
if __name__ == "__main__":
    cliArgs = createCli()
    if cliArgs.version:
        printVersionInformation()
    else:
        data = createData(cliArgs)
        createInvoicePdf(inputFilename, outputFilename, data)
