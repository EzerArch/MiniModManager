# (c) EZER'ARCH - Python script
# This creates a GUI-less mod manager. Main runtime.
# Released under MIT License
# TO-DO:
# (nothing yet)

# FUNTIONS LIB

# Simple
print ("\nFunction.")

#### LIBS

import os
import glob
import subprocess
import easygui as eg


#### FUNCTIONS

# DEF: generic error

def err():
    """
Generic error to be displayed to the user.
"""
    print( "***Error: Check if Minecraft is running with mods or if there are duplicate files!***")
    pass
    

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
    """
path: the path where the function will take place
lst_files: list of files
lst_files_filter: list of files to be filtered out
str_suffix: file extension sufix
"""
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

# EOF
