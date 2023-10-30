# SoundCloud Ripper

SoundCloud Ripper is a python script that uses an IDOR on https://on.soundcloud.com to find privates tracks & playlists just by bruteforcing shareable links.

The soundcloud shortcut link system works like this: https://on.soundcloud.com/xxxxx

The "x" corresponds to the identifier, which is made up of 5 random characters, allowing us to access private content without any verification.

This script generates shortcut links, tests whether or not they correspond to private tracks and saves them in a hits.xml file.


You can find a better version of this script [here](https://github.com/3eyka/sound-cloudripper) ^^


## Installation

Clone the repository :

```
git clone https://github.com/fancymalware/soundcloud-ripper.git
```

## Usage

Use pip ton install dependencies :

```
pip install requirements.txt
```

Then start ripper.py and enjoy >.<


## License

[MIT](https://choosealicense.com/licenses/mit/)