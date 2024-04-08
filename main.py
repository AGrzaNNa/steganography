import tkinter as tk
from tkinter import filedialog
from stegano import lsb
from cryptography.fernet import Fernet

class Steganography:
    """A class for hiding and extracting text using steganography."""
    def __init__(self, master):
        """Initialize the Steganography tool GUI.

        Args:
            master (tk.Tk): The parent Tkinter window.
        """
        self.master = master
        self.master.title("Steganography Tool")

        self.text_label = tk.Label(self.master, text="Enter text to hide:")
        self.text_label.pack()

        self.text_entry = tk.Text(self.master, height=5, width=50)
        self.text_entry.pack()

        self.hide_button = tk.Button(self.master, text="Hide Text", command=self.hide_text)
        self.hide_button.pack()

        self.extract_button = tk.Button(self.master, text="Extract Text", command=self.extract_text)
        self.extract_button.pack()

        self.result_label = tk.Label(self.master, text="")
        self.result_label.pack()

    def hide_text(self):
        """Hide text inside an image."""
        image_path = filedialog.askopenfilename(title="Select Image File")
        if not image_path:
            return

        text = self.text_entry.get("1.0", "end-1c")
        if not text:
            self.result_label.config(text="Error: Text field is empty")
            return

        try:
            key = Fernet.generate_key()
            cipher_key = Fernet(key)
            encrypted_text = cipher_key.encrypt(text.encode())
            img = lsb.hide(image_path, encrypted_text.decode())
            img.save("hidden_image.png")
            with open('key.txt', 'wb') as key_file:
                key_file.write(key)
            self.result_label.config(text="Text hidden successfully in hidden_image.png")
        except Exception as e:
            self.result_label.config(text=f"Error: {e}")

    def extract_text(self):
        """Extract hidden text from an image."""
        image_path = filedialog.askopenfilename(title="Select Image File")
        if not image_path:
            return

        try:
            with open('key.txt', 'rb') as key_file:
                key = key_file.read()
                cipher_key = Fernet(key)
                extracted_text = lsb.reveal(image_path)
                decrypted_text = cipher_key.decrypt(extracted_text.encode()).decode()
                self.result_label.config(text=f"Extracted text: {decrypted_text}")
        except Exception as e:
            self.result_label.config(text=f"Error: {e}")

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = Steganography(root)
    root.mainloop()

if __name__ == "__main__":
    main()
