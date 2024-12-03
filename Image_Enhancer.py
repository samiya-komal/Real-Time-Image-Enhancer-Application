# Importing Libraries
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np
from skimage import restoration

class ImageEnhancerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Image Enhancer")
        self.root.geometry("1100x700")
        self.root.configure(bg="#2e2e2e")

        # Frame for control panel
        self.control_frame = tk.Frame(self.root, bg="#393939", width=300)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Frame for image display
        self.image_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Labels and Canvases
        self.before_label = tk.Label(self.image_frame, text="Before", bg="#2e2e2e", fg="white", font=("Arial", 12))
        self.before_label.grid(row=0, column=0, pady=5)

        self.after_label = tk.Label(self.image_frame, text="After", bg="#2e2e2e", fg="white", font=("Arial", 12))
        self.after_label.grid(row=0, column=1, pady=5)

        # Canvas for original and processed images
        self.canvas_size = (400, 350)
        self.before_canvas = tk.Canvas(self.image_frame, bg="#1e1e1e", width=self.canvas_size[0], height=self.canvas_size[1])
        self.before_canvas.grid(row=1, column=0, padx=10, pady=10)

        self.after_canvas = tk.Canvas(self.image_frame, bg="#1e1e1e", width=self.canvas_size[0], height=self.canvas_size[1])
        self.after_canvas.grid(row=1, column=1, padx=10, pady=10)

        self.original_image = None
        self.processed_image = None
        self.loaded_image = None
        self.add_controls()

    def add_controls(self):
        load_button = ttk.Button(self.control_frame, text="Load Image", command=self.load_image)
        load_button.pack(pady=10, fill=tk.X)

        self.brightness_slider = self.add_slider("Brightness", self.adjust_brightness)
        self.contrast_slider = self.add_slider("Contrast", self.adjust_contrast)
        self.sharpness_slider = self.add_slider("Sharpness", self.adjust_sharpness)
        self.saturation_slider = self.add_slider("Saturation", self.adjust_saturation)
        self.deblur_slider = self.add_slider("Deblur Strength", self.update_deblur)
        self.deblur_slider.set(0)
        self.iteration_slider = self.add_slider("Clarity", self.update_deblur)
        self.iteration_slider.set(15)
        self.iteration_slider.config(from_=1, to=50)

        save_button = ttk.Button(self.control_frame, text="Save Image", command=self.save_image)
        save_button.pack(pady=10, fill=tk.X)

    def add_slider(self, label, command):
        tk.Label(self.control_frame, text=label, bg="#393939", fg="#ffffff", font=("Arial", 10)).pack(pady=5)
        slider = ttk.Scale(self.control_frame, from_=0, to=2, orient="horizontal", command=command)
        slider.set(1)
        slider.pack(pady=5, fill=tk.X)
        return slider

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if not file_path:
            return
        self.original_image = Image.open(file_path)
        self.original_image.thumbnail(self.canvas_size)
        self.processed_image = self.original_image.copy()
        self.loaded_image = cv2.imread(file_path)
        self.display_image(self.original_image, self.before_canvas)

    def display_image(self, image, canvas):
        canvas_image = ImageTk.PhotoImage(image)
        canvas.delete("all")
        canvas.create_image(self.canvas_size[0] // 2, self.canvas_size[1] // 2, anchor=tk.CENTER, image=canvas_image)
        canvas.image = canvas_image

    def adjust_brightness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.processed_image = enhancer.enhance(float(value))
            self.display_image(self.processed_image, self.after_canvas)

    def adjust_contrast(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Contrast(self.original_image)
            self.processed_image = enhancer.enhance(float(value))
            self.display_image(self.processed_image, self.after_canvas)

    def adjust_sharpness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Sharpness(self.original_image)
            self.processed_image = enhancer.enhance(float(value))
            self.display_image(self.processed_image, self.after_canvas)

    def adjust_saturation(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Color(self.original_image)
            self.processed_image = enhancer.enhance(float(value))
            self.display_image(self.processed_image, self.after_canvas)

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg")])
            if file_path:
                self.processed_image.save(file_path)

    def update_deblur(self, event=None):
        if self.loaded_image is not None:
            blur_strength = self.deblur_slider.get()
            iterations = self.iteration_slider.get()
            deblurred_image = self.deblur_image(self.loaded_image, blur_strength, iterations)
            deblurred_image = (deblurred_image * 255).astype(np.uint8)
            deblurred_image = Image.fromarray(deblurred_image)
            deblurred_image.thumbnail(self.canvas_size)
            self.display_image(deblurred_image, self.after_canvas)

    def deblur_image(self, image, blur_strength, iterations):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) / 255.0
            psf_size = int(3 + blur_strength)
            psf = self.create_gaussian_psf(psf_size)
            deblurred_channels = []
            for channel in range(image.shape[2]):
                try:
                    iterations = max(1, int(iterations))
                    deblurred_channel = restoration.richardson_lucy(image[:, :, channel], psf, num_iter=iterations)
                    deblurred_channels.append(deblurred_channel)
                except Exception as e:
                    print(f"Error during deblurring: {e}")
            deblurred_image = np.stack(deblurred_channels, axis=-1)
            return np.clip(deblurred_image, 0, 1)

    def create_gaussian_psf(self, size, sigma=2):
            psf = cv2.getGaussianKernel(size, sigma) @ cv2.getGaussianKernel(size, sigma).T
            return psf / psf.sum()
            
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEnhancerApp(root)
    root.mainloop()
