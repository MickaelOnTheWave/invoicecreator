import argparse
import os
from pyhtml2pdf import converter

versionString = '0.1.0'
inputFilename = 'template.html'
outputFilename = 'output.pdf'

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
    
if __name__ == "__main__":
    cliArgs = createCli()
    if cliArgs.version:
        printVersionInformation()
    else:
        path = os.path.abspath(inputFilename)
        converter.convert(f'file:///{path}', outputFilename)
  