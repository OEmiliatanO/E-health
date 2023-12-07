import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
pic_folder = "/Users/liushiwen/Desktop/大四上/物件導向程式設計/E-health/CAS_STUFF/"

class EHealthSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("eHealth System")

        # Patient Picture on the Left
        self.canvas = tk.Canvas(root, width=150, height=150)
        self.canvas.grid(row=0, column=0, padx=10, pady=10, rowspan=7)

        # Patient ID Entry and Search Button
        self.patient_id_label = tk.Label(root, text="Patient ID:")
        self.patient_id_label.grid(row=0, column=1, padx=10, pady=10)

        self.patient_id_entry = tk.Entry(root)
        self.patient_id_entry.grid(row=0, column=2, padx=10, pady=10)

        self.search_button = tk.Button(root, text="Search", command=self.search_patient)
        self.search_button.grid(row=0, column=3, padx=10, pady=10)

        # Patient Information on the Right
        self.patient_info_label = tk.Label(root, text="Patient Information:")
        self.patient_info_label.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        # Description Entry and Save Button
        self.description_label = tk.Label(root, text="Write Description:")
        self.description_label.grid(row=6, column=1, padx=10, pady=10)

        self.description_entry = tk.Entry(root, width=50)
        self.description_entry.grid(row=6, column=2, padx=10, pady=10, columnspan=2)

        self.save_description_button = tk.Button(root, text="Save Description", command=self.save_description)
        self.save_description_button.grid(row=7, column=1, columnspan=3, pady=10)

    def search_patient(self):
        patient_id = self.patient_id_entry.get()
        patient_data = self.get_patient_data(patient_id)

        if patient_data:
            self.display_patient_info(patient_data)
            self.display_patient_picture(patient_id)
        else:
            messagebox.showinfo("Error", "Patient not found.")

    def get_patient_data(self, patient_id):
        # Replace this function with actual data retrieval logic
        # For simplicity, using a hardcoded patient data dictionary
        patients_data = {
            "0001": {
                "name": "Jager",
                "birthdate": "01/01/2000,01:24:00",
                "last_visit": "11/30/2023,08:04:09",
                "latest_numbers": {
                    "BMI": 0.000383673,
                    "blood_sugar": 100.0,
                    "body_fat_percentage": 15.0,
                    "estradiol": 10.2,
                    "heart_rate": 65.0,
                    "height": 1.88,
                    "testosterone": 5.5,
                    "weight": 70.0
                },
                "reports": [
                    "All numerical reports are in normal range.",
                    "A normal person.",
                    "Vitamin D tablet(10);calcium tablet(10);"
                ]
            }
        }

        return patients_data.get(patient_id)

    def display_patient_info(self, patient_data):
        info_text = f"Name: {patient_data['name']}\n"
        info_text += f"Birthdate: {patient_data['birthdate']}\n"
        info_text += f"Last Visit: {patient_data['last_visit']}\n\n"
        info_text += "Latest Numbers:\n"
        for key, value in patient_data['latest_numbers'].items():
            info_text += f"{key}: {value}\n"

        self.patient_info_label.config(text=info_text)

    def display_patient_picture(self, patient_id):
        try:
            image_path = f"{pic_folder}/pic{patient_id}.png"  # Adjust the path based on your image filenames
            image = Image.open(image_path)
            length = 128
            width = int(image.width / (image.height / length))
            image = image.resize((width, length))
            photo = ImageTk.PhotoImage(image)

            # Update the canvas with the new image
            self.canvas.config(width=image.width, height=image.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.photo = photo  # Prevent image from being garbage collected
        except FileNotFoundError:
            messagebox.showinfo("Error", f"Image not found for patient ID: {patient_id}")

    def save_description(self):
        description = self.description_entry.get()
        if description:
            messagebox.showinfo("Success", "Description saved successfully.")
            # Add logic to save the description (e.g., to a database)
        else:
            messagebox.showinfo("Error", "Please enter a description.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EHealthSystemUI(root)
    root.mainloop()
