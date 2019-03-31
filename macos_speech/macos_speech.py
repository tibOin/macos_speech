#!/usr/bin/env python
#~*~ coding: utf-8 ~*~
from subprocess import call, check_output

DELAYCHAR = "[[slnc {duration}]]" # Needs to be formated with miliseconds

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
        self.bitrates = [bitrate.strip() for bitrate in check_output(['say', '--file-format', self.id, '--bit-rate', '?']).split('\n') if bitrate]


class AudioFormat(object):
    def __init__(self, fileformat, dataformat=None, bitrate=None):
        self.fileformat = fileformat
        self.dataformat = dataformat
        self.bitrate    = str(bitrate)

class Synthesizer:
    def __init__(self, voice=None, infile=None, outfile=None, device=None,
                 rate=None, format=None, quality=None, text=None):

        self._list_devices()
        self._list_formats()
        self._list_voices()

        # Init all to None
        self.voice      = voice
        self.infile     = infile
        self.outfile    = outfile
        self.device     = device
        self.rate       = rate
        self.format     = format
        self.quality    = quality
        self.text       = text

        # Interpret arguments
        if voice:
            for v in self.voices:
                if voice in v.name:
                    self.voice = v
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

    def _list_devices(self):
        self.devices = []
        for line in [line for line in check_output(['say', '-a', '?']).split('\n') if line]:
            self.devices.append(AudioDevice(line))

    def _list_formats(self):
        self.formats = []
        for line in [line for line in check_output(['say', '--file-format', '?']).split('\n') if line]:
            line = line.strip()
            self.formats.append(AudioFormatDescription(line))

    def _list_voices(self):
        self.voices = []
        for line in [line for line in check_output(['say', '-v', '?']).split('\n') if line]:
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
            cmd += ' -r ' + self.rate

        # Requirements
        if self.format:
            if not self.outfile:
                raise SpeechError('Synthesizer needs a file to output formated data. Please provide via Synthesizer.infile')
            cmd += ' --file-format=' + self.format.fileformat
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
            raise SpeechError("Synthesizer is missing text to say... Please provide either via `say(text='your text')`, Synthesiser.text or Synthesiser.infile properties.")

        return cmd.split(' ')

    def talk(self):
        call(self._prepared_cmd())
