import tkinter as tk
from tkinter import filedialog
import Jobs
from PIL import Image, ImageTk

HEIGHT = 600
WIDTH = 1200

# Setting the colors
mainColor = "#202020"
darkColor = "#1b1b1b"
accentColor = "#00d0ff"
placeholderColor = "#ff00ff"

buttonTextColor = "white"
grayedTextColor = "#303030"

def load_main_window(path):

    HEIGHT = 600
    WIDTH = 1200

    frames = Jobs.load_sequence(path)

    rootWindow = tk.Tk()

    previewFrame = tk.Frame(rootWindow)
    previewFrame.place(relwidth=0.7, relheight=0.95)
    previewDisplay = tk.Label(previewFrame)
    previewDisplay.pack(fill="both")

    previewImageImport = Image.open(frames[0]["file"])
    previewImage = ImageTk.PhotoImage(previewImageImport)
    # previewDisplay = tk.Label(previewFrame, image=previewImage)
    # previewDisplay.pack(fill="both", side="left")

    playheadFrame = tk.Frame(rootWindow)
    playheadFrame.place(rely=0.95, relwidth=0.7, relheight=0.05)

    frameSlider = tk.Scale(playheadFrame, from_=1, to_=len(frames), orient="horizontal", width=400)
    frameSlider.pack(fill="both")

    settingsFrame = tk.Frame(rootWindow)
    settingsFrame.place(relx=0.7, relwidth=0.3, relheight=1)
    settingsCanvas = tk.Canvas(settingsFrame)
    settingsCanvas.place(relwidth=1, relheight=0.9)
    scrollbar = tk.Scrollbar(settingsFrame, orient="vertical")
    scrollbar.place(anchor="ne", relx=1, relheight=0.9)
    renderButtonsFrame = tk.Frame(settingsFrame)
    renderButtonsFrame.place(rely=0.9, relwidth=1, relheight=0.1)

    # for nr in list(range(0, 50)):
    #     labelSpam = tk.Label(settingsCanvas, text=str(nr))
    #     labelSpam.grid(row=nr, column=0)

    # The list of options
    # Subdivision
    tk.Label(settingsCanvas, text="Subdivision").grid(row=0, column=0)
    subdivEntryText = tk.IntVar()
    subdivEntry = tk.Entry(settingsCanvas, width=4, textvariable=subdivEntryText, justify="center")
    subdivEntry.grid(row=1, column=0)
    subdivSlider = tk.Scale(settingsCanvas, from_=0, to_=10, orient="horizontal", showvalue=0)
    subdivSliderValue = tk.IntVar()
    subdivSlider.config(variable=subdivSliderValue)
    subdivSlider.set(4)
    subdivSlider.grid(row=1, column=1)
    cubicCheckState = tk.IntVar(0)
    cubicCheck = tk.Checkbutton(settingsCanvas)
    cubicCheck.grid(row=2, column=0)
    tk.Label(settingsCanvas, text="Use cubic regression").grid(row=2, column=1)

    # Feathering
    tk.Label(settingsCanvas, text=" ").grid(row=4, column=0)
    tk.Label(settingsCanvas, text="Feathering").grid(row=5, column=0)
    featherEntryText = tk.StringVar()
    featherEntry = tk.Entry(settingsCanvas, width=4, textvariable=featherEntryText, justify="center")
    featherEntry.grid(row=6, column=0)
    featherSlider = tk.Scale(settingsCanvas, from_=0, to_=10, orient="horizontal", showvalue=0)
    featherSliderValue = tk.IntVar()
    featherSlider.config(variable=featherSliderValue)
    featherSlider.set(2)
    featherSlider.grid(row=6, column=1)


    tk.Label(settingsCanvas, text=" ").grid(row=7, column=0)

    # Eye animation selection
    tk.Label(settingsCanvas, text="Eyes").grid(row=8, column=0)

    leftEyeButton = tk.Button(settingsCanvas, text="...")
    leftEyeButton.grid(row=9, column=0)
    leftEyeEntryText = tk.StringVar()
    leftEyeEntryText.set("Left eye")
    leftEyeEntry = tk.Entry(settingsCanvas, textvariable=leftEyeEntryText)
    leftEyeEntry.grid(row=9, column=1)

    rightEyeButton = tk.Button(settingsCanvas, text="...")
    rightEyeButton.grid(row=10, column=0)
    rightEyeEntryText = tk.StringVar()
    rightEyeEntryText.set("Right eye")
    rightEyeEntry = tk.Entry(settingsCanvas, textvariable=rightEyeEntryText)
    rightEyeEntry.grid(row=10, column=1)

    # Reverse and flip options
    eyeEditFrame = tk.Frame(settingsCanvas, height=20, width=100)
    eyeEditFrame.grid(row=11, columnspan=2)
    tk.Label(eyeEditFrame, text="Left Eye ").grid(row=0, column=1)
    tk.Label(eyeEditFrame, text=" Right Eye").grid(row=0, column=2)
    tk.Label(eyeEditFrame, text="Mirror").grid(row=1, column=0)
    tk.Label(eyeEditFrame, text="Reverse").grid(row=2, column=0)
    tk.Label(eyeEditFrame, text="A-sync").grid(row=3, column=0)

    # Reverse
    leftReverseCheckState = tk.IntVar(0)
    leftReverseCheck = tk.Checkbutton(eyeEditFrame, variable=leftReverseCheckState)
    leftReverseCheck.grid(row=1, column=1)

    rightReverseCheckState = tk.IntVar(0)
    rightReverseCheck = tk.Checkbutton(eyeEditFrame, variable=rightReverseCheckState)
    rightReverseCheck.grid(row=1, column=2)

    # Mirror
    leftMirrorCheckState = tk.IntVar(0)
    leftMirrorCheck = tk.Checkbutton(eyeEditFrame, variable=leftMirrorCheckState)
    leftMirrorCheck.grid(row=2, column=1)

    rightMirrorCheckState = tk.IntVar(0)
    rightMirrorCheck = tk.Checkbutton(eyeEditFrame, variable=rightMirrorCheckState)
    rightMirrorCheck.grid(row=2, column=2)

    # A-Synchronus
    leftASyncCheckState = tk.IntVar(0)
    leftASyncCheck = tk.Checkbutton(eyeEditFrame, variable=leftASyncCheckState)
    leftASyncCheck.grid(row=3, column=1)

    rightASyncCheckState = tk.IntVar(0)
    rightASyncCheck = tk.Checkbutton(eyeEditFrame, variable=rightASyncCheckState)
    rightASyncCheck.grid(row=3, column=2)


    # Master changes

    for child in settingsCanvas.winfo_children():
        child.config(
            #highlightthickness=0,
        )
        try:
            child.config(
                # activebackground=child.cget("bg"),
                justify="center",
                # troughcolor=mainColor
            )
        except:
            None
        if "scale" in str(child):
            child.config(
                length=250
            )
            # print("Set value of "+str(child))


    settingsCanvas.config(yscrollcommand=scrollbar.set, scrollregion=settingsCanvas.bbox("all"))
    scrollbar.config(command=settingsCanvas.yview)

    bakeButton = tk.Button(renderButtonsFrame, text="Bake")
    # bakeButton.pack(side="left", fill="both", expand=True)
    bakeButton.place(relx=0.0625, rely=0.2, relwidth=0.25, relheight=0.6)

    refineButton = tk.Button(renderButtonsFrame, text="Refine")
    # renderButton.pack(side="left", fill="both", expand=True)
    refineButton.place(relx=0.375, rely=0.2, relwidth=0.25, relheight=0.6)

    renderButton = tk.Button(renderButtonsFrame, text="Save")
    # renderButton.pack(side="left", fill="both", expand=True)
    renderButton.place(relx=0.6875, rely=0.2, relwidth=0.25, relheight=0.6)

    # Setting up functionality
    # Checkboxes and sliders
    # Defining the functions
    # FIXME: These checkboxes don't check when testing on my desktop, but they do on my laptop
    def checkbox_toggle(checkbutton):
        print("Checkbox set to: "+str(checkbutton.get()))

    def slider_entry(slider, entry):
        entry.set(slider.get())
        print("Set to: "+str(slider.get())) 

    # Binding the commands
    
    for every_checkbox in settingsCanvas.winfo_children():
        if "check" in str(every_checkbox):
            every_checkbox.config(command=lambda: print("checkeroo"))

    subdivSlider.config(command=lambda x: slider_entry(subdivSliderValue, subdivEntryText))
    subdivSlider.bind("<ButtonRelease-1>", lambda x: print("Re-rendering"))
    featherSlider.config(command=lambda x: slider_entry(featherSliderValue, featherEntryText))
    featherSlider.bind("<ButtonRelease-1>", lambda x: print("Re-rendering"))

    # FIXME previewDisplay claims to be referenced before defined, despite being set up at the beginning of this definition.
    # FIXME the image in previewDisplay isn't updating.
    def update_preview(new_image_index):
        # previewImageImport = Image.open(frames[new_image_index]["file"])
        print("Loading " + str(frames[new_image_index]["file"]))
        previewImage = ImageTk.PhotoImage(previewImageImport)
        previewDisplay.pack_forget()
        previewDisplay = tk.Label(previewFrame, image=previewImage)
        previewDisplay.pack(fill="both", side="left")

    frameSlider.config(command=lambda x: update_preview(int(frameSlider.get())-1))
    frameSlider.bind("<ButtonRelease-1>", lambda x: print("Re-rendering"))

    # Printing defaults
    slider_entry(subdivSliderValue, subdivEntryText)
    slider_entry(featherSliderValue, featherEntryText)

    rootWindow.minsize(WIDTH, HEIGHT)
    rootWindow.title("Eyeless")
    rootWindow.mainloop()


