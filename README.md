# Sims3-Tools
Sims 3 Tools with features such as cleaning your sims 3 cache, or extracting CCs from a .package and automatically copying them into a folder.

## **To make it all work**
First of all, make sure that the _“Sims_Tools”_ folder is on your desktop and extracted, it has to be stored like this : _Desktop/Sims_Tools/Files inside_ and not _Desktop/Sims_Tools/Sims_Tools/Files inside_  or something like that. You can only drag the Sims_Tools.exe onto the desktop, out of the folder.<br/>

Right-click on the _“find_merged_cc.bat”_ file and select _“Modify”_.<br/>
  - Change the CCDIR line to where your Package folder is located.<br/>
    - _Exemple : SET "CCDIR=C:\Users\YOURNAME\Documents\Electronic Arts\Sims 3\Mods\Packages"_<br/>
  - Change the RESULTDIR line, putting the package extractor results where you want them.<br/>
    - _Exemple : SET "RESULTDIR=C:\Users\YOURNAME\Desktop\Results"_
      - Be sure to include quotation marks before CCDIR and RESULTDIR and at the end of the path.
  - And save it !

  ## **Features**
### Clear caches : 
- To clear your cache, you must first select your Sims 3 directory. To make sure you have selected the right Sims 3 folder, it will be written at the bottom of the window in white. Once selected, it will be saved and you won't need to change it again, unless you need to.
- After that, you can click on the button _"Clear caches"_ and it will automatically remove your temporary caches files.
  - I recommend you to clear the caches each time before launching the game.
### Extract the Packages :
- When you click on _"Extract the packages"_ select the .package file from which you want to extract the CCs, and they will automatically be copied to the folder you set in the _RESULTDIR_ line in the .bat file. Each time you perform a new extraction, it deletes the previous results.
- The package extractor works via the .bat file which calls the find_merged_cc.exe, the original .exe comes from [here](https://github.com/kitlith/sims3-rs/), I just modified the .bat
## Made with :
- [Python](https://www.python.org//) - Made with python at 100%
- [The GUI / CustomTKinter](https://customtkinter.tomschimansky.com//) - Graphic interface
## Versions
- Version 0.1
