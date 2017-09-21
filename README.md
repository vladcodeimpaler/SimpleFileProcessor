# SimpleFileProcessor

Python file processor with input, done, error folders. 
You can give it a directory and define a method to run for each file in it.
It will process all files in the directory and move them to 'done' or 'failed' folders 
if processed successfully or not.

It provides two method process() and process_all().

## Usage

Instantiate the object and sets up the directories.

```
sfp = SimpleFileProcessor(input_folder='input',done_folder='done',failed_folder='failed')
```

Now you can drop any number of files into the */input* folder

To process a single file you first define a method to process. This is your *processing method*.

The method can be anything you want, any valid python code as long as it conforms to this signature. 

```
method(filename=filename, **method_kwargs)
```

It just has to return True or False if processing 
was successful or not. You get to define what successful means.

```
def process_method(filename):
    
    with open(filename) as f:
        do_something_with_file() # add it to db ?   
        return True    
    
    return False    # if file was not added to db, or could not be open, 
                    # return False (eg. processing method failed)    
```

The method can have 0 or more additional arguments as needed, besides the filename. 

Again, this is something you define. It just gets passed in as an argument to the SimpleFileProcessor.

You can now let SimpleFileProcessor do its thing by calling the *process()* or *process_all()* methods

Example
```
# run the process_method() against the 'data.csv' file
# the file has to exist in your input folder
status = fp.process(method=process_method,filename='data.csv')
```

Example with additional parameters
```
# run the process_method() against the 'data.csv' file with additional parameters
# the file has to exist in your input folder
status = fp.process(method=process_method,filename='data.csv',param1='hello')
...
# in this case you can define additional parameters in your method
def process_method(filename, param1):
    
    print param1
    with open(filename) as f:
        do_something_with_file() # add it to db ?   
        return True    
    
    return False    # if file was not added to db, or could not be open, 
                    # return False (eg. processing method failed)    
```

If the process_method() return True your file will be considered 'processed' 
and it will be moved to the 'done' folder.

If it returns False, your file will be moved to the 'failed' folder.
 
If the file wasn't processed at all, it will be left in the 'input' folder

You can disable moving of files by setting the following property

```
fp.dont_move_files = True
```




## Description


'Processing' means anything you want (eg. extracting data from the csv file into a db)
As each file completes processing the file is moved to a 'done' folder.
Alternatively if processing failed, it is moved to a 'failed' folder.


## Examples


### Use Case 1

You have a list of files with extension *.csv in your input folder.
You want to process each file sequentially.

Simple file processor lets you filter by file extension.
It also lets you define your input an output folders.

To define how to 'process' a file you define a simple method of this format.
The method looks like this:

### Use Case 2


## Release Log

### Version 1.0
- feature 1
- feature 2

## Todo List
- [s] add proper docstrings
- [s] add proper tests
- package into pip
- add statistics method 

## Enabling/Disabling Logging
```python
logging.basicConfig()
logging.getLogger("simplefileprocessor.simplefileprocessor").setLevel(logging.DEBUG)
```

## Building from Source
```
pip install -e .
```

## Tests
From the tests folder run:
```
python -m unittest -v test_simplefileprocessor
```