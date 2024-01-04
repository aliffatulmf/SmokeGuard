import logging
import os

from git import GitCommandError, Repo


class GitHubRepository:
   def __init__(self, repository_name, dest=None):
       self.__repository_url, self.__dest, self.__repo = f"https://github.com/{repository_name}.git", dest or os.getcwd(), None

   def __directory_exists(self): return os.path.exists(self.__dest)

   def clone(self, ref=None, verbose=False):
       if self.__directory_exists():
           if verbose: logging.info(f"Destination directory already exists: {self.__dest}")
           return True
       try: self.__repo = Repo.clone_from(self.__repository_url, self.__dest, branch=ref)
       except GitCommandError as error:
           if verbose: logging.error(f"An error occurred: {error}")
           return False
       return True

   def check_availability(self, verbose=False):
       if self.__repo is None:
           if verbose: logging.info("Repository is not cloned yet.")
           return False
       try: self.__repo.remotes.origin.pull()
       except GitCommandError:
           if verbose: logging.info("Error while pulling the latest commits.")
           return False
       return True

   def get_latest_commit(self, verbose=False):
       return self.__repo.head.object.hexsha if self.check_availability(verbose) else None
