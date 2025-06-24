# version 1(basic code)
'''
import os
import zlib
import pickle
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
from dahuffman import HuffmanCodec

# App configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COMPRESSED_FOLDER'] = 'compressed'
app.config['DECOMPRESSED_FOLDER'] = 'decompressed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'supersecretkey'

# Ensure all our directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECOMPRESSED_FOLDER'], exist_ok=True)

# --- COMPRESSION & DECOMPRESSION ALGORITHMS (No Changes in this section) ---

def compress_rle(data):
    if not data: return b""
    encoded = bytearray()
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i-1] and count < 255:
            count += 1
        else:
            encoded.append(count)
            encoded.append(data[i-1])
            count = 1
    encoded.append(count)
    encoded.append(data[len(data)-1])
    return bytes(encoded)

def decompress_rle(data):
    decoded = bytearray()
    i = 0
    while i < len(data):
        count = data[i]
        value = data[i+1]
        decoded.extend([value] * count)
        i += 2
    return bytes(decoded)

def compress_lz77(data):
    return zlib.compress(data)

def decompress_lz77(data):
    return zlib.decompress(data)

def compress_huffman(data):
    codec = HuffmanCodec.from_data(data)
    pickled_codec = pickle.dumps(codec)
    codec_len = len(pickled_codec).to_bytes(4, 'big')
    encoded_data = codec.encode(data)
    return codec_len + pickled_codec + encoded_data

def decompress_huffman(data):
    codec_len = int.from_bytes(data[:4], 'big')
    pickled_codec = data[4:4+codec_len]
    codec = pickle.loads(pickled_codec)
    encoded_data = data[4+codec_len:]
    return codec.decode(encoded_data)


COMPRESSION_ALGORITHMS = {
    'rle': {'compress': compress_rle, 'decompress': decompress_rle, 'extension': 'rle'},
    'lz77': {'compress': compress_lz77, 'decompress': decompress_lz77, 'extension': 'lz77'},
    'huffman': {'compress': compress_huffman, 'decompress': decompress_huffman, 'extension': 'huff'}
}

# --- FLASK ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_route():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        original_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_filepath)

        with open(original_filepath, 'rb') as f:
            original_data = f.read()
        
        original_size = len(original_data)
        results = []

        for name, methods in COMPRESSION_ALGORITHMS.items():
            compressed_data = methods['compress'](original_data)
            compressed_filename = f"{os.path.splitext(filename)[0]}_{name}.{methods['extension']}"
            compressed_filepath = os.path.join(app.config['COMPRESSED_FOLDER'], compressed_filename)
            
            with open(compressed_filepath, 'wb') as f:
                f.write(compressed_data)
            
            compressed_size = len(compressed_data)
            ratio = original_size / compressed_size if compressed_size > 0 else 0
            
            results.append({
                'algorithm': name.upper(),
                'original_size': f"{original_size / 1024:.2f} KB",
                'compressed_size': f"{compressed_size / 1024:.2f} KB",
                'compression_ratio': f"{ratio:.2f} : 1",
                'download_filename': compressed_filename
            })
            
        return render_template('results.html', results=results, original_filename=filename)

@app.route('/decompress_page')
def decompress_page():
    return render_template('decompress.html')


@app.route('/decompress', methods=['POST'])
def decompress_route():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_ext = filename.split('.')[-1]
        
        decompress_func = None
        algo_name_found = None
        for name, methods in COMPRESSION_ALGORITHMS.items():
            if methods['extension'] == file_ext:
                decompress_func = methods['decompress']
                algo_name_found = name
                break
        
        if not decompress_func:
            flash(f"Unknown compression format for file extension '.{file_ext}'")
            return redirect(url_for('decompress_page'))

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, 'rb') as f:
            compressed_data = f.read()

        try:
            decompressed_data = decompress_func(compressed_data)

            # --- THIS IS THE CORRECTED LOGIC ---
            # It re-creates a sensible original filename and adds .txt
            base_name = os.path.splitext(filename)[0] # e.g., "sample_rle"
            original_base_name = base_name.replace(f"_{algo_name_found}", "") # e.g., "sample"
            decompressed_filename = f"decompressed_{original_base_name}.txt" # e.g., "decompressed_sample.txt"
            # --- END OF CORRECTION ---

            decompressed_filepath = os.path.join(app.config['DECOMPRESSED_FOLDER'], decompressed_filename)
            
            with open(decompressed_filepath, 'wb') as f:
                f.write(decompressed_data)
            
            return send_from_directory(app.config['DECOMPRESSED_FOLDER'], decompressed_filename, as_attachment=True)
        
        except Exception as e:
            flash(f"Decompression failed. The file may be corrupt or of the wrong type. Error: {e}")
            return redirect(url_for('decompress_page'))


@app.route('/download/compressed/<filename>')
def download_compressed_file(filename):
    return send_from_directory(app.config['COMPRESSED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

'''


