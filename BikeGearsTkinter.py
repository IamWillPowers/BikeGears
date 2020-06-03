import tkinter as tk

WHEEL_SIZE = 25  # g= d (f/r)

gearset = {
    'Shimano 2x Road': {
        'chainring': {
            '53-39': (53, 39),
            '52-36': [52, 36],
            '50-34': [50, 34]
            },
        'cassette': {
            '11-34': [11, 34],
            '11-32': [11, 12, 13, 14, 16, 18, 20, 22, 25, 28, 32],
            '11-28': [11, 12, 13, 14, 15, 17, 19, 21, 23, 25, 28]
            }
        },
    'Shimano 1x Gravel': {
        'chainring': {
            '46': [46],
            '36': [36],
            '34': [34]},
        'cassette': {
            '11-36': [11, 12, 13, 14, 15, 36],
            '11-42': [11, 14, 15, 19, 42]
            }
        },
    'SRAM 2x Road': {
        'chainring': {
            '53-39': [53, 39],
            '52-36': [52, 36],
            '50-34': [50, 34]
            },
        'cassette': {
            '11-28': [11, 12, 20, 21, 22, 23, 24, 25, 26, 27, 28],
            '11-32': [11, 20, 21, 22, 23, 24, 25, 26, 27, 30, 32],
            '11-36': [11, 13, 15, 17, 19, 22, 25, 28, 32, 36]
            }
        },
    'SRAM 1x Gravel': {
        'chainring': {
            '36': [36],
            '40': [40],
            '42': [42]
            },
        'cassette': {
            '10-26': [10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 23, 26],  # range %260
            '10-28': [10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 24, 28],  # range %280
            '10-33': [10, 11, 12, 13, 14, 15, 17, 19, 21, 24, 28, 33], # range %330
            '10-36': [10, 11, 12, 13, 15, 17, 19, 21, 24, 28, 32, 36], # range %360
            '10-42': [10, 12, 14, 16, 18, 21, 24, 28, 32, 36, 42],
            '10-50': [10, 12, 14, 16, 18, 21, 24, 28, 32, 36, 42, 50]
            }
    },
    'Rotor 1x': {
        'chainring': {
            '54': [54],
            '52': [52],
            '50': [50],
            '48': [48],
            '46': [46],
            '44': [44],
            '42': [42],
            '40': [40],
            '38': [38]
        },
        'cassette': {
            '10-36': [10, 36],
            '10-39': [10, 39],
            '10-46': [10, 46],
            '10-52': (10, 52),
            '11-36': [11, 36],
            '11-39': [11, 39],
            '11-46': [11, 46],
            '11-52': [11, 52]
            }
        }
}


def build_ui():
    root = tk.Tk()
    root.title("Bicycle Gear Ratio Visualizer")
    # root.iconbitmap('cog.ico')
    root.geometry("800x400")

    brandOptions = sorted(list(gearset.keys()))
    brandSelection = tk.StringVar(root)
    brandSelection.set(brandOptions[0])

    tk.Label(root, text='Chainring:').grid(row=1, column=0, sticky=tk.E)
    chainringOptions = sorted(list(gearset[brandSelection.get()]['chainring'].keys()))
    chainringSelection = tk.StringVar(root)
    chainringSelection.set(chainringOptions[0])
    chainringOptions = tk.OptionMenu(root, chainringSelection, *chainringOptions)
    chainringOptions.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    tk.Label(root, text='Cassette:').grid(row=2, column=0, sticky=tk.E)
    cassetteOptions = sorted(list(gearset[brandSelection.get()]['cassette'].keys()))
    cassetteSelection = tk.StringVar(root)
    cassetteSelection.set(cassetteOptions[0])
    cassetteOptions = tk.OptionMenu(root, cassetteSelection, *cassetteOptions)
    cassetteOptions.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

    # Have to initialize brand menu last so that it has access to other option menus
    tk.Label(root, text='Brand:').grid(row=0, column=0, sticky=tk.E)
    brandOptions = tk.OptionMenu(root, brandSelection, *brandOptions,
                                 command=lambda val: brandChanged(val, chainringOptions, chainringSelection,
                                                                  cassetteOptions, cassetteSelection))
    brandOptions.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

    resultString = tk.StringVar()
    tk.Label(root, textvariable=resultString).grid(row=4, column=0, columnspan=2)

    tk.Button(root, text="Compute Gear Inch",
              command=lambda: computeResult(
                  resultString,
                  # for some reason selections are list of strings so need to convert back to int (stupid tkinter)
                  gearset[brandSelection.get()]['chainring'][chainringSelection.get()],
                  gearset[brandSelection.get()]['cassette'][cassetteSelection.get()])).grid(row=3, column=1)
    root.mainloop()


# found at https://stackoverflow.com/questions/17580218/changing-the-options-of-a-optionmenu-when-clicking-a-button
def setOptionMenuData(optionMenu, selection, newOptions):
    # It is actually insane that this is how you reset the data here
    optionMenu['menu'].delete(0, 'end')
    selection.set(newOptions[0])
    for option in newOptions:
        optionMenu['menu'].add_command(label=option, command=tk._setit(selection, option))


"""
Callback for when the gear options are changed
"""


def brandChanged(brandOption, chainringOptions, chainringSelection, cassetteOptions, cassetteSelection):
    setOptionMenuData(chainringOptions, chainringSelection, sorted(list(gearset[brandOption]['chainring'].keys())))
    setOptionMenuData(cassetteOptions, cassetteSelection, sorted(list(gearset[brandOption]['cassette'].keys())))


"""
Accepts a list of gears, selecting the mins and maxs
Return the low and high gear in inches distance traveled per pedal stroke
"""


def gearInchLow(chainring, cassette):
    crankMin = min(chainring)
    cassetteMax = max(cassette)
    return WHEEL_SIZE * (crankMin / cassetteMax)  # 24.488 for 700 rim diameter
    # this gives back the inches distance traveled per pedal stroke


"""
Returns the inches distance traveled per pedal stroke
"""


def gearInchHigh(chainring, cassette):
    crankMax = max(chainring)
    cassetteMin = min(cassette)
    return WHEEL_SIZE * (crankMax / cassetteMin)


def computeResult(resultString, chainringSelection, cassetteSelection):
    gLow = gearInchLow(chainringSelection, cassetteSelection)
    gHigh = gearInchHigh(chainringSelection, cassetteSelection)
    resultString.set('Your gear inch are ' + ("{0:.1f}".format(gLow)) + ' to ' + ("{0:.1f}".format(gHigh)))


if __name__ == '__main__':
    build_ui()

"""
This has been a Will + Cole app.
MANY THANKS TO COLE STEWART FOR WRITING THE LAMBDA FUNCTION PART (plus more),
and thank you to Code in Place for making this possible :)
"""