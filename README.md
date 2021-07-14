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