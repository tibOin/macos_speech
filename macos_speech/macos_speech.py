#!/usr/bin/env python
#~*~ coding: utf-8 ~*~

import re
from subprocess import call, check_output

DELAY_STR = "[[slnc {duration}]]" # Needs to be formated with miliseconds
DELAY_RE   = re.compile(r'(\[(\d+)\])') # compile once the parsing regexp

class SpeechError(Exception):
    def __init__(self, description):
        self.description = description
    def __str__(self):
        return self.description

class AudioDevice(object):
    def __init__(self, stdstring):
        stdstring = stdstring.strip()
        self.id = stdstring.split(' ')[0]
        self.name = stdstring.replace(self.id + ' ', '')

class Voice(object):
    def __init__(self, stdstring):
        elements = [el for el in stdstring.split(' ') if el]
        self.name = elements[0]
        self.lang = elements[1]
        self.desc = elements[2].replace('#', '')

class AudioFormatDescription(object):
    def __init__(self, stdstring):

        def _parse_iterable(iterable):
            iterable = iterable.replace('(', '').replace(')', '').replace('[', '').replace(']', '')
            if ',' in iterable:
                return iterable.split(',')
            else:
                return [iterable]

        elements = [el.strip() for el in stdstring.split(' ') if el]
        self.id = elements[0]
        self.name = ' '.join(elements[1:-2])
        self.exts = _parse_iterable(elements[-2])
        self.formats = _parse_iterable(elements[-1])

        self._get_bitrates()

    def _get_bitrates(self):
        self.bitrates = [bitrate.strip() for bitrate in check_output(['say', '--file-format', self.id, '--bit-rate', '?']).decode('utf-8').split('\n') if bitrate]


class AudioFormat(object):
    def __init__(self, id, dataformat=None, bitrate=None):
        self.id = id
        self.dataformat = dataformat
        self.bitrate    = str(bitrate)

class Synthesizer:
    def __init__(self, voice=None, infile=None, outfile=None, device=None,
                 rate=None, format=None, quality=None, text=None):

        # Extract data from system
        self._list_devices()
        self._list_formats()
        self._list_voices()

        # Set user defined properties
        self.infile  = infile
        self.outfile = outfile
        self.rate    = rate
        self.format  = format
        self.quality = quality
        self.text    = text

        if voice:
            for v in self.voices:
                if voice in v.name:
                    self.voice = v
        else:
            self.voice = voice

        if device:
            try:
                int(device)
                for dev in self.devices:
                    if dev.id == device:
                        self.device = dev
            except:
                for dev in self.devices:
                    if device in dev.name:
                        self.device = dev
        else:
            self.device = device

    def _list_devices(self):
        self.devices = []
        for line in [line for line in check_output(['say', '-a', '?']).decode('utf-8').split('\n') if line]:
            self.devices.append(AudioDevice(line))

    def _list_formats(self):
        self.formats = []
        for line in [line for line in check_output(['say', '--file-format', '?']).decode('utf-8').split('\n') if line]:
            line = line.strip()
            self.formats.append(AudioFormatDescription(line))

    def _list_voices(self):
        self.voices = []
        for line in [line for line in check_output(['say', '-v', '?']).decode('utf-8').split('\n') if line]:
            self.voices.append(Voice(line))

    def _prepared_cmd(self):
        cmd = 'say'

        if self.voice:
            cmd += ' -v ' + self.voice.name

        # Mutual exclusion with priority for output file
        if self.outfile:
            cmd += ' -o ' + self.outfile
        elif self.device:
            cmd += ' -a ' + self.device.id

        if self.rate:
            cmd += ' -r ' + str(self.rate)

        # Requirements
        if self.format:
            if not self.outfile:
                raise SpeechError('Synthesizer needs a file to output formated data. Please provide via Synthesizer.outfile')
            cmd += ' --file-format=' + self.format.id
            if self.format.dataformat:
                cmd += ' --data-format=' + self.format.dataformat
            if self.format.bitrate:
                cmd += ' --bit-rate=' + self.format.bitrate

        if self.quality:
            if int(self.quality) < 0 or int(self.quality) > 127:
                raise SpeechError('Synthesizer.quality must be between 0 and 127 (both included)')
            cmd += ' --quality=' + self.quality

        if self.infile:
            cmd += ' -f ' + self.infile
        elif self.text:
            cmd += ' "{your_message_here}"'.format(your_message_here=self.text)
        else:
            raise SpeechError("Synthesizer is missing text to say... Please provide either via `say('your text')`, Synthesiser.text or Synthesiser.infile properties.")

        return cmd.split(' ')

    def _parse_text(self, text):
        for match in DELAY_RE.finditer(text):
            text = text.replace(match.group(1), DELAY_STR.format(duration=match.group(2)))
        return text


    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, name):
        if name:
            if type(name) == Voice:
                self._voice = name
            else:
                for voice in self.voices:
                    if name in voice.name:
                        self._voice = voice
        else:
            self._voice = name

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, string):
        if string:
            if type(string) == AudioDevice:
                self._device = string
            else:
                try:
                    int(string)
                    for device in self.devices:
                        if device.id == string:
                            self._device = device
                except:
                    for device in self.devices:
                        if string in device.name:
                            self._device = device
        else:
            self._device = string

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, string):
        if string:
            self._text = self._parse_text(string)
        else:
            self._text = string

    def talk(self):
        call(self._prepared_cmd())

    def say(self, text):
        self.text = text
        self.talk()


if __name__ == '__main__':
    speaker = Synthesizer(voice='Alex', text="I'm the Python [50] macos_speech [40] module")
    speaker.talk()
