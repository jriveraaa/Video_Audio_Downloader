import os
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
from tkinter import messagebox

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Video Downloader")
        master.resizable(False, False)
        master.config(bg="#DBE7C9")

        self.label = tk.Label(master, text="LINK VIDEO", bg="#DBE7C9", fg="#294B29", font=("Helvetica", 20, "bold"))
        self.label.grid(row=1, column=1, padx=90, pady=30)

        self.entrada = tk.Entry(master, width=30)
        self.entrada.grid(row=2, column=1, padx=90, pady=30)

        self.videoTitle = tk.Label(master=master, text="", bg="#DBE7C9", fg="#294B29", font=("Helvetica", 12, "bold"), wraplength=190)
        self.videoTitle.grid(row=3, column=1, padx=0, pady=3)

        self.views = tk.Label(master, text="", bg="#DBE7C9", fg="#294B29", font=("Helvetica", 12, "bold"), wraplength=190)
        self.views.grid(row=4, column=1, padx=0, pady=5)

        self.download = tk.Button(master, text="Download", fg="white", bg="#4CAF50", font=("Helvetica", 12, "bold"), command=self.download_video)
        self.download.grid(row=5, column=1, padx=90, pady=30)

        self.update_labels()

    def update_labels(self):
        url = self.entrada.get()
        try:
            yt = YouTube(url)
            title = yt.title
            views = yt.views
            self.download.config(state="active")
        except Exception:
            title = "Insert a valid YouTube link"
            self.download.config(state="disabled")
            views = 0

        formatted_views = "{:,}".format(views)
        views_text = f"Views: {formatted_views} views"

        self.videoTitle.config(text=f"Title: {title}")
        self.views.config(text=views_text)

        self.master.after(1000, self.update_labels)  

    def download_video(self):
        # disables the main window while the download window is open
        download_window = tk.Toplevel(master=self.master)
        download_window.geometry("475x295")
        download_window.resizable(False, False)
        download_window.config(bg="#DBE7C9")

        tk.Label(download_window, text="Select format:", bg="#DBE7C9", fg="#294B29", font=("Helvetica", 12, "bold")).grid(row=1, column=1, padx=20, pady=30)

        selected_format = tk.StringVar(value=None)
        selected_format.set(None)

        # formats
        vid = tk.Radiobutton(download_window, text="Video", bg="#DBE7C9", fg="#294B29", font=("Helvetica", 10, "bold"), variable=selected_format, value="video")
        vid.grid(row=2, column=1, padx=20, pady=8)
        aud = tk.Radiobutton(download_window, text="Audio", bg="#DBE7C9", fg="#294B29", font=("Helvetica", 10, "bold"), variable=selected_format, value="audio")
        aud.grid(row=2, column=2, padx=20, pady=8)

        tk.Label(download_window, text="Select the route", bg="#DBE7C9", fg="#294B29", font=("Helvetica", 12, "bold")).grid(row=3, column=1, padx=20, pady=15)

        route_var = tk.StringVar()

        route_entry = tk.Entry(download_window, width=30, textvariable=route_var)
        route_entry.grid(row=3, column=2, columnspan=3, padx=20, pady=5)
        select_route = tk.Button(download_window, text="Select", command=lambda: self.select_route(route_var))
        select_route.grid(row=3, column=5, padx=5, pady=5)

        start_download_btn = tk.Button(download_window, text="Start download", fg="white", bg="#4CAF50", font=("Helvetica", 12, "bold"), command=lambda: self.start_download(selected_format, route_var, download_window))
        start_download_btn.grid(row=4, column=2, padx=10, pady=15)

        download_window.grab_set()

    def select_route(self, route_var):
        ruta = filedialog.askdirectory()

        if ruta:
            route_var.set(ruta)

    def start_download(self, selected_format, route_var, downlaod_window):
        url = self.entrada.get()
        yt = YouTube(url)

        try:
            if not os.path.isdir(route_var.get()):
                messagebox.showinfo("Please select a valid route", "Please select a valid route to save your video to continue with the download.")
                return

            if selected_format.get() == "video":
                yd = yt.streams.get_highest_resolution()
                yd.download(route_var.get())
                messagebox.showinfo("Video downloaded correctly", "The video "+ yt.title + " was downloaded correctly.\nWait a minute and go to the route " + route_var.get() + ".")
                downlaod_window.destroy()

            elif selected_format.get() == "audio":
                yd = yt.streams.get_audio_only()
                yd.download(route_var.get())
                messagebox.showinfo("Video downloaded correctly", "The video "+ yt.title + " was downloaded correctly.\nWait a minute and go to the route " + route_var.get() + ".")
                downlaod_window.destroy()

            else:
                messagebox.showinfo("Please select a format", "Please select a format to continue with the download.")
                return
            
        except Exception:
            messagebox.showerror("Error", "There was an error, please verify all the information provided was correctly and try again.")

def initiate_gui():
    root = tk.Tk()
    GUI(root)
    root.mainloop()

if __name__ == "__main__":
    initiate_gui()
