# FitGuide
FitGuide is a personalized workout recommendation system designed to adapt to your mood, weather, and calorie goals. Using the power of the Random Forest algorithm, it aims to promote a healthier lifestyle by suggesting the most suitable workouts based on your preferences. Each page of the web application is built in a separate Python file to make the development process easier, as the project is developed by a team of three people.

## Installation & Cloning
To clone this repository, use the following command:

```bash
git clone https://github.com/dewiazizah968/FitGuide.git
```

Then navigate to the project folder:

```bash
cd FitGuide
```

Make sure to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Creating an Executable (Desktop-Based Application)
To convert this project into an executable, you'll need to install PyInstaller. Run the following command to install PyInstaller:

```bash
pip install pyinstaller
```

After installation, you can create an executable file using this command:

```bash
pyinstaller --onefile --windowed --icon=ikon.ico main.py
```

### Explanation:
- `--onefile`: Bundles everything into a single executable.
- `--windowed`: Prevents opening a command prompt window when launching the application.
- `--icon=ikon.ico`: Adds a custom icon to the executable.
- `main.py`: The main Python file to be converted into an executable.

Once the process is complete, the executable file will be found in the `dist` folder.

**Note**: This application is desktop-based, meaning it does not run in a web browser.

## View the Application
To see the result directly, visit the project repository at:  
[FitGuide on GitHub](https://github.com/dewiazizah968/FitGuide)

## Contributors
Thank you to the following contributors for their work on this project:

- [Dewi](https://github.com/dewiazizah968)
- [Sheila](https://github.com/SheilaEdistya)
- [Fatimah](https://github.com/FatimahAzzaroh28)

We welcome contributions to improve FitGuide. Please feel free to fork the repository and submit a pull request.