def load_init_popup():
    WIDTH = 300
    HEIGHT = 100
    rootWindow = tk.Tk()

    # Giving the central elements some space
    tk.Frame(rootWindow, width=25, height=23).grid(row=0, column=0)
    tk.Frame(rootWindow, width=25, height=23).grid(row=0, column=0)

    # Creating path entry textbox
    filePath = tk.StringVar()
    pathEntry = tk.Entry(rootWindow, textvariable=filePath, width=24).grid(column=2, row=1)

    # Creating path selection button
    fileButton = tk.Button(rootWindow, text="...", command=lambda: filePath.set(filedialog.askdirectory())).grid(column=1, row=1)
    
    centerer = tk.Frame(rootWindow, height=20, width=100)
    centerer.grid(row=2, column=1, columnspan=4)

    def ok():
        if not Jobs.redo_check(filePath.get()):
            rootWindow.destroy()

    okButton = tk.Button(centerer, text="OK", command=ok).grid(column=0, row=0)

    rootWindow.minsize(WIDTH, HEIGHT)
    rootWindow.maxsize(WIDTH, HEIGHT)
    rootWindow.title("Open image sequence")
    rootWindow.mainloop()

    return(filePath.get())


if __name__ == "__main__":
    # path = load_init_popup()
    # print(path)
    # if path != "":
    #     print("Recived path: " + path)
    load_main_window("media/face_input")
