from pathlib import Path


# Fundamental constants
PROJECT_ROOT = Path(__file__).resolve().parent

CONFIG_PATH = PROJECT_ROOT / 'config.ini'
CONFIG_MISSING = not CONFIG_PATH.exists()
CONFIG_PRESET = """\
[Settings]
effectFrames = 5

[Textures]
effect  = "c:/path/to/texture.png"
hit0    = "c:/path/to/texture.png"
hit50   = "c:/path/to/texture.png"
hit100  = "c:/path/to/texture.png"
hit100k = "c:/path/to/texture.png"
hit300  = "c:/path/to/texture.png"
hit300k = "c:/path/to/texture.png"
hit300g = "c:/path/to/texture.png"

"""


def createConfig() -> None:
    # Delete existing config if it exists
    if not CONFIG_MISSING: 
        CONFIG_PATH.unlink()

    # Then create a new config with the preset content
    CONFIG_PATH.write_text(CONFIG_PRESET, encoding="utf-8")


if __name__ == "__main__":
    createConfig()
else:
    if CONFIG_MISSING:
        # Warn the user about the missing config file and attempt to create one with preset values
        print(f"Config file not found at: \"{CONFIG_PATH}\"!")
        print("Attempting to create a new one with preset values...")

        # Attempt to create the config file with preset values    
        createConfig()

        # Inform the user that they need to edit the config file before running the script again
        print("Preset config created successfully! Exiting...\n")
        print("NOTE: Please edit the config file to set your texture paths and settings before re-running the script.\n")
        
        # Exit with a non-zero status code to indicate that the script did not run successfully due to the missing config file
        quit(1)