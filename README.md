Data Compression & Decompression Portal
Project Description
This web application is a fully functional Data Compression & Decompression Portal built using Python and Flask. It allows users to upload any file (text, image, or binary), compress it using multiple industry-standard algorithms, and visualize the results. The portal provides a side-by-side comparison of the effectiveness and performance of different compression techniques, including Run-Length Encoding (RLE), LZ77 (via zlib), and Huffman coding. Users can also upload a previously compressed file to decompress it and retrieve the original data, byte-for-byte. The primary goal is to serve as an educational tool to demonstrate and compare the efficiency of various compression algorithms in a hands-on manner.

Features
This application includes a comprehensive set of features to provide a complete and informative user experience:

Universal File Upload: Users can upload any type of file, including text, images, and binary files, for compression.

Multiple Compression Algorithms: The portal supports three distinct compression algorithms for comparison:

Run-Length Encoding (RLE)

LZ77 (via zlib)

Huffman Coding

Compression & Decompression: Full end-to-end functionality to both compress original files and decompress the portal's processed files to retrieve the original.

Detailed Compression Statistics: After compression, the application displays a detailed table with key performance metrics for each algorithm, including:

Original File Size

Compressed File Size

Compression Ratio

Processing Time (in milliseconds)

Download Functionality: Users can download both the compressed files and the final decompressed files.

In-App Algorithm Explanations: The results page features expandable sections that provide brief, user-friendly descriptions of how each algorithm works, its strengths, and its weaknesses, fulfilling the educational goal of the project.

Result Visualization: A dynamic bar chart on the results page provides an immediate visual comparison of the file sizes produced by each algorithm against the original.

Robust Error Handling: The application provides user-friendly feedback for common errors, such as failing to upload a file or attempting to decompress an invalid file format.

Automated Extension Handling: The portal intelligently packages the original file extension into the compressed filename and automatically restores it upon decompression, providing a seamless user experience.

Tech Stack Used
Backend: Python

Web Framework: Flask

Compression Libraries: zlib (for LZ77), dahuffman (for Huffman Coding), custom implementation for RLE.

Frontend:

HTML5

CSS3 (for custom styling)

JavaScript

Visualization Library: Chart.js

Production Server: Gunicorn

Setup Instructions to Run Locally
To set up and run this project on your local machine, please follow these steps:

Clone the Repository

git clone <your-github-repository-link>
cd compression_portal

Create a Virtual Environment (Recommended)
It's best practice to create a virtual environment to manage project dependencies.

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install Dependencies
The required Python libraries are listed in the requirements.txt file. Install them using pip:

pip install -r requirements.txt

Run the Application
Once the dependencies are installed, you can start the Flask development server:

python app.py

Access the Portal
The server will start and be running in debug mode. You can access the web application by opening your web browser and navigating to:
http://127.0.0.1:5000

Deployed Demo Link
You can access a live-hosted version of this application here:
https://file-compression-portal.onrender.com