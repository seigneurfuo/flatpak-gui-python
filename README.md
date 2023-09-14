# Flatpak GUI
![](docs/imgs/2023-06-05_14-37-26.png)

## Features
- English translation
- French translation
- Search for installed / list available applications
- Search for installed / list available runtimes
- Install and remove applications
- Launch an installed application

## How to use ?
1. Clone this repository

2. Install the required dependencies.

3. Open a terminal in the f* At the moment, it's the only way to launch the app. In the future, I will make a script to launch it.

4. Launch **src/app.py** with Python3:

   ```sh
   python3 src/app.py
   ```

### Dependencies
- Python 3
- PyQt6


## TODO
- List repos
- Show History
- Add more tools to the toolstab

## Contributing

### Translations

1. Create an new translation file
   Example: If you want to add French translation:

   ```
   pylupdate6 src/app.py src/mainwindow.ui -ts src/translations/ja.ts
   ```

2. Translate
   Use QtLinguist to open the created .ts file and translate the strings with it.

3. Generate the translation file

   ```
   lrelease-qt6 src/translations/ja.ts -qm src/translations/ja.qm
   ```

   

