# panel_desktop_app
Turn a panel app into a desktop app


This project demonstrates how to run the [streaming tabulator example from Panel](https://panel.holoviz.org/gallery/streaming/streaming_tabulator.html) inside a desktop app.


## How to run

- create the environment 

```
conda env create -f environment.yml
```

- **NEW** : Use [Toga:master](https://github.com/beeware/toga) and [Panel>=0.13.0rc05](https://github.com/holoviz/panel/tree/v0.13.0rc5)


- run the script 

```
python poc.py streaming_tabulator.py
```