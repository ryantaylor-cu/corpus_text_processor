#!/usr/bin/env python3

# Base imports
import os
import argparse
import time
from tabulate import tabulate
from multiprocessing import Pool
from functools import partial

# The following are the available custom processors.
from processors import convert_to_plaintext
from processors import encode_to_utf8
from processors import standardize_characters
from processors import remove_pdf_metadata

def get_cmdline_arguments():
    parser = argparse.ArgumentParser(description='command-line Corpus Text Processor')
    parser.add_argument('SOURCE', help='folder to process')
    parser.add_argument('DESTINATION', help='save files to this folder')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--convert-to-plaintext', action='store_true')
    group.add_argument('-e', '--encode-utf8', action='store_true')
    group.add_argument('-s', '--standardize-characters', action='store_true')
    group.add_argument('-r', '--remove-metadata', action='store_true')
    parser.add_argument('-p', '--parallel', action='store_true',
                        help='Run code on multiple cores (faster but needs more RAM)')
    args = parser.parse_args()
    # Convert arguments to the format used by GUI version of Corpus Text Processor
    values = {'source': args.SOURCE,
              'destination':  args.DESTINATION,
              'convertToPlaintext': args.convert_to_plaintext,
              'encodeUtf8': args.encode_utf8,
              'standardizeCharacters': args.standardize_characters,
              'removeMetadata': args.remove_metadata,
              'parallel': args.parallel
    }
    return values

class ProgressInfo:
    """Instead of using a progress bar, output periodic progress to stdout

    update() method called when completed count increases. It
    periodically (depending on interval member variable) prints out
    percent complete to stdout.

    If I can convert to parallel, this probably won't be useful?

    """
    def __init__(self, total):
        self.last_output_count = 0
        self.total = total
        self.interval = 2       # Print out message no more than every interval%

    def update(self, new_count):
        lastpercent = 100 * self.last_output_count / self.total
        newpercent = 100 * new_count / self.total
        if newpercent >= lastpercent + self.interval:
            self.last_output_count = new_count
            lastpercent = newpercent
            print("%s - %d%% (%d of %d)" % (time.strftime("%c"), newpercent, new_count, self.total))

def process_file(filepath, source, destination):
    filename = os.path.basename(filepath)
    file_parts = os.path.splitext(filename)
    extension = file_parts[1].lower()
    if values['convertToPlaintext'] is True:
        processor = convert_to_plaintext
    elif values['encodeUtf8'] is True:
        processor = encode_to_utf8
    elif values['standardizeCharacters'] is True:
        processor = standardize_characters
    elif values['removeMetadata'] is True:
        processor = remove_pdf_metadata
    result = processor.run(filepath, source, destination, filename, extension)
    return result

def process_recursive(values):
    source = values['source']
    destination = values['destination']
    parallel = values['parallel']
    resultList = []
    supported_filetypes = ['.docx', '.pdf', '.html', '.pptx', '.txt', '.rtf', '.doc']

    # Reset the progress in the GUI.
    inc = 0
    processable_files = []
    skipped_files = []

    # Calculate the number of files to be processed.
    for dirpath, dirnames, files in os.walk(values['source']):
        for filename in files:
            file_parts = os.path.splitext(filename)
            extension = file_parts[1].lower()
            # Count supported filetypes.
            if extension in supported_filetypes:
                # Save the absolute path to the current file
                processable_files.append(os.path.join(dirpath, filename))
            else:
                # Otherwise save in a list of skipped files
                skipped_files.append(filename)

    progress = ProgressInfo(len(processable_files))
                
    # Loop through all files found in the source directory.
    if parallel:
        pool = Pool()

        # Default work chunk size to send to workers
        # Should there be a maximum cap to avoid using too much RAM?
        chunksize, extra = divmod(len(processable_files), 4*pool._processes)
        if extra:
            chunksize += 1

        results = list(pool.imap(process_file_nopaths,
                                 processable_files,
                                 chunksize=chunksize))
        pool.close()
        pool.join()
    else:
        for filepath in processable_files:
            # Perform the user-selected operation.
            result = process_file_nopaths(filepath)
            resultList.append(result)

            # Update the progress in the GUI.
            inc = inc + 1
            progress.update(inc)

    # Process results for output.
    failed = []
    succeeded = []
    for i in resultList:
        if i['result'] is True:
            succeeded.append([i['name'], i['message']])
        else:
            failed.append([i['name'], i['message']])

    print(' ')
    print('**********************************************************')
    print('******** The following were successfully processed *******')
    print(tabulate(succeeded, headers=['Filename', 'Message']))
    print(' ')
    print('**********************************************************')
    print(' ')
    if len(skipped_files) > 0:
        print('***** The following file(s) were ineligible for processing: *****')
        for skipped_file in skipped_files:
            print(skipped_file)
        print(' ')
    # Print failures, if present.
    if (len(failed) > 0):
        print('***** WARNING: The following failed or were skipped: *****')
        print(tabulate(failed, headers=['Filename', 'Message']))
        print(' ')
    else:
        print('*********** ALL FILES SUCCESSFULLY PROCESSED! ************')
    print('**********************************************************')
    print('Success count: ', len(succeeded))
    print('Failure/skipped count: ', len(failed) + len(skipped_files))
    print('**********************************************************')

    

values = get_cmdline_arguments()
process_file_nopaths = partial(process_file,
                               source=values['source'],
                               destination=values['destination'])
process_recursive(values)
