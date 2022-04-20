import tkinter as tk
from tkinter import filedialog, messagebox
from types import MethodType
from optimizer import Optimizer


class OptimizerApp:
    """This app allows the user to select images to optimize and the destination folder to save the optimized images.
    The images are optimzied for web. Most images are reduced to around 25kb in size with the default settings."""
    _root: tk.Tk
    _number_images_label: tk.StringVar
    _finished_directory_label: tk.StringVar
    _optimizer: Optimizer
    _images_selected_paths: list
    _destination_path: str
    _minimum_dimension: int

    def __init__(self) -> None:
        self._root = tk.Tk()
        self._init_variables()
        self._apply_settings("Image Optimizer for Web", 400, 230)

        self._add_label("Images Directory:", 10, 20)
        self._add_textvar_label(self._number_images_label, 110, 20)
        self._add_button(self._add_images_path, "Select Files", 10, 40)

        self._add_label("Finished Directory:", 10, 80)
        self._add_textvar_label(self._finished_directory_label, 115, 80)
        self._add_button(self._add_finished_path, "Select Folder", 10, 100)

        self._add_label("Minimum px dimension:", 10, 140)
        self._number_text_input(10, 160)

        self._add_button(self._optimize, "Start Optimization", 10, 190, background="#83C12E")

    def run(self) -> None:
        """Run the application."""
        self._root.mainloop()

    def _init_variables(self) -> None:
        """Initialize strings."""
        self._images_selected_paths = []
        self._destination_path = ""
        self._optimizer = Optimizer()
        self._minimum_dimension = 600
        self._number_images_label = tk.StringVar(value=self._format_files_selected_text())
        self._finished_directory_label = tk.StringVar(value="No directory selected")

    def _apply_settings(self, title: str, width: int, height: int) -> None:
        """Apply settings to the root window.

            Arguments:
                `title` (str): The title of the window.
                `width` (int): The width of the window.
                `height` (int): The height of the window."""
        self._root.title(title)
        self._root.geometry(f"{width}x{height}")
        self._root.configure(background="#E6E6E6")

    def _add_button(self, command: MethodType, text: str, x: int, y: int, textcolor: str = "white", background: str = "#006EB4", padding: int = 5) -> None:
        """Add a button to the root window

            Arguments:
                `command` (MethodType): The command to execute when the button is clicked.
                `text` (str): The text of the button.
                `x` (int): The x coordinate of the button.
                `y` (int): The y coordinate of the button.
                `textcolor` (str): The text color of the button. Defaults to white.
                `background` (str): The background color of the button. Defaults to black.
                `padding` (int): The padding of the button. Defaults to 5."""
        button = tk.Button(self._root, text=text, command=command, foreground=textcolor, background=background, border=0, padx=padding, pady=padding)
        button.place(x=x, y=y)

    def _add_label(self, text: str, x: int, y: int) -> None:
        """Add a label to the root window.

            Arguments:
                `text` (str): The text of the label.
                `x` (int): The x coordinate of the label.
                `y` (int): The y coordinate of the label."""
        label = tk.Label(self._root, text=text, background="#E6E6E6")
        label.place(x=x, y=y)

    def _add_textvar_label(self, textvar: tk.StringVar, x: int, y: int) -> None:
        """Add a textvariable label to the root window.

            Arguments:
                `textvar` (tk.StringVar): The textvariable of the label.
                `x` (int): The x coordinate of the label.
                `y` (int): The y coordinate of the label."""
        label = tk.Label(self._root, textvariable=textvar, background="#E6E6E6")
        label.place(x=x, y=y)

    def _add_images_path(self) -> None:
        """Add path to images directory."""
        files = filedialog.askopenfilenames(filetypes=[("Image Files", ("*.jpg", "*.jpeg", "*.png", "*.webp", ".tiff"))],)
        self._images_selected_paths.clear()
        for file in files:
            self._images_selected_paths.append(file)

        self._number_images_label.set(self._format_files_selected_text())

    def _number_text_input(self, x: int, y: int) -> None:
        """Add a text input to the root window. The input is a number.
        The number is used as the minimum dimension of the image.

            Arguments:
                `x` (int): The x coordinate of the text input.
                `y` (int): The y coordinate of the text input."""
        register = self._root.register(self._validate_number)

        dimension_entry = tk.Entry(self._root, width=10)
        dimension_entry.place(x=x, y=y)
        dimension_entry.insert(0, 600)
        dimension_entry.config(validate="key", validatecommand=(register, "%P"))

    def _add_finished_path(self) -> None:
        """Add path to images directory."""
        self._destination_path = filedialog.askdirectory()
        self._finished_directory_label.set(self._destination_path)

    def _format_files_selected_text(self) -> str:
        """Format the text of the label.

        Returns:
            case 1: if there are no files selected. Returns `"No files selected"`.
            case 2: if there is one file selected. Returns `"1 file selected"`.
            case 3: if there are more than one files selected. Returns `"x files selected"`."""
        number_of_files = len(self._images_selected_paths)

        if number_of_files == 0:
            return "No files selected"
        elif number_of_files == 1:
            return "1 file selected"
        else:
            return f"{number_of_files} files selected"

    def _alert_box(self, message: str, type: str) -> None:
        """Create an alert box.

            Arguments:
                `message` (str): The message to display in the alert box.
                `type` (str): The type of alert box. Can be `info`, `warning` or `error`."""
        match type:
            case "info":
                messagebox.showinfo("Image Optimizer for Web", message)
            case "warning":
                messagebox.showwarning("Image Optimizer for Web", message)
            case "error":
                messagebox.showerror("Image Optimizer for Web", message)

    def _check_optimize_requirements(self) -> bool:
        """Check if the requirements for optimization are met.

            Returns: `bool`
                `True` if the requirements are met. `False` otherwise."""
        if len(self._images_selected_paths) == 0:
            self._alert_box("No images selected", "error")
            return False
        if self._destination_path == "":
            self._alert_box("No directory selected", "error")
            return False
        if self._minimum_dimension <= 0:
            self._alert_box("Minimum dimension must be greater than 0", "error")
            return False

        return True

    def _optimize(self) -> None:
        """Optimize images."""
        status = self._check_optimize_requirements()
        if status is False:
            return

        percentage_saved = self._optimizer.optimize_images(self._images_selected_paths, self._destination_path, self._minimum_dimension)
        self._alert_box(f"{percentage_saved} of size was reduced", "info")

    def _validate_number(self, input: str) -> bool:
        """Validate the input of the number entry. Only allows numbers

            Arguments:
                `input` (str): The input to validate."""
        if input == "":
            self._minimum_dimension = 0
            return True

        if input.isnumeric() is False:
            return False

        self._minimum_dimension = int(input)
        return True
