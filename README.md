# panel_desktop_app
Turn a panel app into a desktop app


This project demonstrates how to run the [streaming tabulator example from Panel](https://panel.holoviz.org/gallery/streaming/streaming_tabulator.html) inside a desktop app.


## How to run

- create the environment 

```
conda env create -f environment.yml
```

- **Important** : 
  - As stated in the `environment.yml` file, [Panel>=0.13.0](https://github.com/holoviz/panel/tree/v0.13.0) is required.
  - To benefit from the last improvements on Windows, use [Toga:master](https://github.com/beeware/toga). Refer to [Toga's documentation](https://toga.readthedocs.io/en/latest/how-to/contribute.html) to install it.
  

- run the script 

```
# python poc.py [panel app to run]
python poc.py streaming_tabulator.py
```
