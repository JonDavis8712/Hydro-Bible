# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS # Import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing requests from any origin.
          # For production, you might want to restrict this to your app's domain.

# The parts data (as provided by you)
parts_data = [
    {'PartNumber': '3A004', 'NomenClature': 'Pressure Reducer', 'NSN': '4820-00-991-0785'},
    {'PartNumber': 'PD60', 'NomenClature': 'Plug', 'NSN': '5340-00-682-1857'},
    {'PartNumber': '52-27-17', 'NomenClature': 'Aircraft Airframe Structural Components (FSC 1650)', 'NSN': '1650-00-566-3329'},
    {'PartNumber': '52-27-20', 'NomenClature': 'LOCK NUT', 'NSN': ''},
    {'PartNumber': '52-27-18', 'NomenClature': 'Coil, Flat, Leaf, and Wire Springs (FSC 5360)', 'NSN': ''},
    {'PartNumber': '92-07-11', 'NomenClature': 'SPRING', 'NSN': '5360-01-377-7249'},
    {'PartNumber': '52-27-19', 'NomenClature': 'RETAINER', 'NSN': '4820-00-566-3331'},
    {'PartNumber': 'MS28774-116', 'NomenClature': 'PACKING RETAINER', 'NSN': '5330-00-582-2111'},
    {'PartNumber': 'M83461/1-116', 'NomenClature': 'PREFORMED PACKING', 'NSN': '5330-00-291-3284'},
    {'PartNumber': 'M83461/1-013', 'NomenClature': 'PACKING, PREFORMED', 'NSN': '5331-01-088-6108'},
    {'PartNumber': '71-07-17', 'NomenClature': 'DASHPOT', 'NSN': '1650-00-859-9720'},
    {'PartNumber': '71-07-12', 'NomenClature': 'PLUNGER', 'NSN': '5340-01-110-8287'},
    {'PartNumber': '52 27-23', 'NomenClature': 'BEARING, BALL', 'NSN': '3110-01-246-2436'},
    {'PartNumber': '71-07-16-2', 'NomenClature': 'FITTING', 'NSN': '4820-00-013-3541'},
    {'PartNumber': 'MS28774-006', 'NomenClature': 'RETAINER,PACKING', 'NSN': '5330-00-057-5709'},
    {'PartNumber': 'M83461/1-006', 'NomenClature': 'O-RING', 'NSN': '5331-00-595-6325'},
    {'PartNumber': 'MS28774-012', 'NomenClature': 'PACKING RETAINER', 'NSN': '5330-00-543-7090'},
    {'PartNumber': 'M83461/1-012', 'NomenClature': 'O-RING', 'NSN': '5331-01-335-8010'},
    {'PartNumber': '3A004-102', 'NomenClature': 'Signs, Advertising Displays, and Identification Plates (FSC 9905)', 'NSN': ''},
    {'PartNumber': '3A016-11', 'NomenClature': 'VALVE, REGULATING, FLUID PRESSURE', 'NSN': '4820-00-983-3598'},
    {'PartNumber': 'AN535-00-2', 'NomenClature': 'SCREW, DRIVE', 'NSN': '5305-00-253-5603'},
    {'PartNumber': '3A004-101', 'NomenClature': 'VALVE BODY', 'NSN': '01-562-9438'},
    {'PartNumber': '3A016 10', 'NomenClature': 'VALVE, REGULATING, FLUID PRESSURE', 'NSN': '4820-00-983-3598'},
    {'PartNumber': '9776461-10', 'NomenClature': 'KIT', 'NSN': '4820-00-870-4223'},
    {'PartNumber': '9776508-10', 'NomenClature': 'KIT', 'NSN': '4820-00-065-3578'}
]

@app.route('/')
def home():
    """A simple route to check if the API is running."""
    return jsonify({"message": "Parts API is running!"})

@app.route('/parts', methods=['GET'])
def get_all_parts():
    """Returns all parts in the dataset."""
    return jsonify(parts_data)

@app.route('/part/<string:part_number_req>', methods=['GET'])
def get_part_by_number(part_number_req):
    """Returns a specific part by its PartNumber.
    Handles URL decoding for part numbers that might contain spaces.
    """
    # The part_number_req comes URL decoded from Flask routing.
    part = next((p for p in parts_data if p['PartNumber'] == part_number_req), None)
    if part:
        return jsonify(part)
    else:
        return jsonify({"error": "Part not found"}), 404

@app.route('/parts/search', methods=['GET'])
def search_parts():
    """
    Searches parts based on query parameters:
    - nsn: Exact match for NSN
    - nomenclature: Case-insensitive keyword search in NomenClature
    - partnumber: Exact match for PartNumber
    Returns a list of matching parts.
    """
    query_nsn = request.args.get('nsn')
    query_nomenclature = request.args.get('nomenclature')
    query_partnumber = request.args.get('partnumber')

    results = []

    if not any([query_nsn, query_nomenclature, query_partnumber]):
        return jsonify({"error": "Please provide a search query (nsn, nomenclature, or partnumber)"}), 400

    # Iterate through a copy of parts_data for filtering
    current_results = list(parts_data)

    if query_partnumber:
        current_results = [p for p in current_results if p.get('PartNumber') == query_partnumber]

    if query_nsn:
        current_results = [p for p in current_results if p.get('NSN') == query_nsn]

    if query_nomenclature:
        current_results = [
            p for p in current_results
            if p.get('NomenClature') and query_nomenclature.lower() in p['NomenClature'].lower()
        ]
    
    results = current_results
    return jsonify(results)

# This is for local development. Render will use Gunicorn or another WSGI server.
if __name__ == '__main__':
    # Runs the Flask development server.
    # Debug=True is helpful for development as it provides detailed error messages
    # and auto-reloads the server when code changes. Do NOT use debug=True in production.
    app.run(debug=True, port=5000)
