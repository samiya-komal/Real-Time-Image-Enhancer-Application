# Importing Libraries

import tkinter as tk    # For creating the GUI interface.
from tkinter import filedialog, ttk  # For creating the user interface and handling file dialogs
from PIL import Image, ImageTk, ImageEnhance    # Pillow (PIL) for image processing. 
import cv2  # OpenCV module for advanced image processing, particularly Gaussian kernel generation and image handling.
import numpy as np # For numerical operations
from skimage import restoration # For deblurring images using Richardson-Lucy deconvolution.


# Main class

class ImageEnhancerApp:
    # Constructor method for initializing an instance of the class 
    def __init__(self, root):
        self.root = root
        self.root.title("Real Time Image Enhancer")  # Set the title of the application
        self.root.geometry("1100x700")  # Set the size of the app 
        self.root.configure(bg="#2e2e2e")   # Set the background color of the app

        # Creating a section(frame) for the buttons and controls
        self.control_frame = tk.Frame(self.root, bg="#393939", width=300)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # # Create a canvas to display the image
        self.canvas = tk.Canvas(self.root, bg="#1e1e1e", width=800, height=700)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initializing Variables to hold the images: original, processed, and loaded for deblurring
        self.original_image = None
        self.processed_image = None
        self.loaded_image = None  # For deblurring
        self.image_on_canvas = None

        # Add the buttons and sliders for user controls
        self.add_controls()


    # function initializes and adds UI components to the control frame.
    def add_controls(self):
        # Load Image Button
        load_button = ttk.Button(self.control_frame, text="Load Image", command=self.load_image)
        load_button.pack(pady=10, fill=tk.X)

        # Brightness Slider
        self.brightness_slider = self.add_slider("Brightness", self.adjust_brightness)

        # Contrast Slider
        self.contrast_slider = self.add_slider("Contrast", self.adjust_contrast)

        # Sharpness Slider
        self.sharpness_slider = self.add_slider("Sharpness", self.adjust_sharpness)

        # Saturation Slider
        self.saturation_slider = self.add_slider("Saturation", self.adjust_saturation)

        # Deblur Strength Slider
        self.deblur_slider = self.add_slider("Deblur Strength", self.update_deblur)
        self.deblur_slider.set(0)  # Sets the initial slider value to 0, meaning no deblurring effect is applied by default.

        # Iterations Slider for deblurring: 
        # To adjust the clarity of the deblurring effect by specifying the number of iterations for the Richardson-Lucy deconvolution algorithm.
        self.iteration_slider = self.add_slider("Clarity", self.update_deblur)
        self.iteration_slider.set(15) # Default value
        self.iteration_slider.config(from_=1, to=50)  # Range for iterations from 1 to 50

        # Save Image Button
        save_button = ttk.Button(self.control_frame, text="Save Image", command=self.save_image)
        save_button.pack(pady=10, fill=tk.X)
    

    # Function to create slider labeles and links it to a callback function for interactive adjustments.
    def add_slider(self, label, command):   
        tk.Label(self.control_frame, text=label, bg="#393939", fg="#ffffff", font=("Arial", 10)).pack(pady=5)    # Adds a label above the slider
        slider = ttk.Scale(self.control_frame, from_=0, to=2, orient="horizontal", command=command) # Creates a horizontal slider  
        slider.set(1)  # Default value
        slider.pack(pady=5, fill=tk.X)  # To place the slider within the layout to expand horizontally.
        return slider


    # Function to load an image   
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])   # Opens a file dialog to load an image in JPG, PNG, or JPEG format. 
        if not file_path:
            return
        self.original_image = Image.open(file_path)
        self.original_image.thumbnail((800, 700))
        self.processed_image = self.original_image.copy()
        self.loaded_image = cv2.imread(file_path)  # For deblurring
        self.display_image(self.original_image)


    # Function to display an image on the Tkinter canvas.
    def display_image(self, image):
        self.image_on_canvas = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.create_image(400, 350, anchor=tk.CENTER, image=self.image_on_canvas)


    # Function to adjust the brightness of the original image based on the slider value
    def adjust_brightness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Brightness(self.original_image)   # Create a brightness enhancer object
            self.processed_image = enhancer.enhance(float(value))   # Apply the enhancement using the given value
            self.display_image(self.processed_image)    # Update the displayed image


    # Function to adjust the contrast of the original image based on the slider value
    def adjust_contrast(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Contrast(self.original_image)   # Create a contrast enhancer object
            self.processed_image = enhancer.enhance(float(value))   # Apply the enhancement using the given value
            self.display_image(self.processed_image)    # Update the displayed image


    # Function to adjust the sharpness of the original image based on the slider value
    def adjust_sharpness(self, value):
        if self.original_image: 
            enhancer = ImageEnhance.Sharpness(self.original_image)  # Create a sharpness enhancer object
            self.processed_image = enhancer.enhance(float(value))   # Apply the enhancement using the given value
            self.display_image(self.processed_image)    # Update the displayed image


    # Function to adjust the saturation(color intensity) of the original image based on the slider value
    def adjust_saturation(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Color(self.original_image)  # Create a saturation enhancer object
            self.processed_image = enhancer.enhance(float(value))   # Apply the enhancement using the given value
            self.display_image(self.processed_image)    # Update the displayed image


    # Function that save the processed image to a file after user confirmation
    def save_image(self):
        if self.processed_image:
            # Prompt the user to choose a save location and file format
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg")])
            if file_path:
                self.processed_image.save(file_path)    # Save the processed image to the specified path


    # Deblur-related methods: Gaussian Point Spread Function (PSF) for deblurring
    def create_gaussian_psf(self, size, sigma=2):
        psf = cv2.getGaussianKernel(size, sigma) @ cv2.getGaussianKernel(size, sigma).T # Generate a 2D Gaussian kernel
        return psf / psf.sum()  # Normalize the kernel to ensure it sums to 1


    #  Function to apply the Richardson-Lucy deblurring algorithm on an image. It processes each color channel (Red, Green, Blue) individually and attempts to remove blur caused by a point spread function (PSF).
    def deblur_image(self, image, blur_strength, iterations):
    # image: The input image to be deblurred, blur_strength: A value that controls the strength of the blur. Higher values increase the blur size.
    # iterations: The number of iterations the deblurring algorithm should run. More iterations generally lead to better results.

        # Convert the image from BGR to RGB and normalize the pixel values to the range [0, 1]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) / 255.0  

        # Calculate the PSF size based on the blur strength, increasing the size for stronger blur
        psf_size = int(3 + blur_strength)

         # Generate the Point Spread Function (PSF) using a Gaussian kernel
        psf = self.create_gaussian_psf(psf_size)

        # Initialize a list to store the deblurred channels (RGB channels)
        deblurred_channels = []

        # Loop over each color channel (R, G, B) to apply deblurring individually
        for channel in range(image.shape[2]):
            try:
                # Ensure the number of iterations is an integer and is at least 1
                iterations = int(iterations)  
                if iterations < 1:
                    iterations = 1  # Minimum 1 iteration

                # Apply the Richardson-Lucy deblurring algorithm to each channel with the calculated PSF
                deblurred_channel = restoration.richardson_lucy(image[:, :, channel], psf, num_iter=iterations)

                # Append the deblurred channel to the list
                deblurred_channels.append(deblurred_channel)

            except Exception as e:
                print(f"Error during deblurring: {e}")
                # Handle the error or revert to a previous image state

        # Stack the deblurred channels (R, G, B) back into a single image
        deblurred_image = np.stack(deblurred_channels, axis=-1)

        # Ensure the pixel values are in the valid range [0, 1] and return the deblurred image
        return np.clip(deblurred_image, 0, 1)



    # Function handles the real-time update of an image's deblurring effect in the user interface based on user input through the sliders for blur strength and iterations.
    def update_deblur(self, event=None):
        # Check if an image is loaded for deblurring
        if self.loaded_image is not None:
            # Get the current values for blur strength and number of iterations from the sliders
            blur_strength = self.deblur_slider.get()    
            iterations = self.iteration_slider.get()

            # Perform the deblurring operation on the loaded image using the selected parameters
            deblurred_image = self.deblur_image(self.loaded_image, blur_strength, iterations)

            # Convert the deblurred image back to the range [0, 255] and change to uint8 for display
            deblurred_image = (deblurred_image * 255).astype(np.uint8)

            # Convert the deblurred image to a PIL Image object
            deblurred_image = Image.fromarray(deblurred_image)

            # Resize the deblurred image to fit within the canvas (800x700 maximum size)
            deblurred_image.thumbnail((800, 700))

            # Display the deblurred image on the canvas
            self.display_image(deblurred_image)


# Initializes the tkinter root window and runs the app.
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEnhancerApp(root)
    root.mainloop()
