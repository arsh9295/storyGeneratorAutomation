import tkinter as tk
from tkinter import ttk, Text, filedialog
import sys
import os
from tkinter import messagebox
import subprocess
import re

class SettingsWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("500x300")
        self.window.configure(bg="#f0f0f0")
        
        # Center the settings window
        self.center_window()
        
        # Make it modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        
        # Load current settings
        self.load_current_settings()

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Secret Key
        ttk.Label(main_frame, text="API Key:").grid(row=0, column=0, sticky=tk.E, pady=(0, 10))
        self.secret_key_var = tk.StringVar()
        self.secret_key_entry = ttk.Entry(main_frame, textvariable=self.secret_key_var, width=40)
        self.secret_key_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 10), padx=(10, 0))
        
        # Output Path
        ttk.Label(main_frame, text="Output Path:").grid(row=1, column=0, sticky=tk.E, pady=(0, 20))
        self.output_path_var = tk.StringVar()
        self.output_path_entry = ttk.Entry(main_frame, textvariable=self.output_path_var, width=40)
        self.output_path_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 20), padx=(10, 0))
        
        # Browse button
        browse_button = ttk.Button(main_frame, text="Browse", command=self.browse_output_path)
        browse_button.grid(row=1, column=2, padx=(5, 0))
        
        # Update Button
        update_button = ttk.Button(main_frame, text="Update Settings", command=self.update_settings)
        update_button.grid(row=2, column=0, columnspan=3, pady=20)

    def browse_output_path(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_path_var.set(folder_path)

    def load_current_settings(self):
        try:
            backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Backend')
            main_script_path = os.path.join(backend_dir, 'main.py')
            
            with open(main_script_path, 'r') as file:
                content = file.read()
                
                # Find the API key
                api_key_match = re.search(r"geminiKey\s*=\s*['\"]([^'\"]*)['\"]", content)
                if api_key_match:
                    self.secret_key_var.set(api_key_match.group(1))
                
                # Find the output path
                output_path_match = re.search(r"outputPath\s*=\s*['\"]([^'\"]*)['\"]", content)
                if output_path_match:
                    self.output_path_var.set(output_path_match.group(1))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load current settings: {str(e)}")

    def update_settings(self):
        try:
            backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Backend')
            main_script_path = os.path.join(backend_dir, 'main.py')
            
            with open(main_script_path, 'r') as file:
                content = file.read()
            
            # Update the API key
            content = re.sub(
                r"(geminiKey\s*=\s*)['\"]([^'\"]*)['\"]",
                f"\\1'{self.secret_key_var.get()}'",
                content
            )
            
            # Update the output path
            content = re.sub(
                r"(outputPath\s*=\s*)['\"]([^'\"]*)['\"]",
                f"\\1'{self.output_path_var.get()}'",
                content
            )
            
            with open(main_script_path, 'w') as file:
                file.write(content)
            
            messagebox.showinfo("Success", "Settings updated successfully!")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update settings: {str(e)}")

class StoryGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Story Generator")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Center the window on screen
        self.center_window()

        # Set theme
        style = ttk.Style()
        style.theme_use('clam')
          # Configure styles
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        style.configure('TCombobox', padding=5, font=('Helvetica', 10))
        style.configure('TButton', padding=10, font=('Helvetica', 10, 'bold'))
        
        # Settings button style
        style.configure('Settings.TButton', padding=8)
        style.configure('Settings.TButton', font=('Helvetica', 10, 'bold'))
        style.map('Settings.TButton',
                 background=[('!active', '#4a90e2'), ('active', '#357abd')],
                 foreground=[('!active', 'white'), ('active', 'white')])

        self.create_widgets()

    def center_window(self):
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate x and y coordinates for the window
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2        # Set the position of the window to the center of the screen
        self.root.geometry(f"800x600+{x}+{y}")
        
    def create_widgets(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Settings button in the top-right corner
        settings_button = ttk.Button(
            main_frame, 
            text="⚙ Settings", 
            style='Settings.TButton',
            command=self.open_settings
        )
        settings_button.grid(row=0, column=1, sticky="NE", padx=5, pady=5)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Center the main frame
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create a fixed-width inner frame for consistent layout
        inner_frame = ttk.Frame(main_frame)
        inner_frame.grid(row=0, column=0, sticky=(tk.N, tk.S))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Language selection
        ttk.Label(inner_frame, text="Story Language:").grid(row=0, column=0, sticky=tk.E, pady=(0, 5))
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(inner_frame, textvariable=self.language_var, width=40)
        self.language_combo['values'] = ('English', 'Spanish', 'French', 'German', 'Italian')
        self.language_combo.grid(row=0, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        self.language_combo.set('English')

        # Story type selection
        ttk.Label(inner_frame, text="Story Type:").grid(row=1, column=0, sticky=tk.E, pady=(0, 5))
        self.story_type_var = tk.StringVar()
        self.story_type_combo = ttk.Combobox(inner_frame, textvariable=self.story_type_var, width=40)
        self.story_type_combo['values'] = ('Supernatural', 'Horror', 'Crime', 'Romance', 'Adventure', 'Science Fiction')
        self.story_type_combo.grid(row=1, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        self.story_type_combo.set('Supernatural')

        # Story duration selection
        ttk.Label(inner_frame, text="Story Duration:").grid(row=2, column=0, sticky=tk.E, pady=(0, 5))
        self.duration_var = tk.StringVar()
        self.duration_combo = ttk.Combobox(inner_frame, textvariable=self.duration_var, width=40)
        self.story_type_combo['values'] = ('Short', 'Medium', 'Long', 'Very Short', 'Very Long')
        # self.duration_combo['values'] = ('5 minutes', '10 minutes', '15 minutes', '20 minutes', '30 minutes')
        self.duration_combo.grid(row=2, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        self.duration_combo.set('Short')

        # AI Model selection
        ttk.Label(inner_frame, text="AI Model:").grid(row=3, column=0, sticky=tk.E, pady=(0, 5))
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(inner_frame, textvariable=self.model_var, width=40)
        self.model_combo['values'] = ('gemini-2.0-flash', 'GPT-4', 'GPT-3.5', 'Claude', 'PaLM')
        self.model_combo.grid(row=3, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        self.model_combo.set('gemini-2.0-flash')

        # Description
        ttk.Label(inner_frame, text="Description:").grid(row=4, column=0, sticky=tk.NE, pady=(10, 5))
        self.description_text = Text(inner_frame, height=4, width=50, font=('Helvetica', 10))
        self.description_text.grid(row=4, column=1, sticky=tk.W, pady=(10, 5), padx=(10, 0))

        # Prompt
        ttk.Label(inner_frame, text="Prompt:").grid(row=5, column=0, sticky=tk.NE, pady=(10, 5))
        self.prompt_text = Text(inner_frame, height=4, width=50, font=('Helvetica', 10))
        self.prompt_text.grid(row=5, column=1, sticky=tk.W, pady=(10, 5), padx=(10, 0))

        # Generate Button
        generate_button = ttk.Button(inner_frame, text="Generate Story", command=self.generate_story)
        generate_button.grid(row=6, column=0, columnspan=2, pady=20)        # Configure grid weights for inner_frame
        inner_frame.grid_columnconfigure(1, weight=1)

    def get_settings(self):
        try:
            backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Backend')
            main_script_path = os.path.join(backend_dir, 'main.py')
            
            with open(main_script_path, 'r') as file:
                content = file.read()
                
                # Find the API key
                api_key_match = re.search(r"geminiKey\s*=\s*['\"]([^'\"]*)['\"]", content)
                api_key = api_key_match.group(1) if api_key_match else ""
                
                # Find the output path
                output_path_match = re.search(r"outputPath\s*=\s*['\"]([^'\"]*)['\"]", content)
                output_path = output_path_match.group(1) if output_path_match else ""
                
                return api_key, output_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")
            return "", ""

    def generate_story(self):
        language = self.language_var.get()
        story_type = self.story_type_var.get()
        duration = self.duration_var.get()
        ai_model = self.model_var.get()
        description = self.description_text.get("1.0", tk.END).strip()
        prompt = self.prompt_text.get("1.0", tk.END).strip()
          # Get current settings
        api_key, output_path = self.get_settings()

        # Validate required inputs
        if not all([language, story_type, duration, ai_model, api_key, output_path]):
            messagebox.showerror("Error", "Please fill in all required fields (Language, Type, Duration, AI Model) and configure settings (API Key and Output Path)")
            return

        try:
            # Get the path to main.py
            backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Backend')
            main_script = os.path.join(backend_dir, 'main.py')            # Run the backend script with arguments            # Build command with required arguments
            command = [
                sys.executable,
                main_script,
                '--language', language,
                '--type', story_type,
                '--duration', duration,
                '--model', ai_model,
                '--api-key', api_key,
                '--output-path', output_path
            ]
            
            # Add optional arguments if they are provided
            if description.strip():
                command.extend(['--description', description])
            if prompt.strip():
                command.extend(['--prompt', prompt])
            
            subprocess.run(command)
            messagebox.showinfo("Success", "Story generation process started!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_settings(self):
        SettingsWindow(self.root)

def main():
    root = tk.Tk()
    app = StoryGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
