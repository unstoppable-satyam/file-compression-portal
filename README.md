<div align="center">
  <h1 align="center">📊 Data Compression & Decompression Portal 📊</h1>
  <p align="center">
    <em>An interactive web tool to compress, decompress, and visually compare the performance of various data compression algorithms.</em>
    <br />
    <br />
    <a href="https://file-compression-portal.onrender.com"><strong>View Live Demo »</strong></a>
  </p>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn">
</p>

---

### 📝 About The Project

This web application is a fully functional Data Compression & Decompression Portal built using Python and Flask. It allows users to upload any file (text, image, or binary), compress it using multiple industry-standard algorithms, and visualize the results. The portal provides a side-by-side comparison of the effectiveness and performance of different compression techniques, including Run-Length Encoding (RLE), LZ77 (via zlib), and Huffman coding. Users can also upload a previously compressed file to decompress it and retrieve the original data, byte-for-byte. The primary goal is to serve as an educational tool to demonstrate and compare the efficiency of various compression algorithms in a hands-on manner.


![image](https://github.com/user-attachments/assets/1c43fe58-bfa7-4e97-8a81-0232af7d106c)

---

### ✨ Key Features

* **📁 Universal File Handling**: Upload any file type—text, images, or raw binary data.
* **🔬 Multi-Algorithm Comparison**: Simultaneously compress using **RLE**, **LZ77**, and **Huffman Coding**.
* **🔄 Full Compression/Decompression Cycle**: Complete, lossless round-trip from original to compressed and back to the original file.
* **📈 Detailed Performance Statistics**: Instantly view and compare:
    * Original vs. Compressed File Size
    * Compression Ratio
    * Processing Time (in milliseconds)
* **📊 Result Visualization**: A dynamic bar chart provides an immediate visual comparison of algorithm effectiveness.
* **🎓 Educational Explanations**: In-app "Learn More" sections detail how each algorithm works, its pros, and its cons.
* **🔗 Automated Extension Handling**: Intelligently preserves and restores the original file extension upon decompression.
* **✅ Robust Error Handling**: Clear, user-friendly feedback for common errors.

---

### 🛠️ Tech Stack

This project is built with a simple and powerful set of technologies:

* **Backend**:
    * **Python**: The core programming language.
    * **Flask**: A lightweight web framework for routing and handling requests.
    * **Gunicorn**: A robust WSGI server for running the application in production.
    * **Compression Libraries**:
        * `zlib` (for LZ77)
        * `dahuffman` (for Huffman Coding)
* **Frontend**:
    * **HTML5 & CSS3**: For structure and custom styling.
    * **JavaScript**: For dynamic client-side interactions.
    * **Chart.js**: For rendering the visualization chart.

---

### 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

<details>
  <summary><strong>Click to expand Setup Instructions</strong></summary>
  
  1.  **Clone the Repository**
      ```sh
      git clone https://github.com/unstoppable-satyam/file-compression-portal.git
      cd file-compression-portal 
      ```

  2.  **Create and Activate a Virtual Environment**
      Using a virtual environment is highly recommended to manage dependencies cleanly.
      ```sh
      # For Windows
      python -m venv venv
      venv\Scripts\activate
      
      # For macOS/Linux
      python3 -m venv venv
      source venv/bin/activate
      ```

  3.  **Install Dependencies**
      This project's dependencies are listed in `requirements.txt`.
      ```sh
      pip install -r requirements.txt
      ```

  4.  **Run the Flask Application**
      This command starts the local development server.
      ```sh
      python app.py
      ```

  5.  **Open in Browser**
      Navigate to the following address in your web browser:
      <http://127.0.0.1:5000>
</details>

---

### 🌐 Live Demo

You can access a live-hosted version of this application here:

[**https://file-compression-portal.onrender.com**](https://file-compression-portal.onrender.com)

---

### 📜 License

Distributed under the MIT License. See `LICENSE.txt` for more information.
