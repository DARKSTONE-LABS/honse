import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import random
from PIL import Image
import numpy as np

class ImageCollageApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("honseLAGOOR")
        self.root.geometry("400x250")

        # Modern theme
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # Target folder selection
        self.folder_path = tk.StringVar()
        ttk.Label(self.root, text="Select Folder:").pack(pady=(10, 0))
        ttk.Entry(self.root, textvariable=self.folder_path, width=50).pack(pady=(0, 5))
        ttk.Button(self.root, text="Browse", command=self.browse_folder).pack()

        # Output settings
        ttk.Label(self.root, text="Output Quantity:").pack(pady=(10, 0))
        self.output_quantity = ttk.Entry(self.root)
        self.output_quantity.pack()

        ttk.Label(self.root, text="Output Folder Name:").pack(pady=(10, 0))
        self.output_folder_name = ttk.Entry(self.root)
        self.output_folder_name.pack()

        # Start process button
        ttk.Button(self.root, text="Start", command=self.start_processing).pack(pady=(10, 0))

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.folder_path.set(folder_selected)

    def start_processing(self):
        folder = self.folder_path.get()
        try:
            output_qty = int(self.output_quantity.get())
            output_folder = self.output_folder_name.get()
            if not folder or output_qty <= 0 or not output_folder:
                raise ValueError
            self.create_collages(folder, output_qty, output_folder)
            messagebox.showinfo("hell yeah my boi", f"{output_qty} pictur is sav in '{output_folder}'")
        except ValueError:
            messagebox.showerror("Error", "Please ensure all fields are correctly filled.")

    def create_collages(self, folder, output_qty, output_folder):
        blend_modes = ['multiply', 'screen', 'overlay']
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        for i in range(output_qty):
            images = self.get_random_images(folder, 3)
            if len(images) == 3:
                base_image = images.pop().resize((1020, 1020), Image.Resampling.LANCZOS)
                while images:
                    top_image = images.pop().resize((1020, 1020), Image.Resampling.LANCZOS)
                    mode = random.choice(blend_modes)
                    base_image = self.blend_images(base_image, top_image, mode)
                base_image.save(os.path.join(output_folder, f'collage{i}.png'))

    def get_random_images(self, folder, count):
        images = [Image.open(os.path.join(folder, img)) for img in os.listdir(folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
        random.shuffle(images)
        return images[:count] if len(images) >= count else []

    def blend_images(self, bottom_img, top_img, mode):
        bottom_img, top_img = self.match_image_modes(bottom_img, top_img)
        if mode == 'multiply':
            return Image.fromarray(np.uint8(np.array(bottom_img) * np.array(top_img) / 255))
        elif mode == 'screen':
            return Image.fromarray(np.uint8(255 - (255 - np.array(bottom_img)) * (255 - np.array(top_img)) / 255))
        elif mode == 'overlay':
            bottom = np.array(bottom_img) / 255
            top = np.array(top_img) / 255
            return Image.fromarray(np.uint8(255 * np.where(top < 0.5, 2 * bottom * top, 1 - 2 * (1 - bottom) * (1 - top))))
        else:
            return top_img

    def match_image_modes(self, img1, img2):
        if img1.mode != img2.mode:
            if img1.mode == 'RGBA':
                img2 = img2.convert('RGBA')
            elif img2.mode == 'RGBA':
                img1 = img1.convert('RGBA')
            else:
                img1 = img1.convert('RGB')
                img2 = img2.convert('RGB')
        return img1, img2

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCollageApp(root)
    root.mainloop()
