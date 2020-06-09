<h1 align="center">Unsilence</h1>

*<p align="center">Console Interface and Library to remove silent parts of a media file</p>*

<p align="center">
  <a href="https://github.com/lagmoellertim/unsilence/blob/master/LICENSE" target="_blank"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat"/></a>
</p>

---

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/912008edef1b4960818c29a16ef2c29f)](https://app.codacy.com/manual/lagmoellertim/unsilence?utm_source=github.com&utm_medium=referral&utm_content=lagmoellertim/unsilence&utm_campaign=Badge_Grade_Dashboard)

<p align="center">
  <a href="https://asciinema.org/a/jnU7VsPNqaNER3dSrvLp2RAQF" target="_blank"><img src="https://asciinema.org/a/jnU7VsPNqaNER3dSrvLp2RAQF.svg"/></a>
</p>

## Introduction

Unsilence is an **open-source tool** that **removes silence** from a media clip of your choice (audio, video).

You can use it to **speed up** videos without changing the audible speed, so you can understand everything, but get through a video **faster**.

### Exemplary use cases

- You are a college student and watch your lectures online (but have access to the video files). Instead of just increasing the playback speed to ~1.5x, you can remove
    the parts that do not contain any value, like your lecturer thinking or waiting for something. But instead of cutting out these silent parts, speeding them up by a 
    different, much faster factor (think 6-8x) makes you still able to follow what is happening, so drawing or writing with no speech is sped up, which makes it far more pleasant to watch
    
- You want a video editor that automatically cuts any time you talk (or make any sound). That could be useful for manual time lapses
    (you make a sound every time a short segment should be recorded), or for very fast jump cut videos with no manual editing required
    
- You want to have some fun and remove all the audible parts from a video, leaving only the parts where nearly silent noises are in the video (breathing, writing, ...)

### Usage Information

Unsilence can be used as a console line interface or as a python library, with which you can develop your own projects

### Prerequisites

- [Python](https://www.python.org/) >= 3.8.0
- [pip](https://pypi.org/) (should be installed automatically with python, could be different on some linux distros)
- [ffmpeg](https://ffmpeg.org/)  >= 4.2.0

### Installation as command line interface (using pip and pipx)

```sh
# Installing pipx
pip install pipx

# Installing Unsilence as Command Line Software
pipx install unsilence

# If pipx asks you to, you also need to execute the following line
# as well as close and reopen your terminal window
pipx ensurepath
```

### Installation as library (using pip)

```sh
# Installing Unsilence as Command Line Software
pip install unsilence
```

### Installation as command line interface (from source)

```sh
# Clone the repository (stable branch)
git clone -b master https://github.com/lagmoellertim/unsilence.git unsilence

#Change Directory
cd unsilence

# Install pip packages
pip install -r requirements.txt
pip install pipx

# Install unsilence package
pipx install .
```

### Installation as library (from source)

```sh
# Clone the repository (stable branch)
git clone -b master https://github.com/lagmoellertim/unsilence.git unsilence

#Change Directory
cd unsilence

# Install pip packages
pip install -r requirements.txt

# Install unsilence package
python3 setup.py install
```

## Basic Command Line Usage

This generates a new file, where the silent parts are 6x as fast as before, the audible parts are the same speed as before
```sh
unsilence [input_file] [output_file]
``` 
You can change the speed of audible parts with `-as [speed]`, the speed of silent parts with `-ss [speed]`
```sh
unsilence [input_file] [output_file] -as [speed] -ss [speed]
``` 
You can change the volume of audible parts with `-av [volume]`, the volume of silent parts with `-sv [volume]`
```sh
unsilence [input_file] [output_file] -av [volume] -sv [volume]
``` 
To generate an audio only output file, you can add the `-ao` flag
```sh
unsilence [input_file] [output_file] -ao
``` 
To speed up the rendering process, you can increase the thread count using `-t [threads]`
```sh
unsilence [input_file] [output_file] -t [threads]
``` 
For many more settings, type `-h` or `--help`
```sh
unsilence --help
``` 

## Basic Library Usage
Take a look at this [example](https://github.com/lagmoellertim/unsilence/blob/master/examples/basic_usage.py)

## Contributing

If you are missing a feature or have new idea, go for it! That is what open-source is for!

## Author

**Tim-Luca Lagmöller** ([@lagmoellertim](https://github.com/lagmoellertim))

## Donate

You can also contribute by [buying me a coffee](https://www.buymeacoffee.com/lagmoellertim).

## License

[MIT License](https://github.com/lagmoellertim/unsilence/blob/master/LICENSE)

Copyright © 2019-present, [Tim-Luca Lagmöller](https://lagmoellertim.de)

## Have fun :tada:
