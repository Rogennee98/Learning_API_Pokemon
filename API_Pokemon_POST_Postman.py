from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Route for POST request to insert data into the PostgreSQL database
@app.route('/insert_data', methods=['POST'])
def post_pokemon():
    if request.method == 'POST':
        try:
            # Extracting data from the request body
            id = request.json.get('id')
            pokemon_number = request.json.get('pokemon_number')
            pokemon_name = request.json.get('pokemon_name')
            pokemon_type = request.json.get('pokemon_type')
            notes = request.json.get('notes')

            # Connect to the database
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='sqa123',
                host='10.0.30.245',
                port='5432'
            )

            # Create a cursor object to execute SQL queries
            cur = conn.cursor()

            # Execute the INSERT query with data from the request #thiss is in table Post gress  pokemon_dvalenzuela (id, pokemon_number, pokemon_name, pokemon_type, notes)
            cur.execute("""
                INSERT INTO pokemon_dvalenzuela (id, pokemon_number, pokemon_name, pokemon_type, notes) 
                VALUES (%s, %s, %s, %s, %s);
            """, (id, pokemon_number, pokemon_name, pokemon_type, notes))

            # Commit the transaction
            conn.commit()

            # Close the cursor and connection
            cur.close()
            conn.close()

            # Return a success message
            return jsonify({'message': 'Data inserted successfully'}), 201
        except Exception as e:
            # If an error occurs, rollback the transaction and return an error message
            conn.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        # Return a method not allowed error if the request method is not POST
        return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)