# version 2( modified)

'''
import os
import zlib
import pickle
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
from dahuffman import HuffmanCodec

# App configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COMPRESSED_FOLDER'] = 'compressed'
app.config['DECOMPRESSED_FOLDER'] = 'decompressed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'supersecretkey'

# Ensure all our directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECOMPRESSED_FOLDER'], exist_ok=True)

# --- COMPRESSION & DECOMPRESSION ALGORITHMS (No Changes in this section) ---
def compress_rle(data):
    # ... (same as before)
    if not data: return b""
    encoded = bytearray()
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i-1] and count < 255:
            count += 1
        else:
            encoded.append(count)
            encoded.append(data[i-1])
            count = 1
    encoded.append(count)
    encoded.append(data[len(data)-1])
    return bytes(encoded)

def decompress_rle(data):
    # ... (same as before)
    decoded = bytearray()
    i = 0
    while i < len(data):
        count = data[i]
        value = data[i+1]
        decoded.extend([value] * count)
        i += 2
    return bytes(decoded)

def compress_lz77(data):
    return zlib.compress(data)

def decompress_lz77(data):
    return zlib.decompress(data)

def compress_huffman(data):
    codec = HuffmanCodec.from_data(data)
    pickled_codec = pickle.dumps(codec)
    codec_len = len(pickled_codec).to_bytes(4, 'big')
    encoded_data = codec.encode(data)
    return codec_len + pickled_codec + encoded_data

def decompress_huffman(data):
    codec_len = int.from_bytes(data[:4], 'big')
    pickled_codec = data[4:4+codec_len]
    codec = pickle.loads(pickled_codec)
    encoded_data = data[4+codec_len:]
    return codec.decode(encoded_data)

COMPRESSION_ALGORITHMS = {
    'rle': {'compress': compress_rle, 'decompress': decompress_rle, 'extension': 'rle'},
    'lz77': {'compress': compress_lz77, 'decompress': decompress_lz77, 'extension': 'lz77'},
    'huffman': {'compress': compress_huffman, 'decompress': decompress_huffman, 'extension': 'huff'}
}

# --- FLASK ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_route():
    # ... (file checks are the same)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        original_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_filepath)

        with open(original_filepath, 'rb') as f:
            original_data = f.read()
        
        original_size = len(original_data)
        results = []

        # --- MODIFIED FILENAME LOGIC ---
        base, ext = os.path.splitext(filename)
        original_ext = ext.replace('.', '') # Get 'jpg' from '.jpg'

        for name, methods in COMPRESSION_ALGORITHMS.items():
            compressed_data = methods['compress'](original_data)
            # New filename format: basename---original_ext---algorithm.new_ext
            compressed_filename = f"{base}---{original_ext}---{name}.{methods['extension']}"
            # --- END OF MODIFICATION ---
            
            compressed_filepath = os.path.join(app.config['COMPRESSED_FOLDER'], compressed_filename)
            
            with open(compressed_filepath, 'wb') as f:
                f.write(compressed_data)
            
            compressed_size = len(compressed_data)
            ratio = original_size / compressed_size if compressed_size > 0 else 0
            
            results.append({
                'algorithm': name.upper(),
                'original_size': f"{original_size / 1024:.2f} KB",
                'compressed_size': f"{compressed_size / 1024:.2f} KB",
                'compression_ratio': f"{ratio:.2f} : 1",
                'download_filename': compressed_filename
            })
            
        return render_template('results.html', results=results, original_filename=filename)

@app.route('/decompress_page')
def decompress_page():
    return render_template('decompress.html')


@app.route('/decompress', methods=['POST'])
def decompress_route():
    # ... (file checks are the same)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file_ext = filename.split('.')[-1]
        
        decompress_func = None
        for name, methods in COMPRESSION_ALGORITHMS.items():
            if methods['extension'] == file_ext:
                decompress_func = methods['decompress']
                break
        
        if not decompress_func:
            flash(f"Unknown compression format for file extension '.{file_ext}'")
            return redirect(url_for('decompress_page'))

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, 'rb') as f:
            compressed_data = f.read()

        try:
            decompressed_data = decompress_func(compressed_data)

            # --- MODIFIED FILENAME LOGIC ---
            # Parse the filename to get the original name and extension
            parts = os.path.splitext(filename)[0].split('---')
            original_base_name = parts[0]
            original_ext = parts[1]
            decompressed_filename = f"decompressed_{original_base_name}.{original_ext}"
            # --- END OF MODIFICATION ---

            decompressed_filepath = os.path.join(app.config['DECOMPRESSED_FOLDER'], decompressed_filename)
            
            with open(decompressed_filepath, 'wb') as f:
                f.write(decompressed_data)
            
            return send_from_directory(app.config['DECOMPRESSED_FOLDER'], decompressed_filename, as_attachment=True)
        
        except Exception as e:
            flash(f"Decompression failed. The file may be corrupt or of the wrong type. Error: {e}")
            return redirect(url_for('decompress_page'))


@app.route('/download/compressed/<filename>')
def download_compressed_file(filename):
    return send_from_directory(app.config['COMPRESSED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

    
'''

