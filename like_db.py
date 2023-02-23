import json
#Create Like counting class
from tinydb import TinyDB
from tinydb.table import Document

class LikeDB:
    def __init__(self, db_path):
        #Initialize the database
        self.db_path = db_path
        self.db = TinyDB(db_path, indent=4)
        self.users = self.db.table('users')
        self.img=self.db.table('img')

    def add_immage(self,image_id):
        imge={'likes':0,'dislikes':0}
        image=Document(imge,doc_id=image_id)
        self.img.insert(image)
        return None


    def get_likes_dislike(self, image_id):
        """Counts all users likes
        returns
            all users likes
        """
        # Query the database for all images
        # Count the number of likes
        likes=self.img.get(doc_id=image_id)
        return [likes['likes'],likes['dislikes']]
        
        
    #Add a like to the database
    def add_like(self, user_id,image_id)->dict:
        '''
        Add a like to the database
        args:
            user_id: The user id of the user who liked the post
            image_id: The image id of the image that was liked
        returns:
            The number of likes and dislikes for the post
        '''
        # Get the user document
        # If the user document does not exist, create it
        likes,dislikes=self.get_likes_dislike(image_id)
        if self.users.contains(doc_id=user_id):
            user_doc = self.users.get(doc_id=user_id)
            if user_doc.get(str(image_id),False):
                if user_doc[str(image_id)]['like'] == 0 and user_doc[str(image_id)]['dislike']==1:
                    self.users.update({image_id:{'like':1,'dislike':0}},doc_ids=[user_id])
                    self.img.update({'likes':likes+1,'dislikes':dislikes-1},doc_ids=[image_id])
                elif user_doc[str(image_id)]['like'] == 1 and user_doc[str(image_id)]['dislike']==0:
                    self.users.update({image_id:{'like':0,'dislike':0}},doc_ids=[user_id])
                    self.img.update({'likes':likes-1,'dislikes':dislikes},doc_ids=[image_id])
                else:
                    self.users.update({image_id:{'like':1,'dislike':0}},doc_ids=[user_id])
                    self.img.update({'likes':likes+1,'dislikes':dislikes},doc_ids=[image_id])   
            else:
                user_doc[image_id] = {'like': 1, 'dislike': 0}
                user_doc=Document(user_doc,doc_id=str(user_id))
                self.users.insert(user_doc)
                self.img.update({'likes':likes+1,'dislikes':dislikes},doc_ids=[image_id])

        else:
            user_doc = {image_id: {'like': 1, 'dislike': 0}}
            user_doc=Document(user_doc,doc_id=user_id)
            self.users.insert(user_doc)
            self.img.update({'likes':likes+1,'dislikes':dislikes},doc_ids=[image_id])
        return None

    #Add a dislike to the database
    def add_dislike(self, user_id,image_id):
        '''
        Add a dislike to the database
        args:
            user_id: The user id of the user who disliked the post
        returns:
            The number of likes and dislikes for the post
        '''
        imge=self.img.get(doc_id=image_id)
        likes=imge['likes']
        dislikes=imge['dislikes']
        if self.users.contains(doc_id=user_id):
            user_doc = self.users.get(doc_id=user_id)
            if user_doc.get(str(image_id),False):
                if user_doc[str(image_id)]['dislike'] == 0 and user_doc[str(image_id)]['like']==1:
                    self.users.update({image_id:{'like':0,'dislike':1}},doc_ids=[user_id])
                    self.img.update({'likes':likes-1,'dislikes':dislikes+1},doc_ids=[image_id])
                elif user_doc[str(image_id)]['like'] == 0 and user_doc[str(image_id)]['dislike']==1:
                    self.users.update({image_id:{'like':0,'dislike':0}},doc_ids=[user_id])
                    self.img.update({'likes':likes,'dislikes':dislikes-1},doc_ids=[image_id])
                else:
                    self.users.update({image_id:{'like':0,'dislike':1}},doc_ids=[user_id])
                    self.img.update({'likes':likes,'dislikes':dislikes+1},doc_ids=[image_id])   
            else:
                user_doc[image_id] = {'like': 0, 'dislike': 1}
                user_doc=Document(user_doc,doc_id=str(user_id))
                self.users.insert(user_doc)
                self.img.update({'likes':likes,'dislikes':dislikes+1},doc_ids=[image_id])

        else:
            user_doc = {image_id: {'like': 0, 'dislike': 1}}
            user_doc=Document(user_doc,doc_id=user_id)
            self.users.insert(user_doc)
            self.img.update({'likes':likes,'dislikes':dislikes+1},doc_ids=[image_id])
        return None

