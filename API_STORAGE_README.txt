    # For shared media, documents, and downloads
    ############################################
    # 
    # Shared Storage is a database, NOT a Linux file system.
    # See notes below about implementation differences for devices using
    # api <29
    #
    # The database is organized in Root Directories
    #  'Music'         
    #  'Movies'        
    #  'Pictures'      
    #  'Documents'     
    #  '*'             (default) one of the first 4 depending on file extension
    #  'Downloads'     
    #  'DCIM'          For retrive of camara data. 
    #
    #  Within those Root Directories this app's public files are stored under
    #  its 'AppName'. Sub-directories are available.
    #
    # The database operations 'insert', 'retrieve', and 'delete' are
    # implemented. An insert overwrites an existing entry. Retrieve from
    # storage created by other apps requires READ_EXTERNAL_STORAGE
    #
    # Entries are defined by Root Directory, optional sub-directory, and file
    # name.
    #
    # Entries persist after this app is uninstalled.
    # 
    # The api defaults to the 'external' volume, 'internal' is available.
    #
    # Device api<29 requires WRITE_EXTERNAL_STORAGE
    #
    # Files in 'Downloads' do not have a uri if device api < 29
    #
    # Two additional methods enable interoperability with the Android
    # 'android.net.Uri' class.
    #
    # ######## Android Version Transition, Read me, Really ###############
    #
    # The api above is consistent from device api = 21 to at least api = 30.
    # However the internal implementation is different between devices with
    # api >= 29 and api < 29. This is a characteristic of Android storage.
    # See for example
    #  https://www.raywenderlich.com/10217168-preparing-for-scoped-storage
    #
    # On new Android versions the file is owned by the database, on older
    # Android versions the file is owned by the app.
    # Thus when device api < 29 , a file can be deleted by the user but the
    # data base entry may still exist. And retrieve() will return ""
    #
    # On newer devices the datebase key for file path is RELATIVE_PATH
    # on older devices it is DATA which is now depreciated.
    #
    # The two implementations require special handling of the user's
    # data when the user moves files to a platorm with api >= 29 from one with
    # api < 29. This is a general Android issue and not specific to this
    # module.
    #
    # The transition handling might involve:
    # Before transition 1) Copy the app's shared files to private storage.
    #                   2) Delete the app's database entries
    # After transition  3) Insert the copies into the database
    #                   4) Delete the copied files.
    # If 1) and 2) are done after the transition, before doing 3) manually
    # delete the shared files
    #
    ###################
    #
    # Database Operations:
    # insert()      - copy a PrivateStorage file into this app's SharedStorage.
    # retrieve()    - copy a SharedStorage file to PrivateStorage on device
    #                 api>= 29 and return a file path, else return a file path.
    # delete()      - delete a file in this app's SharedStorage.
    #
    # Interoperability with Android 'android.net.Uri' class:
    # getUri()      - get a Uri from SharedStorage path,          returns Uri
    # retrieveUri() - copy SharedStorage Uri to PrivateStorage,
    #                  returns a file path
    #
    ###################
    # The API:
    #
    # insert(file_path,       
    #        root_dir = '*', 
    #        sub_dir = '',  
    #        volume = 'external') 
    #               returns True if file inserted
    #
    # retrieve(file_name           
    #        root_dir = '*'      
    #        sub_dir = '',       
    #        app_name = '',    requires READ_EXTERNAL_STORAGE   
    #        volume = 'external')
    #                returns a PrivateStorage file path, or a URL string
    #
    # delete(file_name,          
    #        root_dir = '*',     
    #        sub_dir = '',       
    #        volume = 'external')
    #                 returns True if file exists to delete
    #
    # getUri(file_name,          
    #        root_dir = '*',     
    #        sub_dir = '',       
    #        app_name = '',    requires READ_EXTERNAL_STORAGE   
    #        volume = 'external')
    #                   returns a Uri ('android.net.Uri')
    #                   Except if 'Downloads' and device api <29, returns None
    #
    # retrieveUri(uri) #A 'android.net.Uri' from some other Android Activity
    #                   returns a PrivateStorage file path.
    #     
    #######################
    #
    # Examples:
    # Where txt_file could be PrivateStorage().getFilesDir() + 'text.txt'
    # and so on.
    # All methods take a required file name, and optional directory parameters.
    #
    #   Insert:
    #   SharedStorage().insert(txt_file, 'Documents')
    #   SharedStorage().insert(txt_file, sub_dir= 'a/b')
    #   SharedStorage().insert(txt_file, 'Downloads')
    #   SharedStorage().insert(jpg_file, 'Pictures')
    #   SharedStorage().insert(mp3_file)
    #   SharedStorage().insert(ogg_file, 'Music')
    #
    #   Retrieve:
    #   path = SharedStorage().retrieve('test.txt')
    #   path = SharedStorage().retrieve('test.txt', 'Documents', 'a/b')
    #
    #   Delete:
    #   SharedStorage().delete('test.mp3', 'Music')
    #
    #   Retrieve from another app's storage (requires READ_EXTERNAL_STORAGE) :
    #   SharedStorage().retrieve('10_28_14.jpg', 'DCIM', '2021_03_12',
    #                            'CameraXF')
    #   SharedStorage().retrieve('10_33_48.mp4', 'DCIM', '2021_03_12',
    #                            'CameraXF')
    #
    #######################



