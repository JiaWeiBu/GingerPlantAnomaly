# __init__.py

from classes.util_lib import Color

# Define a flag to check if the package has already been imported
if not globals().get('__classes_package_imported__', False):
    Color.Print(Color.ColorCode.red_, "Classes Package has been imported")
    globals()['__classes_package_imported__'] = True
else:
    Color.Print(Color.ColorCode.green_, "Successfully re-imported the Classes Package")