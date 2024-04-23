from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Route for DELETE request to delete data from the PostgreSQL database based on pokemon_number
@app.route('/delete_data', methods=['DELETE'])
def delete_data():
    if request.method == 'DELETE':
        try:
            # Extracting data from the request body
            pokemon_number = request.json.get('pokemon_number')

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

            # Execute the DELETE query with data from the request
            cur.execute("""
                DELETE FROM pokemon_dvalenzuela
                WHERE pokemon_number = %s;
            """, (pokemon_number,))

            # Commit the transaction
            conn.commit()

            # Close the cursor and connection
            cur.close()
            conn.close()

            # Return a success message
            return jsonify({'message': 'Data deleted successfully'}), 200
        except Exception as e:
            # If an error occurs, rollback the transaction and return an error message
            conn.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        # Return a method not allowed error if the request method is not DELETE
        return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)
