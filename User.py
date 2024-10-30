# -*- coding: utf-8 -*-
"""
Created for the community of Ravers!!
Enjoy it!

@author: Deneider
"""

#%%% User class

#  User
class User:
    def __init__(self, userId, name, password):
        self.userId = userId
        self.name = name
        self.password = password
        
    def addSong(self,song):
        # Add a new song in the list
        self.lastSong.insert(0, song)
        # Delete the final song of the list
        if len(self.lastSong) > 10:
            self.lastSong.pop()

# Admin user is a type of user
class Admin(User):
    def __init__(self, userId, name, password, admin = True):
        super().__init__(userId, name, password )
        self.admin = admin
        


