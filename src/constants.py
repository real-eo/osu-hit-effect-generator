from pathlib import Path
from configparser import ConfigParser


# Config
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / 'config.ini'
config = ConfigParser()
config.read(CONFIG_PATH)

def _cleanPath(value: str) -> str:
    # Allow quoted values in config.ini while keeping plain values untouched.
    return value.strip().strip('"').strip("'")


# Settings
EFFECT_DURATION = config.getint('Settings', 'effectFrames')                             # ? Duration in frames
HIT_FADE_IN_DURATION = 8                                                                # ? Duration in frames (frames 0-7)
HIT_OPAQUE_DURATION = 22                                                                # ? Duration in frames (frames 8-30)
HIT_FADE_OUT_DURATION = 36                                                              # ? Duration in frames (frames 31-66)

HIT_FIRST_FRAME = 0
HIT_LAST_FRAME = sum([
    HIT_FADE_IN_DURATION, 
    HIT_OPAQUE_DURATION, 
    HIT_FADE_OUT_DURATION
]) - 1


# Textures
class Texture:
    NONE = -1                                                                           # ? Default value for textures that are not set
    
    EFFECT = _cleanPath(config.get('Textures', 'effect'))
    HIT0 = _cleanPath(config.get('Textures', 'hit0'))
    HIT50 = _cleanPath(config.get('Textures', 'hit50'))
    HIT100 = _cleanPath(config.get('Textures', 'hit100'))
    HIT100K = _cleanPath(config.get('Textures', 'hit100k'))
    HIT300 = _cleanPath(config.get('Textures', 'hit300'))
    HIT300K = _cleanPath(config.get('Textures', 'hit300k'))
    HIT300G = _cleanPath(config.get('Textures', 'hit300g'))


# Exporting
class Export:
    # Save location
    class Location:                                                                         # ? Where to save the generates frames to
        _ROOT = PROJECT_ROOT / "out"
        
        # Subfolders for each hit type
        HIT0 = _ROOT / "hit0"
        HIT50 = _ROOT / "hit50"
        HIT100 = _ROOT / "hit100"
        HIT100K = _ROOT / "hit100k"
        HIT300 = _ROOT / "hit300"
        HIT300K = _ROOT / "hit300k"
        HIT300G = _ROOT / "hit300g"
    
    # Texture templates
    class Template:                                                                         # ? Template for the generated frames
        HIT0 = "hit0-{frame}.png"
        HIT50 = "hit50-{frame}.png"
        HIT100 = "hit100-{frame}.png"
        HIT100K = "hit100k-{frame}.png"
        HIT300 = "hit300-{frame}.png"
        HIT300K = "hit300k-{frame}.png"
        HIT300G = "hit300g-{frame}.png"
