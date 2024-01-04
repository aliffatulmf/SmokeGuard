import logging
import os

from git import GitCommandError, Repo


class GitHubRepository:
   def __init__(self, repository_name, dest=None):
       self.__repository_url = f"https://github.com/{repository_name}.git"
       self.__dest = dest or os.getcwd() # Default destination is current working directory
       self.__repo = None

   def __directory_exists(self):
       return os.path.exists(self.__dest)

   def clone(self, ref=None, verbose=False):
       if self.__directory_exists():
           if verbose:
               logging.info(f"Destination directory already exists: {self.__dest}")
           return True
       try:
           self.__repo = Repo.clone_from(self.__repository_url, self.__dest, branch=ref)
       except GitCommandError as error:
           if verbose:
               logging.error(f"An error occurred: {error}")
           return False
       return True

   def check_availability(self, verbose=False):
       if self.__repo is None:
           if verbose:
               logging.info("Repository is not cloned yet.")
           return False
       try:
           self.__repo.remotes.origin.pull() # Pull the latest commits. If this fails, an exception is thrown.
           return True
       except GitCommandError: # Catch the specific exception thrown by git pull.
           if verbose:
               logging.info("Error while pulling the latest commits.")
           return False

   def get_latest_commit(self, verbose=False):
       if self.check_availability(verbose):
           return self.__repo.head.object.hexsha
       else:
           return None