# version 3 (chart plotting)
import os
import zlib
import pickle
import json
import time # Import the time module
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
from dahuffman import HuffmanCodec

# App configuration and other functions remain the same...
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COMPRESSED_FOLDER'] = 'compressed'
app.config['DECOMPRESSED_FOLDER'] = 'decompressed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'supersecretkey'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECOMPRESSED_FOLDER'], exist_ok=True)

# ALL COMPRESSION/DECOMPRESSION FUNCTIONS ARE THE SAME
def compress_rle(data):
    if not data: return b""
    encoded = bytearray()
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i-1] and count < 255:
            count += 1
        else:
            encoded.append(count)
            encoded.append(data[i-1])
            count = 1
    encoded.append(count)
    encoded.append(data[len(data)-1])
    return bytes(encoded)

def decompress_rle(data):
    decoded = bytearray()
    i = 0
    while i < len(data):
        count = data[i]
        value = data[i+1]
        decoded.extend([value] * count)
        i += 2
    return bytes(decoded)

def compress_lz77(data):
    return zlib.compress(data)

def decompress_lz77(data):
    return zlib.decompress(data)

def compress_huffman(data):
    codec = HuffmanCodec.from_data(data)
    pickled_codec = pickle.dumps(codec)
    codec_len = len(pickled_codec).to_bytes(4, 'big')
    encoded_data = codec.encode(data)
    return codec_len + pickled_codec + encoded_data

def decompress_huffman(data):
    codec_len = int.from_bytes(data[:4], 'big')
    pickled_codec = data[4:4+codec_len]
    codec = pickle.loads(pickled_codec)
    encoded_data = data[4+codec_len:]
    return codec.decode(encoded_data)

