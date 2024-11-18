# lights-out-pygame
A version of the game Lights Out created with Pygame and using linear algebra notions

## Python script
You can find in the repo the Python script to execute the game in a Python interpreter :
```bash
python3 LightsOut_KevinPETIT.py
```

Before playing this way, you might need to install the required packages in your Python environment the following way :
```bash
pip install -r requirements.txt
```

## Executables
You can also simply dowload the executable of the game:
- download and extract the .tar.gz archive if you are on Linux
- download and extract the .zip if you are on Windows

## The game itself

The game is powered by Pygame for Python. The goal is to turn off all the yellow lights on the grid by clicking them: clicking a light changes its status and those of all the surrounding lights in a cross shape. 

You can play on 3x3, 4x4 and 5x5 grids to change the level of difficulty. If at any given point you're having trouble solving the grid, you can toggle on and off the solution to see which lights need to be pressed. When you have finished, you can simply start a new random game by selecting a grid size of quit the app.

This game was an interesting way to put in practice different concepts of linear algebra seen during my studies.
