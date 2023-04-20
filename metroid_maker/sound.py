import ctypes
import openal.al as al
import soundfile as sf


class Sound:
    def __init__(self, file_path, loop):
        self._file_path = file_path
        self._is_playing = False

        raw_audio, sample_rate = sf.read(file_path, dtype="int16")
        raw_audio = raw_audio.flatten().tobytes()
        channels = sf.info(file_path).channels

        sound_format = -1

        if channels == 1:
            sound_format = al.AL_FORMAT_MONO16
        elif channels == 2:
            sound_format = al.AL_FORMAT_STEREO16

        self._buffer_id = ctypes.c_uint()
        al.alGenBuffers(1, ctypes.pointer(self._buffer_id))
        al.alBufferData(
            self._buffer_id,
            sound_format,
            raw_audio,
            ctypes.c_int(len(raw_audio)),
            ctypes.c_int(sample_rate),
        )

        self._source_id = ctypes.c_uint()
        al.alGenSources(1, ctypes.pointer(self._source_id))

        al.alSourcei(self._source_id, al.AL_BUFFER, ctypes.c_int(self._buffer_id.value))
        al.alSourcei(self._source_id, al.AL_LOOPING, ctypes.c_int(loop))
        al.alSourcefv(
            self._source_id, al.AL_POSITION, (ctypes.c_float * 3)(0.0, 0.0, 0.0)
        )
        al.alSourcef(self._source_id, al.AL_GAIN, ctypes.c_float(0.3))

    def delete(self):
        al.alDeleteSources(1, ctypes.pointer(self._source_id))
        al.alDeleteBuffers(1, ctypes.pointer(self._buffer_id))

    def play(self):
        state = ctypes.c_int()
        al.alGetSourcei(self._source_id, al.AL_SOURCE_STATE, state)
        if state.value == al.AL_STOPPED:
            self._is_playing = False
            al.alSourcefv(
                self._source_id,
                ctypes.c_int(al.AL_POSITION),
                (ctypes.c_float * 3)(0.0, 0.0, 0.0),
            )

        if not self._is_playing:
            al.alSourcePlay(self._source_id)
            self._is_playing = True

    def stop(self):
        if self._is_playing:
            al.alSourceStop(self._source_id)
            self._is_playing = False

    @property
    def file_path(self):
        return self._file_path

    @property
    def is_playing(self):
        state = ctypes.c_int()
        al.alGetSourcei(self._source_id, al.AL_SOURCE_STATE, state)
        if state.value == al.AL_STOPPED:
            self._is_playing = False

        return self._is_playing
