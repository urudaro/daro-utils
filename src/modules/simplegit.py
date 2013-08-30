#!/usr/bin/python
# -*- coding: utf8 -*-
# Description: Basic routines to handle a GIT repository
# Authors: Daniel Rodríguez
# Date: $Date: $
# Revision: $Revision: $
# LastChangedBy: $LastChangedBy: $
# HeadURL: $HeadURL: $

import os, os.path
#import datetime,  sys

def output_lines (cmd):
    import subprocess as sp
    p = sp.Popen ([cmd], shell=True, stdout=sp.PIPE, stderr=sp.PIPE, close_fds=True)
    stdoutdata, stderrdata = p.communicate ()
    return stderrdata.splitlines (True) + stdoutdata.splitlines (True)
    
def create_git_repository (base_path):
        dotgit = os.path.join (base_path,  ".git") 
        if os.path.isdir (dotgit): return dotgit
        r = output_lines ("git --git-dir=%s init" % dotgit)
        return dotgit, r
        
class REPOSITORY (object):
    """Simple encapsulation of a git-repository providing some functions used to manipulate a collection of files using git"""
    def __init__(self,  base_path, user=None, email= None):
        """In 'base_path' must reside a valid git-repositry"""
        self.dotgit = os.path.join (base_path,  ".git")    
        assert os.path.isdir (self.dotgit),  "%s is not a valid git-repository" % self.dotgit
        self.base_path = base_path
        u = ""
        if user:
            u = "-c user.name=%s " % user
        e = ""
        if email:
            e = "-c user.email=%s " % email
        c = u + e
        self.git_alias = "git %s--git-dir=%s --work-tree=%s" % (c,  self.dotgit, self.base_path)
        self.last_gitcmd = ""
        self._tags = None
        
    def _load_tags (self):
        self.last_gitcmd = "%s tag" % self.git_alias
        self._tags = [x.strip() for x in output_lines (self.last_gitcmd)]
        
    def ls (self, adir,  tn="master"):
        """List git tracked files in the directory 'dir' of the tag 'tn' running the command ls-tree 'tn':'adir'.
        'adir' is a path relative to self.base_path"""
        assert tn == "master" or self.has_tag (tn),  "%s is not avalid tag name" % tn 
        assert os.path.isdir (os.path.join(self.base_path,  adir))
        self.last_gitcmd = "%s ls-tree %s:%s --name-only" % (self.git_alias,  tn, adir)
        return output_lines (self.last_gitcmd)
        
    def ls_date (self,  adir,  d):
        """List files in directory 'dir' included in the latest tag earlier than the date 'd'."""
        return self.ls (adir,  tn=self.tag (d))
        
    def cat (self, fn,  tn="master"):
        """Retrieve contents of the file 'fn' in the tag 'tn'. 
        'fn' is the file path relative to self.base_path, usually gotten in a self.ls* call"""
        assert tn == "master" or self.has_tag (tn)
        self.last_gitcmd = "%s show %s:%s" % (self.git_alias,  tn,  fn)
        return "".join (output_lines (self.last_gitcmd))
        
    def tags (self):
        """List all the tags in the repository"""
        if not self._tags: self._load_tags ()
        return self._tags
        
    def first_tag (self):
        return self.tags ()[0]
        
    def last_tag (self):
        return self.tags ()[-1]
        
    def tag (self, d= "3000"):
        """Latest tag earlier then 'd'"""
        latest = None
        for t in self.tags():
            if t <= d:
                latest =t
            else:
                break
        return latest

    def has_tag (self,  tn):
        return tn in self.tags ()
        
    def set_tag (self,  tn):
        assert not self.has_tag (tn),  "Tag named %s already exists" % tn
        self.last_gitcmd = "%s tag %s" % (self.git_alias,  tn)
        lines = output_lines (self.last_gitcmd)
        self._load_tags ()
        return lines
        
    def add_directory (self,  adir):
        """Add files in the directory 'adir' relative to self.base_path."""
        assert os.path.isdir (os.path.join (self.base_path,  adir)),  "%s is not a valid directory" % adir
        self.last_gitcmd = "%s add %s" % (self.git_alias,  adir)
        return output_lines (self.last_gitcmd)
        
    def add_file (self,  fn):
        """Add file 'fn' relative to self.base_path"""
        assert os.path.isfile (os.path.join (self.base_path,  fn)),  "%s is not a valid file" % fn
        self.last_gitcmd = "%s add %s" % (self.git_alias,  fn)
        return output_lines (self.last_gitcmd)
        
    def commit (self,  m):
        """Commit added changes"""
        self.last_gitcmd = '%s commit -m "%s"' % (self.git_alias,  m)
        return output_lines (self.last_gitcmd)
        
    def log (self, filename=""):
        """history"""
        if filename != "":
            filename = " -- " + filename
        self.last_gitcmd = '%s log %s' % (self.git_alias, filename)
        return output_lines(self.last_gitcmd)
        
def test_git ():
    pass ## TODO
    
if __name__ == '__main__':
    test_git ()
