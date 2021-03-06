# macos_speech
Ever wanted to leverage the macOS builtin speech synthesis directly into python ? Or just make your code to talk...<br>
With the Python macos_speech package you can do it in a pythonic way. Easy and zen.

### Getting Started:

#### Installation
`pip install macos_speech`

or

```
git clone https://github.com/tibOin/macos_speech.git
cd macos_speech
pip install .
```

#### Requirements
macOS 10.x or for oldest OS X <br>
For now, this package only works on Python >= 2.6 and Python >= 3.6.x <br>
Only tested on Python 2.7.10 and >= 3.7.2.

#### Basic usage
```python
from macos_speech import Synthesizer

speaker = Synthesizer(voice='Alex', device='Built-in')

speaker.text = """Oh my God! I can make my python code to talk!

And I can even send multiple lines! Awesome.
"""

speaker.talk()

# or

speaker.say("Hello!")
```

#### Get informations

```python
from macos_speech import Synthesizer

speaker = Synthesizer()

print('''Voices:
NAME    LANGUAGE    DESCRIPTION
''')
for voice in speaker.voices:
  print('{} {} {}'.format(voice.name, voice.lang, voice.desc))

print('')

print('Audio devices:')
for device in speaker.devices:
  print('ID: {}, NAME: {}'.format(device.id, device.name))

print('')

print('''Output file possible formats:
ID    NAME    FILE_EXT    DATA_FORMATS    BIT_RATES
''')
for format in speaker.formats:
  print('{} {} ({}) [{}] [{}]'.format(format.id, format.name,
                                      ','.join(format.exts),
                                      ','.join(format.formats),
                                      ','.join(format.bitrates)))

```

#### Synthesizer Properties
```python
from macos_speech import Synthesizer

synthe = Synthesizer()

# Helper properties
synthe.devices
synthe.voices
synthe.formats

# Configuration properties

# File IO (takes absolute pathes strings)
synthe.infile  # A file containing text to say (mutually exclusive with self.text - high priority)
synthe.outfile # The output audio file (default should be 'output.aiff'
               # but you can specify file and data formats)

# Simple configs (takes strings)
synthe.rate    # The speech rate
synthe.quality # The audio quality (between 0 and 127 both included)
synthe.text    # The text to say (mutually exclusive with self.infile - low priority)

# Pythonified configs (takes macos_speech.CustomClasses)
synthe.format  # The audio output file/data format : macos_speech.AudioFormat
               # (Works only with self.outfile populated)

synthe.device  # The audio output device           : macos_speech.AudioDevice
               #                                 (or 'name' or 'id' on Python 3)
               # (Only used if no self.outfile)

synthe.voice   # The voice to use                  : macos_speech.Voice
               #                                   (or 'name' on Python 3)
```

#### Go Further

```python
from macos_speech import Synthesizer, AudioFormat

# Speech manipulation:
# To create more realistic speech you can play on time and rate.

# You can add delays between words by following a simple syntax.
# Just set the delay by writing time in milliseconds between brackets.
mytext = 'I want to say... [100] something.'

# And/Or specify a rate in words per minutes to your Synthesiser
speaker = Synthesizer(voice='Alex', rate=50, text=mytext)

speaker.talk()

# Record to file:

# Basically, setting an outfile with supported extension would be enough to correctly encode the file.
# (There are some limitations: setting just 'out.mp4' doesn't work for example)
speaker = Synthesizer(voice='Alex', text='Some text to record', outfile='out.aac')

speaker.talk()

# But you can customize a lot more your output file:
format  = AudioFormat('mp4f', dataformat='alac')
speaker.format = format
speaker.outfile = 'out.mp4'
speaker.talk()

```
