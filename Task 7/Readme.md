## 🖼️ Task 7 – Image Resizer & Converter (CLI Tool)
### Automated Batch Image Processing using Python & Pillow<br>
This project is part of the Elevate Labs Internship – Task 7, where the goal is to build a <b>Python-based image processing tool</b> that resizes and converts multiple images automatically.<br>
This upgraded version includes:
- Batch resizing for all images in a folder
- Progress bar using tqdm
- Maintain aspect ratio
- Auto-detect landscape/portrait orientation
- Quality control for JPEG/WEBP
- Bulk rename support
- Choose custom width & height
- Full CLI tool using argparse

---

### 🌟 Features

### Batch Image Resizing
Automatically reads all images from:
```bash
input_images/
```
Processes them and saves output to:
```bash
output_images/
```
### Maintain Aspect Ratio
Fits images inside a bounding box without stretching:
```bash
--keep-aspect
```

### Auto Orientation
Adapts size based on image orientation:
```bash
--auto-orientation
```

### Bulk Rename

rename files like:
```bash
sample_pic_001.jpg
sample_pic_002.jpg
```
use:
```bash
--rename-prefix sample_pic
```

### Choose Output Format
Supports:
- JPEG
- PNG
- WEBP
- BMP
<br>
Example:

```bash
-f PNG
```

### Quality Control
Lower quality = smaller file size:
```bash
-q 70
```

### progress Bar
Uses tqdm for real-time progress during processing.

---

## 📂 Project Structure
```bash
Task 7/
│── image_tool.py
│── input_images/        # place original images here
│── output_images/       # auto-created, contains resized images
└── Demo Screenshots/    # contains Camparision of Input and Output Images and Screenshots of CLI
```
---

## ⚙️ Installation
Install dependencies:
```bash
pip install pillow tqdm
```
## ▶️ How to Run the Tool
1️⃣ Basic resize (800×800 JPEG)
```bash
python image_tool.py
```
2️⃣ Keep aspect ratio
```bash
python image_tool.py --keep-aspect
```
3️⃣ Keep aspect + auto orientation
```bash
python image_tool.py --keep-aspect --auto-orientation
```
4️⃣ Custom size and format
```bash
python image_tool.py -W 1024 -H 1024 -f PNG
```
5️⃣ Reduce quality
```bash
python image_tool.py -q 60
```
6️⃣ Bulk rename
```bash
python image_tool.py --rename-prefix photo
```
---

### 🎯 Outcome

By completing this task, I gained experience with:
- CLI app development
- Image processing with Pillow
- Argument parsing using argparse
- Batch task automation
- File I/O operations
- Progress bar integration
A valuable skill for automation, image ML pipelines, and backend utilities.

---

### 👨‍💻 Author
Kethari Madhu Sudhan Reddy<br>
Python Developer • Data Analyst • AIML Engineer<br>
maddoxer143@gmail.com

### 📜 License

This project is an Open Source — use it freely!