COMPRESSION_ALGORITHMS = {
    'rle': {'compress': compress_rle, 'decompress': decompress_rle, 'extension': 'rle'},
    'lz77': {'compress': compress_lz77, 'decompress': decompress_lz77, 'extension': 'lz77'},
    'huffman': {'compress': compress_huffman, 'decompress': decompress_huffman, 'extension': 'huff'}
}


@app.route('/')
def index():
    return render_template('index.html')

# --- ONLY 'compress_route' is MODIFIED ---
@app.route('/compress', methods=['POST'])
def compress_route():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        original_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_filepath)

        with open(original_filepath, 'rb') as f:
            original_data = f.read()
        
        original_size = len(original_data)
        table_results = []
        chart_labels = ['Original']
        chart_data = [original_size]

        base, ext = os.path.splitext(filename)
        original_ext = ext.replace('.', '')

        for name, methods in COMPRESSION_ALGORITHMS.items():
            # --- Start timing ---
            start_time = time.time()
            compressed_data = methods['compress'](original_data)
            end_time = time.time()
            # --- End timing ---

            processing_time = (end_time - start_time) * 1000 # Convert to milliseconds

            compressed_filename = f"{base}---{original_ext}---{name}.{methods['extension']}"
            compressed_filepath = os.path.join(app.config['COMPRESSED_FOLDER'], compressed_filename)
            
            with open(compressed_filepath, 'wb') as f:
                f.write(compressed_data)
            
            compressed_size = len(compressed_data)
            ratio = original_size / compressed_size if compressed_size > 0 else 0
            
            table_results.append({
                'algorithm': name.upper(),
                'original_size': f"{original_size / 1024:.2f} KB",
                'compressed_size': f"{compressed_size / 1024:.2f} KB",
                'compression_ratio': f"{ratio:.2f} : 1",
                'download_filename': compressed_filename,
                'processing_time': f"{processing_time:.2f} ms" # Add formatted time
            })

            chart_labels.append(name.upper())
            chart_data.append(compressed_size)
        
        return render_template('results.html', 
                               results=table_results, 
                               original_filename=filename,
                               chart_labels=json.dumps(chart_labels),
                               chart_data=json.dumps(chart_data))

# All other routes remain the same
@app.route('/decompress_page')
def decompress_page():
    return render_template('decompress.html')

@app.route('/decompress', methods=['POST'])
def decompress_route():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_ext = filename.split('.')[-1]
        
        decompress_func = None
        algo_name_found = None
        for name, methods in COMPRESSION_ALGORITHMS.items():
            if methods['extension'] == file_ext:
                decompress_func = methods['decompress']
                algo_name_found = name
                break
        
        if not decompress_func:
            flash(f"Unknown compression format for file extension '.{file_ext}'")
            return redirect(url_for('decompress_page'))

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, 'rb') as f:
            compressed_data = f.read()

        try:
            decompressed_data = decompress_func(compressed_data)
            parts = os.path.splitext(filename)[0].split('---')
            original_base_name = parts[0]
            original_ext = parts[1]
            decompressed_filename = f"decompressed_{original_base_name}.{original_ext}"

            decompressed_filepath = os.path.join(app.config['DECOMPRESSED_FOLDER'], decompressed_filename)
            
            with open(decompressed_filepath, 'wb') as f:
                f.write(decompressed_data)
            
            return send_from_directory(app.config['DECOMPRESSED_FOLDER'], decompressed_filename, as_attachment=True)
        
        except Exception as e:
            flash(f"Decompression failed. The file may be corrupt or of the wrong type. Error: {e}")
            return redirect(url_for('decompress_page'))

@app.route('/download/compressed/<filename>')
def download_compressed_file(filename):
    return send_from_directory(app.config['COMPRESSED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)