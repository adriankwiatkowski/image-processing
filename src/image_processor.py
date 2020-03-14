import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename

# internal module
from image_operations import resize_image, load_image, save_image, show_image_plot, image_to_uint8

# Plots
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Application(tk.Frame):

    rgb_multiplier = [1, 1, 1]
    image_path_in = 'assets/wow.jpg'
    image_path_out = 'assets/wow_out.jpg'
    width = 1920
    height = 1080
    background_color = '#110754'

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH)
        self.create_widgets()
        root.configure(background=self.background_color)

    def create_widgets(self):

        self.frame1 = tk.Frame(self)
        self.frame1.pack(fill=tk.X)
        self.frame1.configure(background=self.background_color)

        self.lbl1 = tk.Label(self.frame1, text='Pick color and then process image. Load and then save')
        self.lbl1.pack(side=tk.LEFT, padx=5, pady = 5)

        self.frame2 = tk.Frame(self)
        self.frame2.pack(fill=tk.X)
        self.frame2.configure(background=self.background_color)

        self.color_picker_button = tk.Button(self.frame2, text='PICK COLOR', command=self.create_color_picker)
        self.color_picker_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.process_button = tk.Button(self.frame2, text='PROCESS IMAGE', command=self.process_image)
        self.process_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.frame3 = tk.Frame(self)
        self.frame3.pack(fill=tk.X)
        self.frame3.configure(background=self.background_color)

        self.quit = tk.Button(self.frame3, text='QUIT', bg='black', fg='red', command=self.master.destroy)
        self.quit.pack(side=tk.LEFT, padx=5, pady=5)

        self.rgb_multiplier_text = tk.Label(self.frame3)
        self.update_rgb_multiplier_text()
        self.rgb_multiplier_text.pack(side=tk.LEFT, padx=5, pady=5)

        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.plot_canvas = FigureCanvasTkAgg(self.figure, root)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(side=tk.TOP, expand=True)

    def process_image(self):
        print('Asking user to load file...')
        file_name = self.open_file()

        if file_name is None or file_name == '':
            print('File not loaded. User probably canceled dialog')
            return

        print(f'Loaded file name {file_name}')
        print('Processing image...')

        img_in = load_image(file_name)
        img_tinted = img_in
        img_tinted = img_in * self.rgb_multiplier
        img_tinted = resize_image(img_tinted, self.width, self.height)

        print('Showing image plot')
        self.show_plot(image_to_uint8(img_tinted))

        print('Asking user to save file...')
        file_name = self.save_file(img_tinted)
        print('Image saved!')

    def show_plot(self, image):
        self.ax.cla()
        self.ax.imshow(image)
        self.plot_canvas.draw()

    def create_color_picker(self):
        color = colorchooser.askcolor(title='select color')
        try:
            root.configure(background=color[1])
            color = color[0]
            self.rgb_multiplier = [color[0] / 255, color[1] / 255, color[2] / 255]
        except TypeError as e:
            print(f'User probably canceled picking color\n {e}')
            pass
        self.update_rgb_multiplier_text()

    def update_rgb_multiplier_text(self):
        self.rgb_multiplier_text['text'] = f'Color Multiplier {self.rgb_multiplier}'

    def open_file(self):
        return askopenfilename(title = "Open file",
                                    filetypes = (
                                        ('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),
                                        ('PNG', '*.png'),
                                        ('BMP', ('*.bmp','*.jdib')),
                                        ('GIF', '*.gif')
                                    ))

    def save_file(self, image):
        file_name = asksaveasfilename(title = "Save file",
                                    defaultextension='.jpg',
                                    filetypes = (
                                        ('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),
                                        ('PNG', '*.png'),
                                        ('BMP', ('*.bmp','*.jdib')),
                                        ('GIF', '*.gif')))

        if file_name is None or file_name == '':
            print('File was not selected. User probably canceled dialog')
            return

        print(f'file_name {file_name}')
        img_saved = save_image(file_name, image)
        return img_saved

# Initialize tkinter
root = tk.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width, height))
# root.attributes('-fullscreen', True)
app = Application(master=root)
app.mainloop()