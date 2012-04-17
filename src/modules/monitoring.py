#!/usr/bin/python
# -*- coding: utf8 -*-
# Description: Process identification files
# Authors: Daniel Rodríguez
# Date: $Date: $
# Revision: $Revision: $
# LastChangedBy: $LastChangedBy: $
# HeadURL: $HeadURL: $

import os, os.path, datetime,  sys

"""This module is used for monitoring and locking purposes. Each application
       using this resource is responsible for creating it's own monitor file and can
       use it to record information about the process execution status and other data 
       about the current status of the application. 
       Other applications can use the recorded status information in the monitoring files. 
       There is always a single process that holds the file and it is the only process allowed to write in it. 
       Other processes are only allowed to read it.
       The modality of use depend on if the application is the one that publishes the status information or is the one that consumes it.
       The publisher
        ========
        It is responsible of create the monitor file. It is usually dome in the main file of the application :
            import monitoring
            monitoring.start_record ("SOME_APPLICATION", /some/directory/path)
            
        The main application and all imported modules can publish information by:
        
            monitoring.record.set_line ("progress", "10/100")
            
        The publisher is also responsible of cleaning up the monitor file before exit:
        
            monitoring.record.destroy()
            
        The consumer
        =========
        
        Consumer processes should know the name of the application they want to monitor and the location of the file (the directory).
        Then it is easy for them to read the records:
        
            import monitoring
            
            remote_record = monitoring.MONITOR_FILE ("SOME_APPLICATION", /some/directory/path)
            
            print remote_record.read().progress
        
        Outputs: 10/100
        
       """

def start_record (application_name,  directory_path="."):
    global record
    try:
        record = MONITOR_FILE (application_name,  dirpath=directory_path).create ()
    except:
        raise Exception
    

class MONITOR_FILE (object):

    """MONITOR_FILE is used for monitoring and locking purposes. 
        """

    def __init__ (self, appl, dirpath="."):
        """Initialize with the monitor file name 'appl'.pid."""
        assert os.path.isdir (dirpath),  "Nonexistent dirpath: '%s'" % dirpath
        dirpath = os.abspath (dirpath)
        self._appl = appl
        self._fn = os.path.join (dirpath,  appl + ".pid")
        self.created = os.path.isfile (self._fn)
        self._load_data ()
        
    def create (self):
        """Create the monitor file."""
        assert not self.created, "File '%s' already exists" % (self.name ())
        f = file (self._fn,  "w+")
        pid = str (os.getpid ())
        user = os.environ['LOGNAME']
        t = datetime.datetime.now ().isoformat ()
        lines = ["pid: " + pid + "\n", "user: " + user + "\n", "start: " + t + "\n" ]
        f.writelines (lines)
        f.close ()
        self.created = os.path.isfile (self._fn)
        self._load_data ()
        assert self.created
        return self
    
    def destroy (self):
        """Destroy the monitor file."""
        assert self.created
        assert self.created_by_me ()
        self._data = {}
        bck = self._fn + "~"
        os.rename (self._fn,  bck)
        self.created = os.path.isfile (self._fn)
        assert not self.created
        
    def name (self):
        """Name of the monitor file."""
        return self._fn
        
    def read (self):
        """Read the monitor file."""
        self._load_data ()
        return self

    def _load_data (self):
        self._data = {}
        if self.created:
            f = file (self._fn)
            lines = f.readlines ()
            f.close ()
            for line in lines:
                parts = line.split (":")
                k = parts [0]
                c = line [len (k )+ 1:].strip()
                self._data [k] = c
            
    def __getattr__(self, key):
        return self._data.get (key, "")
        
    def keys (self):
        return self._data.keys()
    
    def _save_data (self):
        assert self.created
        assert self.created_by_me ()
        lines = [k + ": " + self._data [k] + "\n" for k in self._data.keys () ]
        f = file (self._fn,  "w+")
        f.writelines (lines)
        f.close ()

    def created_by_me (self):
        """Was the monitor file created by me (the current process)?"""
        if self.created:
            pid_in_file = self._data ["pid"]
            my_pid = str (os.getpid ())
            return pid_in_file  == my_pid
        else:
            self.create ()
            return True
            
    def set_line (self, key, value):
        """Set a line of information in the monitor file containing the given 'key'
           and 'value'."""
        assert self.created
        self._load_data ()
        assert self.created_by_me ()
        self._data [key] = value
        self._save_data()
