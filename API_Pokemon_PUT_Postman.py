from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Route for PUT request to update data in the PostgreSQL database
@app.route('/update_data', methods=['PUT'])
def update_data():
    if request.method == 'PUT':
        try:
            # Extracting data from the request body
            id = request.json.get('id')
            new_pokemon_name = request.json.get('new_pokemon_name')
            new_notes = request.json.get('new_notes')

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

            # Execute the UPDATE query with data from the request
            cur.execute("""
                UPDATE pokemon_dvalenzuela
                SET pokemon_name = %s, notes = %s
                WHERE id = %s;
            """, (new_pokemon_name, new_notes ,  id))

            # Commit the transaction
            conn.commit()

            # Close the cursor and connection
            cur.close()
            conn.close()

            # Return a success message
            return jsonify({'message': 'Data updated successfully'}), 200
        except Exception as e:
            # If an error occurs, rollback the transaction and return an error message
            conn.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        # Return a method not allowed error if the request method is not PUT
        return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)
