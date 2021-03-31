###
# A small script to rename invoices in date order - requires tika and datefinder
###

from tika import parser
from datetime import datetime
import datefinder
import re
import os
from copy import copy

# can be implemented in future to prevent incorrect year using now.year, currently unnecessary
# now = datetime.now()

# take input to invoice directory
month_path = os.path.join(str(input("Copy the full path of the month's invoices and paste it here:")), '')

# print list of vendors
print([i for i in os.listdir(month_path)])

# initialise a list for failed vendors
fail_list = []


# text pdf checker function
def text_checker(file):
    text_test = parser.from_file(file)
    if text_test == "" or file.lower().startswith('._'):
        return False
    else:
        return True


for vendor in os.listdir(month_path):
    vendor_date_list = []  # setup for date ordering invoices
    for invoice in os.listdir(month_path + vendor):
        # go through every invoice per vendor and parse the pdf to text
        # skip statements and non-pdfs
        if invoice.lower().endswith('.pdf') and 'statement' not in invoice.lower() \
                and text_checker(os.path.join(month_path + vendor, '') + str(invoice)):
            raw = parser.from_file(os.path.join(month_path + vendor, '') + str(invoice))

            # known methods to find dates via regex if there the text is in a string
            if isinstance(raw['content'], str):
                matches_224_slash = re.findall(r'\d{2}/\d{2}/\d{4}', raw['content'])
                matches_222_slash = re.findall(r'\d{2}/\d{2}/\d{2}', raw['content'])
                matches_224_dash = re.findall(r'\d{2}-\d{2}-\d{4}', raw['content'])
                matches_222_dash = re.findall(r'\d{2}-\d{2}-\d{2}', raw['content'])
                matches_222_dot = re.findall(r'\d{2}.\d{2}.\d{2}', raw['content'])
                matches_224_dot = re.findall(r'\d{2}.\d{2}.\d{4}', raw['content'])
                matches_232_space = re.findall(r'\d{2}\s\w{3}\s\d{2}', raw['content'])
                matches_234_space = re.findall(r'\d{2}\s\w{3}\s\d{4}', raw['content'])

                # match methods to matches
                match_method_list = [(matches_222_dash, '%d-%m-%y'), (matches_224_dash, '%d-%m-%Y'),
                                     (matches_222_slash, '%d/%m/%y'), (matches_224_slash, '%d/%m/%Y'),
                                     (matches_222_dot, '%d.%m.%y'), (matches_224_dot, '%d.%m.%Y'),
                                     (matches_232_space, '%d %b %y'), (matches_234_space, '%d %b %Y')]

                # generate list of empty sublists for every method's detections
                date_sub_list = []
                for i in range(len(match_method_list)):
                    date_sub_list.append([])

                # TODO: get datefinder to stop spitting out errors in a try-except loop
                # date_sub_list_checker = copy(date_sub_list)
                # if date_sub_list == date_sub_list_checker:
                #     try:
                #         date_sub_list[-1] = datefinder.find_dates(raw['content'],strict=True)
                #     except:
                #         pass

                # for loop to go through each of the methods and try to convert the date string into a datetime object
                for method in match_method_list:
                    for match in method[0]:
                        # try method used here to filter out false detections (e.g. sort codes)
                        try:
                            date_sub_list[match_method_list.index(method)].append(
                                datetime.strptime(match, method[1]).date())
                        except:
                            pass

                # flatten and sort the date list
                date_list = [i for j in date_sub_list for i in j]
                date_list.sort()

                # if the list is not empty, add the invoice name and earliest date in the invoice to the vendor date list
                if date_list != []:
                    vendor_date_list.append(
                        (invoice, date_list[0]))  # earliest entry is most likely to be the invoice date

    # sort by date attached to invoice
    vendor_date_list.sort(key=lambda tup: tup[1])

    # initialise file numbering scheme
    file_number = 1

    # go through the vendor date list if it is not empty (this prevents renaming errors)
    if vendor_date_list != []:
        for file in vendor_date_list:
            # rename command use padded 2-digit values and a hyphen
            os.rename(os.path.join(month_path + vendor, '') + str(file[0]),
                      os.path.join(month_path + vendor, '') + str(file_number).zfill(2) + ' - ' + str(file[0]))
            file_number += 1
    else:
        fail_list.append(vendor)

if fail_list == []:
    print('All directories renumbered!')
else:
    print('The following directories have failed: ' + str(fail_list))
