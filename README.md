# **PyBuilder**

### **Folders:**

1. Documentation - any documentation/meeting notes.



2. Input_Files - contains dummy input files for Foundries.



3. Param Inventory and UI Mockup
    - *2. ParamtersTab_Inventory_20191107_withCTHWork.xlsx*  - descriptions of all parameters in the Excel Builder "Parameters" sheet, including primary/secondary designation, implementation within Excel Builder, and ideas on implementation in the new pyBuilder. See the Powerpoint file below for visual mockup ideas of the pyBuilder UI.



    - *3. AllOtherTabs_Inventory_20191107_withCTHWork.xlsx*  - same as file 2 above, but for all the other sheets in the Excel Builder.



    - *GUI Slides.pptx*  - Powerpoint mockups of potential pyBuilder UI screens. The two Excel files above are a companion to this, as they contain additional descriptions of these screens and their functionality.



4. PyQt5_Test - PyQt5 example.



5. Scripts - contains the following folders:
    - *Classes*  - contains Parcel.py, ParcelCollection.py, and OutputFormatter.py, which implement a parcel, parcel collection, and output formatting classes respectively. Also includes test_modules.py, a non-exhaustive unit test file which tests the Parcel and Parcel Collection classes.



    - *HelperFunctions* - contains Layout.py which houses miscellaneous functions used in the Layout tab of the builder. Additional helper functions can go here.



    - *OutputFileGenerators* - contains GenerateCompartments.py, GenerateProperties.py, GenerateSources.py, and GenerateVolumeElements.py which produce the TRIM syntax output files. 



### For Development Testing

#### Console

1. Navigate to the `./Scripts` folder.
2. Start a Python console in your virtual environment.
    1. If the DB has not previously been initialized, run the following,
    then restart your python console:
        ```python
        from trim_db.migrate import run_migration
        run_migration('./trim_db/migrations/scripts/migrate.sql')
        ```
3. Open a DB connection and initialize dummy User/Role classes:
    ```python
    from trim_db.local import *
    ```
4. Import the DB services:
    ```python
    from trim_db.services import *
    ```

    This will let you use the `db` object and `[name]Service` classes
    from the console. E.g.,

    ```python
    c = ChemicalService.get(name='MethylMercury')
    ```

##### Importing Scenarios from Old Syntax

1. To do this from the console, run the following in your virtual environment:
```bash
python ./Scripts/import_scenario.py -c "path/to/import/config.json"
```
Or,
```bash
python ./Scripts/import_scenario.py --scenario "Name" --directory "path/to/trim/files" --import-rules "import/rules/file.json"
```
See `./Scripts/import_config` for premade configs.

2. To do this from the Python interpreter, run
```python
from import_scenario import import_scenario
import_scenario({
    "scenario_name": "Name",
    "directory": "path/to/trim/files",
    "import_rules": "import/rules/file.json"  # Optional
})
```