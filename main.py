from flask import Flask, request, jsonify
import psycopg2
import psycopg2.pool
import logging
from flask_cors import CORS
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', handlers=[logging.StreamHandler()])
from config import DB_CREDENTIALS

app = Flask(__name__)
CORS(app)  # Enable CORS on the Flask app
logging.basicConfig(level=logging.INFO)

# Set up a connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,  # minconn, maxconn
                                                     host=DB_CREDENTIALS['host'],
                                                     port=DB_CREDENTIALS['port'],
                                                     dbname=DB_CREDENTIALS['database'],
                                                     user=DB_CREDENTIALS['user'],
                                                     password=DB_CREDENTIALS['password'],
                                                     sslmode=DB_CREDENTIALS['sslmode'])

@app.route('/track', methods=['POST'])
def track_event():
    event_data = request.get_json()
    if not event_data:
        return jsonify({"error": "Invalid data"}), 400

    conn = connection_pool.getconn()
    if conn is None:
        logging.error("Failed to connect to the database")
        return jsonify({"error": "Database connection error"}), 500
    
    cur = conn.cursor()
    # try:
    #     cur.execute("""
    #         INSERT INTO coupons_tracking (event_type, event_name, user_id, utm_source, utm_medium, utm_campaign, utm_content, time_of_event, event_url, app)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #     """, (
    #         event_data.get('eventType'),
    #         event_data.get('eventName'),
    #         event_data.get('userId'),
    #         event_data.get('utmSource'),
    #         event_data.get('utmMedium'),
    #         event_data.get('utmCampaign'),
    #         event_data.get('utmContent'),
    #         event_data.get('timeOfEvent'),
    #         event_data.get('eventUrl'),
    #         event_data.get('appName')
    #     ))
    #     conn.commit()
    #     logging.info(event_data)
    # except Exception as e:
    #     logging.error(f"Failed to insert event data: {e}")
    #     conn.rollback()
    #     return jsonify({"error": "Failed to insert event data"}), 500
    # finally:
    #     cur.close()
    #     connection_pool.putconn(conn)
    logging.info(f"Received webhook data: {event_data}")
    return jsonify({"success": "webhook tracked succesfuly"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)