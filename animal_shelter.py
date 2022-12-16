from pymongo import MongoClient
from bson import ObjectId

# AnimalShelter object provides CRUD functionality for a MongoDB.
class AnimalShelter():
    
    # The constructor will connect to the specified mongodb server using authentication.
    def __init__(
            self, host, port, db, collection, auth_db, username, password):
        
        self.client = MongoClient("mongodb://%s:%s@%s:%d/?authMechanism=DEFAULT&authSource=%s"
                                  % (username, password, host, port, auth_db))
        self.database = self.client[db]
        self.collection = collection
        
    # Function to insert a document into the database.
    def create(self, document):
        if document is not None:
            self.database[self.collection].insert_one(document)
            return True
        else:
            # Return false since there is no document to insert.
            return False
            
    # Read function accepts a query as a Python dictionary and returns a cursor object
    def read(self, document):
        if document is not None:
            cursor = self.database[self.collection].find(document, {'_id': False})
            return cursor
        else:
            print("Document must contain a valid MongoDB query as a dictionary.")
            return None
    def read_one(self, document):
        if document is not None:
            return self.database[self.collection].find_one(document, {"_id": False})
        else:
            print("Document must contain a valid MongoDB query as a dictionary")
            return None
        
    # Update function accepts a query and update data as a dictionary and retuns a Pymongo result object.
    # Returns none if an error occurs othwerwise returns a Pymongo result object.
    def update(self, query, data, multi = False):
        if not multi: # Update single document
            try:
                result = self.database[self.collection].update_one(query, data)
                
                # If document was not found or document found but not updated, inform the user and return.
                if result.matched_count <= 0:
                    print("Error: Query did not return any documents to update.")
                    return None
                elif result.modified_count <= 0:
                    print("Error: Unable to update document. Check your query and update data and try again.")
                    return None
                
                return result
            
            # Handle exceptions.
            except ValueError: 
                print("Error: Query or data not formatted correctly.")
                return None
            except TypeError:
                print("Error: Query and data must be of the dictionary type.")
                return None
            
        # Update multiple records
        try:
            result = self.database[self.collection].update_many(query, data)
            
            # If document was not found or document found but not updated, inform the user and return.
            if result.modified_count <= 0:
                print("Error: Unable to update document. Check your query and update data and try again.")
                return None
            elif result.matched_count <= 0:
                print("Error: Query did not return any documents to update.")
                return None
            return result
        # Handle exceptions.
        except ValueError:
            print("Error: Query or data not formatted correctly.")
            return None
        except TypeError:
            print("Error: Query and data must be of the dictionary type.")
            return None
    # Delete accepts a query as a dictionary and returns a Pymongo result object.
    def delete(self, data, multi = False):
        if not multi:
            try:
                result = self.database[self.collection].delete_one(data)
                if result.deleted_count <= 0:
                    print("Error: Unable to delete document")
                    return None
                return result
            except ValueError:
                print("Error: Query not formatted correctly.")
                return None
            except TypeError:
                print("Error: Data must be of the dictionary type.")
                return None
            
        else: # Delete multiple documents
            try:
                result = self.database[self.collection].delete_many(data)
                
                if result.delted_count <= 0:
                    print("Error: Unable to delete document.")
                    return None
                return result
            except ValueError:
                print("Error: Query not formatted correctly.")
                return None
            except TypeError:
                print("Error: Data must be of the dictionary type.")
                return None
    
    # Accepts a column name and returns a distinct list.    
    def distinct(self, columnName):
        if columnName is None or not columnName:
            print("Error: column name must not be blank or empty.")
            return None
        return self.database[self.collection].distinct(columnName)

    # Returns the number of documents matching a query
    def count(self, query):
        if query is None or not query:
            print("Invalid Query")
            return None
        return self.database[self.collection].count_documents(query)

    