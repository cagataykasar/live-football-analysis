from flask import Flask, render_template, request, jsonify, send_file
import time
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Predefined tags
TAGS = [
    "OYUN KURMA", "KARŞILAMA - BASKI", "GEÇİŞ-HÜCUM",
    "GEÇİŞ-SAVUNMA", "GOLLER", "DURAN TOPLAR"
]

# Timer variables
timer_running = False
start_time = 0
elapsed_time = 0

# XML Data
xml_root = ET.Element("file")

sort_info = ET.SubElement(xml_root, "SORT_INFO")
ET.SubElement(sort_info, "sort_type").text = "sort order"

all_instances = ET.SubElement(xml_root, "ALL_INSTANCES")
instance_counter = 0  # ID counter

@app.route('/')
def index():
    return render_template("index.html", tags=TAGS)

@app.route('/start_timer', methods=['POST'])
def start_timer():
    global timer_running, start_time
    if not timer_running:
        start_time = time.time() - elapsed_time
        timer_running = True
    return jsonify({"status": "started"})

@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    global timer_running, elapsed_time
    if timer_running:
        elapsed_time = time.time() - start_time
        timer_running = False
    return jsonify({"status": "stopped", "elapsed_time": elapsed_time})

@app.route('/reset_timer', methods=['POST'])
def reset_timer():
    global timer_running, start_time, elapsed_time
    timer_running = False
    start_time = 0
    elapsed_time = 0
    return jsonify({"status": "reset"})

@app.route('/add_tag', methods=['POST'])
def add_tag():
    new_tag = request.json.get("tag")
    if new_tag and new_tag not in TAGS:
        TAGS.append(new_tag)
    return jsonify(TAGS)

@app.route('/delete_tag', methods=['POST'])
def delete_tag():
    tag_to_delete = request.json.get("tag")
    if tag_to_delete in TAGS:
        TAGS.remove(tag_to_delete)
    return jsonify(TAGS)


@app.route('/get_time', methods=['GET'])
def get_time():
    if timer_running:
        current_time = time.time() - start_time
    else:
        current_time = elapsed_time
    return jsonify({"time": round(current_time, 3)})

@app.route('/add_instance', methods=['POST'])
def add_instance():
    global instance_counter

    data = request.json
    tag = data.get("tag")
    click_time = data.get("time")

    if tag not in TAGS:
        return jsonify({"error": "Invalid tag"}), 400

    start_time = round(click_time - 5, 3)
    end_time = round(click_time + 10, 3)

    # Create new instance
    instance = ET.SubElement(all_instances, "instance")
    ET.SubElement(instance, "ID").text = str(instance_counter)
    ET.SubElement(instance, "code").text = tag
    ET.SubElement(instance, "start").text = str(start_time)
    ET.SubElement(instance, "end").text = str(end_time)

    label = ET.SubElement(instance, "label")
    ET.SubElement(label, "group").text = "Event"
    ET.SubElement(label, "text").text = tag

    instance_counter += 1  # Increment ID

    return jsonify({"status": "added", "ID": instance_counter - 1})

@app.route('/download_xml', methods=['GET'])
def download_xml():
    xml_tree = ET.ElementTree(xml_root)
    xml_path = "generated.xml"

    # Pretty print XML formatting
    from xml.dom import minidom
    xml_str = minidom.parseString(ET.tostring(xml_root)).toprettyxml(indent="  ")

    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_str)

    return send_file(xml_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)