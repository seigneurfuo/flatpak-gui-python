# Flatpak GUI
![](docs/imgs/2023-06-05_14-37-26.png)

## Features
- English translation (in progress)
- French translation
- Search for installed / list available applications
- Search for installed / list available runtimes
- Install and remove applications
- Launch an installed application


## TODO
- List repos
- Show History
- Add more tools to the toolstab

## Contributing

### Translations

1. Create an new translation file
   Example: If you want to add French translation:

   ```
   pylupdate5 src/app.py src/mainwindow.ui -ts src/translations/ja.ts
   ```

2. Translate
   Use QtLinguist to open the created .ts file and translate the strings with it.

3. Generate the translation file

   ```
   lrelease-qt5 src/translations/ja.ts -qm src/translations/ja.qm
   ```

   

