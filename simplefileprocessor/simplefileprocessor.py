"""
    Simple File Processor Module

    https://github.com/vladcodeimpaler/SimpleFileProcessor
"""

import os,logging,shutil
import errno
from glob import glob

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # setup default module logging


class SimpleFileProcessor(object):

    """
        Simple File Processor

        processes files from input folder using a method created by the user
        method is passed in as a parameter method=process_file
        creates output files (if any) in output folder
        moves every processed file from input folder to done folder when done
    """

    def __init__(self,input_folder,done_folder,failed_folder):
        self.input_folder = input_folder
        self.done_folder = done_folder
        self.failed_folder = failed_folder
        self.dont_move_files = False

        try:
            os.makedirs(self.input_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        try:
            os.makedirs(self.done_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


        try:
            os.makedirs(self.failed_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


    def cleanup(self, input_folder=False, done_folder=False, failed_folder=False):

        """
        deletes all files in given folders
        """

        pass


    def process(self, method, filename, **method_kwargs):

        """
            processes given filename using method passed in.
            filename must exist in input_folder
            method should be a method that return true or false indicating the file was
            processed successfully or not
            returns true if method() returns true

        """

        log.info("Processing file '{}'".format(filename))

        if os.path.isfile(os.path.join(self.input_folder,filename)):
            # status = method(*method_args,filename=filename)
            status = method(filename=filename, **method_kwargs)
            if status:
                self.move_to_folder(filename,self.done_folder)
                return True
            else:
                self.move_to_folder(filename,self.failed_folder)
                return False
        else:
            log.error("Could not process file '{}'. File doesn't exist in {}".format(filename,self.input_folder))
            return False


    def process_all(self, method, extension_filter=None, process_subfolders=False, **method_kwargs):

        """
        processes all files in input folder. same logic as process()
        return true if all matching files were successfully processed

        :param process_subfolders - if True, it will process any files in all subfolders of the input_folder recursively
        """

        files_processed = 0
        total_files = 0

        files = []

        if process_subfolders:
            log.info("Processing all files in '{}' and subfolders".format(self.input_folder))
            files = [y for x in os.walk(self.input_folder) for y in glob(os.path.join(x[0],'*.html'))]
        else:
            log.info("Processing all files in '{}'".format(self.input_folder))
            files = os.listdir(self.input_folder) # process only files in input_folder only

        for filename in files:
            if extension_filter:
                if filename.endswith("."+extension_filter):
                    total_files += 1
                    status = self.process(filename=filename, method=method, **method_kwargs)
                    if status:
                        files_processed += 1
            else:
                total_files += 1
                status = self.process(filename=filename, method=method, **method_kwargs)
                if status:
                    files_processed += 1

        log.info("Summary: Matched {} files. Processed {} files".format(total_files, files_processed))

        if files_processed == total_files:
            return True
        else:
            return False


    def move_to_folder(self,filename,folder):
        """
            Moves file to folder when done. Internal method.
        """
        if self.dont_move_files:
            return True

        log.info("File '{}' processed and moved to '{}' folder".format(filename,folder))

        # move file to done, keep folder structure

        subfolders = filename.split(os.path.sep)[0:-1]
        # print subfolders

        try:
            os.makedirs(os.path.join(folder,* subfolders)) # create all subdirectories
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        shutil.move(os.path.join(self.input_folder,filename),os.path.join(folder,filename))

        return True