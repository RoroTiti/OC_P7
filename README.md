# GrandPyBot by @RoroTiti

![Screenshot](https://i.imgur.com/FQnLJ6z.png)

## User manual

### Getting started

To run the application, it's recommended to setup a virtual environment. We will use virtualenv.

- Move to the source root directory
```
cd "/the/app/directory"
```

- Initialize a virtualenv
```
pip install virtualenv # install virtualenv if not already installed
virtualenv venv
```

- Enable the virtual environment 

  - MacOS/Linux
    ```
    source venv/bin/
    ```
    
  - Windows
    ```
    .\venv\Scripts\activate
    ```

- Install GrandPyBot dependencies
```
pip install -r requirements.txt
```

### Run GrandPyBot

- You can now start GrandPyBot with the following commands. Run them from the root of the source code directory

  - macOS/Linux
    ```
    export FLASK_APP=grandpybot.main
    python -m flask run
    ```
    
  - Windows (with PowerShell)
    ```
    $env:FLASK_APP = "grandpybot.main"
    python -m flask run
    ```

- Once the Flask server is started, you can now browse the URL given in the terminal to start talking to GrandPyBot.

## Working environment
- Windows 10 or macOS Mojave and upper
- Python 3.8