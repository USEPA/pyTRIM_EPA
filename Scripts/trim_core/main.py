import os

from .classic.BuilderMain import BuilderMain


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BuilderMain(f"{root}/Input_Files/1Parameters.csv",
                f"{root}/Input_Files/8Layout_Parceldf.csv",
                f"{root}/Input_Files/2Layout_Coordinatesdf.csv",
                f"{root}/Input_Files/9Layout_EmissionSources.csv",
                f"{root}/Input_Files/3Plants.csv",
                f"{root}/Input_Files/10USLECalcs.csv",
                f"{root}/Input_Files/4Land_Constants.csv",
                f"{root}/Input_Files/11Land_ErosionParameters.csv",
                f"{root}/Input_Files/5Land_SedDelivCoeff.csv",
                f"{root}/Input_Files/12Land_SedDeliv.csv",
                f"{root}/Input_Files/6Soil.csv",
                f"{root}/Input_Files/13Watersheds.csv",
                f"{root}/Input_Files/7Lakes.csv",
                f"{root}/Input_Files/14Fish.csv",
                f"{root}/Output_Files/")
