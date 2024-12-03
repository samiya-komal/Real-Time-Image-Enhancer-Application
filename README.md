# Real-Time-Image-Enhancer-Application
Real-time image enhancement app enabling users to adjust brightness, contrast, sharpness, blur, denoise, and deblur with interactive previews. Uses advanced computer vision techniques like Wiener Filtering for precise deblurring, delivering professional-quality results and an intuitive user experience.

> **Setup Instructions**
To set up and run the Image Enhancement application, follow the steps below. The application is built in Python, and the necessary dependencies are installed via pip. 

> **Step 1: Install Required Dependencies**
1.	Python 3.x: The application is compatible with Python 3 and above. You can download and install the latest version of Python from the official website: Python Download.
2.	Pip: Ensure that pip (Python package installer) is installed. It is bundled with Python by default. You can check if pip is installed by running the command: pip --version
3.	Install the required libraries using the following command:
pip install tkinter pillow numpy opencv-python scikit-image 
	OpenCV: For image processing and enhancement functionalities.
	NumPy: For numerical operations required in image manipulation.
	Pillow (PIL): For basic image loading, saving, and manipulation.
	Tkinter: For building the graphical user interface (GUI). 
	Scikit-Image: For advanced image processing tasks like deblurring.

> **Step 2: Running the Application**
1.	Once all dependencies are installed, you can run the application by navigating to the directory where the Python script is located and executing the following command:
2.	Open a terminal or command prompt in the directory where the Python script is located.
3.	Run the script using:
python image_enhancer_app.py

> **Step 3: Using the Application**
1.	Launch the application by running the script.
2.	The graphical user interface (GUI) will open.
3.	Use the "Upload Image" button to load an image from your computer.
4.	Use the sliders to adjust the image's brightness, contrast, sharpness, and saturation.
5.	Preview the adjustments in real-time on the displayed image.
6.	Once satisfied with the changes, click the "Save Image" button to store the enhanced version of the image on your computer
