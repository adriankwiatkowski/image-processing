import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename

# internal module
from image_operator import resize_image, load_image, save_image, image_to_uint8, treshold_high_image, treshold_low_image
from utils.tkinter_helper import create_button, create_label, create_slider

# Plots
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Application(tk.Frame):

    rgb_multiplier = [1.000000, 1.000000, 1.000000]
    image_path_in = 'assets/wow.jpg'
    image_path_out = 'assets/wow_out.jpg'
    width = 1920
    height = 1080
    background_color = '#110754'
    image = np.zeros(0)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH)
        self.create_widgets()
        root.configure(background=self.background_color)

    def create_widgets(self):
        # top frame
        self.frame1 = tk.Frame(self)
        self.frame1.pack(fill=tk.X)
        self.frame1.configure(background=self.background_color)
        self.pick_color_label = create_label(grid_frame=self.frame1, row=0, column=0, text='Pick color and then process image. Load and then save')

        # grid tools
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack(fill=tk.X)
        self.frame_grid.configure(background=self.background_color)

        # row 0
        self.color_picker_button = create_button(grid_frame=self.frame_grid, row=0, column=0, text='PICK COLOR', command=self.create_color_picker)
        self.rgb_multiplier_text = create_label(grid_frame=self.frame_grid, row=0, column=1)
        self.update_rgb_multiplier_text()

        # row 1
        self.load_image_button = create_button(grid_frame=self.frame_grid, row=1, column=0, text='LOAD IMAGE', command=self.open_file)
        self.save_image_button = create_button(grid_frame=self.frame_grid, row=1, column=1, text='SAVE IMAGE', command=self.save_file)

        # row 2
        self.rgb_button = create_button(grid_frame=self.frame_grid, row=2, column=0, text='MULTIPLY RGB', command=self.apply_rgb)
        self.scale_button = create_button(grid_frame=self.frame_grid, row=2, column=1, text='RESIZE', command=self.scale_image)

        # row 3
        self.width_text = create_label(grid_frame=self.frame_grid, row=3, column=0, text='Width')
        self.width_slider = create_slider(grid_frame=self.frame_grid, row=3, column=1, min=100, max=7680, start_value=self.width)

        # row 4
        self.height_text = create_label(grid_frame=self.frame_grid, row=4, column=0, text='Height')
        self.height_slider = create_slider(grid_frame=self.frame_grid, row=4, column=1, min=100, max=4320, start_value=self.height)

        # row 5
        self.treshold_high_button = create_button(grid_frame=self.frame_grid, row=5, column=0, text='TRESHOLD HIGH', command=self.apply_high_treshold)
        self.treshold_low_button = create_button(grid_frame=self.frame_grid, row=5, column=1, text='TRESHOLD LOW', command=self.apply_low_treshold)

        # row 6
        self.treshold_slider = create_slider(grid_frame=self.frame_grid, row=6, column=0, min=0, max=255, start_value=255, columnspan=2)

        # row 7
        self.quit_button = create_button(grid_frame=self.frame_grid, row=7, column=0, text='QUIT', columnspan=2, command=self.master.destroy)
        self.quit_button['bg'] = 'black'
        self.quit_button['fg'] = 'red'

        # plot figure
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.plot_canvas = FigureCanvasTkAgg(self.figure, root)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(side=tk.TOP, expand=True)

    def is_image_null(self):
        if (self.image.size <= 0):
            print('Image is null')
            return True
        return False

    def apply_high_treshold(self):
        if self.is_image_null():
            print('Cannnot apply treshold on null image')
            return

        self.image = treshold_high_image(image=self.image, treshold=self.treshold_slider.get() / 255)
        self.show_plot()

    def apply_low_treshold(self):
        if self.is_image_null():
            print('Cannnot apply treshold on null image')
            return
        
        self.image = treshold_low_image(image=self.image, treshold=self.treshold_slider.get()/ 255)
        self.show_plot()

    def apply_rgb(self):
        if self.is_image_null():
            print('Cannot rgb image. Image is null')
            return

        print('Processing RGB image...')

        img_in = self.image
        img_tinted = img_in
        img_tinted = img_in * self.rgb_multiplier
        img_tinted = resize_image(img_tinted, self.width, self.height)

        self.image = img_tinted
        self.show_plot()

    def show_plot(self):
        print('Showing image plot')
        plot_image = image_to_uint8(self.image)
        self.ax.cla()
        self.ax.imshow(plot_image)
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
        self.rgb_multiplier_text['text'] = f'RGB {self.rgb_multiplier}'

    def scale_image(self):
        if self.is_image_null():
            print('Cannot scale image. Image is null')
            return

        print('Resizing image')
        self.width = self.width_slider.get()
        self.height = self.height_slider.get()
        self.image = resize_image(self.image, self.width, self.height)
        self.show_plot()

    def open_file(self):
        file_name = askopenfilename(title = "Open file",
                                    filetypes = (
                                        ('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),
                                        ('PNG', '*.png'),
                                        ('BMP', ('*.bmp','*.jdib')),
                                        ('GIF', '*.gif')
                                    ))

        if file_name is None or file_name == '':
            print('File not loaded. User probably canceled dialog')
            return

        print(f'Loading file name {file_name}')
        self.image = load_image(file_name)

        self.show_plot()

    def save_file(self):
        print('Asking user to save file...')
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

        print(f'Saving file {file_name}')
        img_saved = save_image(file_name, self.image)
        print('Image saved!')
        return img_saved

# Initialize tkinter
root = tk.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width, height))
# root.attributes('-fullscreen', True)
app = Application(master=root)
app.mainloop()