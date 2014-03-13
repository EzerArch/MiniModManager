# (c) EZER'ARCH - Python script
# This creates a GUI-less mod manager. YAY!

# Simple
print ("\nThis is a Python application.")
print ("Created by: Ezer'Arch (www.ezerarch.com)")
print ("Date: 2013/10/23")

#### LIBS

import os
import glob
import subprocess
import easygui as eg


#### FUNCTIONS

# DEF: list and select the config

def cfgMan( path ):
    print( "\n-- Configs available --" )
    dir_cfg = os.path.join( path, '*.cfg' )
    lst_cfgs = glob.glob( dir_cfg )    # Display a list of CFGs
    if lst_cfgs:
        n = 1
        for path_cfg in lst_cfgs:
            print( '[', n, ']', os.path.split( path_cfg )[1][:-4] ) # namefile without extension
            n+= 1
        print( '[ ENTER ] for none and exit' )
        # CFG
        n = input ( 'Choose a config by typing a number: ' )
        if n is not '':
            cfg_n = int( n )
            path_cfg = lst_cfgs[ cfg_n - 1 ] # pick one from the list of cfgs
            file_cfg = os.path.split( path_cfg )[1][:-4] # file name of cfg
            print( 'You chose [', cfg_n, ']:', file_cfg, '.' ) # prompt user
            return path_cfg
        else:
            print( 'You chose no config. Nothing done.' )
            return None
    else:
        print( 'There is no config in the directory!' )
        return None


# DEF: list files in a directory (path)

def listFiles( path, tup_ext ):
    lst_files = os.listdir( path ) # list all content, includes folders
    lst_files_ext = [] # empty list
    for file in lst_files:
        if file.endswith( tup_ext ): # has the extension (.xxx) found in the tuple
            lst_files_ext.append( file ) # add the item in the list
    return lst_files_ext


# DEF: get the files to filter out

def readCfg( path ):
    if path is not None:
        lst_files_filter = [line.strip() for line in open( path )]
        return lst_files_filter
    else:
        pass


# DEF: rename all files not found in lst_files to -str_suffix

def renFiles( path, lst_files, lst_files_filter, str_suffix ):
    # Prompt
    print( "\n-- Renaming files --" )
    print( "Files from the config: " )
    for file in lst_files_filter:
        if file in lst_files:
            print( '*', file )
        else:
            print( '*', file, '(* not found! *)' )
    # Rename
    lst_files_rename = []
    for file in lst_files:
        if not file in lst_files_filter:
            path_file = os.path.join( path, file )
            path_file_new = path_file + str_suffix
            os.rename( path_file, path_file_new )
            lst_files_rename.append( file ) # add the item in the list
    print( "\nFiles renamed: " )
    for file in lst_files_rename:
        print( '*', file )


# DEF: rename back

def renFiles_back( path, lst_files, tup_ext ):
    print( "\n-- Renaming files back --" )
    print( 'Files found to be renamed back:', len( lst_files ) )
    for file in lst_files:
        if file.endswith( tup_ext ):
            path_file = os.path.join( path, file )
            path_file_new = path_file[:-1] # remove the last character
            os.rename( path_file, path_file_new )
    print( "Files renamed back!" )


# DEF: create CFG

def createCfg( pathdir_mod , file_exts ):
    files = listFiles( pathdir_mod, file_exts )
    cfg_files = eg.multchoicebox(msg='Pick as many items as you like.', title='Choose files', choices=files)
    if cfg_files:
        cfg_filename = input( "Type a name for the CFG: " ) + '.cfg'
        pathfile_cfg = os.path.join( pathdir_mod, 'MiniModManager', cfg_filename )
        f = open( pathfile_cfg,'w')
        for line in cfg_files:
            f.write( line + '\n' )
        f.close()
        print( "CFG created/edited." )

        key = input( 'Do you want to use the just-created config? y/<n>: ' ).lower()
        if key == 'y':
            files_filter = readCfg( pathfile_cfg ) # open cfg
            renFiles( pathdir_mod, files, files_filter, 'X' ) # rename files with 'X' in the end
    else:
        print( "No CFG was created/edited." )


#### VARIABLES

# Paths
path_app = os.getenv('APPDATA') # get appdata path
path_sav = os.path.join( path_app, '.minecraft\\saves' ) # make saves path
path_mod = os.path.join( path_app, '.minecraft\\mods' ) # make mod path
path_man = os.path.join( path_mod, 'MiniModManager' ) # make MiniModManager path


# File extensions
file_exts = ('.jar', '.zip') # files to be renamed
file_exts_x = ('.jarX', '.zipX') # files to be renamed back


#### EXECUTION

# HELLO WORLD!
print( '\nInitializing...')

# Check for folders
if os.path.exists( path_mod ): # mod directory
    print( 'Minecraft Mod directory found...' )
else:
    print( 'Minecraft Mod directory NOT found!' )

if os.path.exists( path_man ): # manager directory
    print( 'MiniModManager directory found...' )
else:
    print( 'MiniModManager directory was not found! Creating one in Minecraft\Mods.' )    
    os.makedirs( path_man ) # create manager directory

# Message
print( "\n*** MiniModManager is ready ***\nThis is a GUI-less mod manager that blocks files that shouldn't be loaded." )
input( "\nHit ENTER to proceed: " )


# Options
option = input( '''\nSelect an option:
1 = Use a config
2 = Unblock all files
3 = Create a config
4 = Open MiniModManager directory in the file manager
5 = Open Mods directory in the file manager
6 = Open Saves directory in the file manager
7 = (NOT WORKING) Block all files
ENTER = Exit
Enter the number for the option: ''' )

if option == '1':
    # check for *X-files
    files = listFiles( path_mod, file_exts_x ) # files to rename back
    if files:
        print( 'Your mod folder contains remaned files! Renaming them back... ' )
        renFiles_back( path_mod, files, file_exts_x )

    # Init CFG manager
    path_cfg = cfgMan( path_man )

    if path_cfg:
        # List the files
        lst_files = listFiles( path_mod, file_exts ) # list all files in the directory
        # Rename files
        lst_files_filter = readCfg( path_cfg ) # open cfg
        renFiles( path_mod, lst_files, lst_files_filter, 'X' ) # rename files with 'X' in the end

elif option == '2':
    #Rename files back
    lst_files = listFiles( path_mod, file_exts_x ) # files to rename back
    renFiles_back( path_mod, lst_files, file_exts_x )

elif option == '3':
    # check for _X-files
    files = listFiles( path_mod, file_exts_x ) # files to rename back
    if files:
        print( 'Your mod folder contains remaned files! Renaming them back... ' )
        renFiles_back( path_mod, files, file_exts_x )

    #Creates a new config
    createCfg( path_mod, file_exts )

elif option == '4':
    # open MiniModManager in the file manager
    print( 'Opening MiniModManager in your file manager...' )
    print( '>>>' )
    subprocess.Popen('explorer ' + path_man)
    print( 'Done!' )

elif option == '5':
    # open Mods directory in the file manager
    print( 'Opening Mods directory in your file manager...' )
    print( '>>>' )
    subprocess.Popen('explorer ' + path_mod)
    print( 'Done!' )

elif option == '6':
    # open Saves directory in the file manager
    print( 'Opening Saves directory in your file manager...' )
    print( '>>>' )
    subprocess.Popen('explorer ' + path_sav)
    print( 'Done!' )

else:
    print( 'Nothing was done.' )

# Exit
input("\nHit ENTER to exit.")

#EOF
