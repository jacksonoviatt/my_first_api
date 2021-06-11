import dbconnect
import mariadb
import traceback
from flask import Flask, Response, request
import json



# set app to conect with Flask
app = Flask(__name__)

# add the GET endpoint of animals
@app.get("/animals")

def get_animals():
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    animals = None
    try:
        # select all of the animals from the db and set to animals
        cursor.execute("SELECT name, id FROM animals")
        animals = cursor.fetchall()
    except:
        traceback.print_exc()
        print("something went wrong with the database")
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # send back an error message or a proper response if everything above goes well
    if(animals == None):
        return Response("Failed to get animals from DB", mimetype="text/plain", status=500)
   
    else:
         # translate animals to json
        animals_json = json.dumps(animals, default=str)
        # return the json response for Post man
        return Response(animals_json, mimetype="application/json", status=200)
    

# add the POST endpoint of animals
@app.post("/animals")

def post_animals():
    conn = None
    cursor = None
    new_animal = None
    try:
        new_animal = request.json['newAnimal']
    except:
        traceback.print_exc()
        print("There was a problem with the request")
   
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    try:
        cursor.execute("INSERT INTO animals (name) VALUES (?)", [new_animal])
        conn.commit()
    except:
        traceback.print_exc()
        print("something went wrong with the database")
    # new_animal_json = json.dumps(new_animal, default=str)
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    if(new_animal == None):
        return Response("Failed to post animal", mimetype="text/plain", status=500)
    else:
        return Response(f"Successfully posted {new_animal}!", mimetype="text/plain", status=200)

@app.patch("/animals")

def patch_animals():
    conn = None
    cursor = None
    animal_id = None
    updated_animal = None
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # your postman should look like something like this
    # {
    #     "idAnimal": 14,
    #     "updateAnimal": "Snow Owl"
    # }
    # request this JSON:
    try:
        animal_id = int(request.json['idAnimal'])
        updated_animal = request.json['updateAnimal']
    except:
        traceback.print_exc()
        print("There was a problem with the request")

    try:
        # select the animal based on the id so we have the animals previous name
        cursor.execute("SELECT name, id FROM animals WHERE id=?", [animal_id])
        # use fetchone because we selected by a single id
        old_animal = cursor.fetchone()[0]
    except:
        traceback.print_exc()
        print("There was a problem selecting the original animals name")
    try:
        # update the db with the updated animal and the animal id then commit
        cursor.execute(f"UPDATE animals SET name=? WHERE id=?", [updated_animal, animal_id])
        conn.commit()
    except:
        traceback.print_exc()
        print("There was a problem updating animals name")

#    close connections
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)

    # send back an error message or a proper response if everything above goes well
    if(updated_animal == None or animal_id == None):
        return Response("Failed the patch request", mimetype="text/plain", status=400)
    else:
        return Response(f"Succesfully updated {old_animal} to {updated_animal}", mimetype="text/plain", status=200)

@app.delete("/animals")

def delete_animals():
    conn = None
    cursor = None
    animal_id = None
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)

    try:
         # your postman should look like something like this
    # {
    #     "idAnimal": 14,
    # }
    # request this JSON:
        animal_id = int(request.json['idAnimal'])
        cursor.execute("SELECT name, id FROM animals WHERE id=?", [animal_id])
        # set the name of the animal to be deleted
        animal_name = cursor.fetchone()[0]
    except:
        traceback.print_exc()
        print("There was a problem selecting the name of the animal to be deleted")
    try: 
        # delete the animal from the database based on the id
        cursor.execute("DELETE FROM animals WHERE id=?", [animal_id])
        conn.commit()
    except:
        traceback.print_exc()
        print("There was a problem deletimg the name of the animal from the database")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)

    # send back an error message or a proper response if everything above goes well
    if(animal_id == None):
        return Response("Failed to delete animals", mimetype="text/plain", status=400)
    else:
        return Response(f"Succesfully deleted {animal_name}", mimetype="text/plain", status=200)



app.run(debug=True)