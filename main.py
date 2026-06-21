from pathlib import Path
from PIL import Image
from src.constants import (
	EFFECT_DURATION,
	HIT_FADE_IN_DURATION,
    HIT_OPAQUE_DURATION,
    HIT_FADE_OUT_DURATION,
	HIT_FIRST_FRAME,
    HIT_LAST_FRAME,
	Export,
	Texture,
)

def lerp(valueStart: float, valueEnd: float, t: float) -> float:
	return valueStart + (valueEnd - valueStart) * t


def alphaScaleFromFrame(frame: int) -> float:
	if frame < HIT_FIRST_FRAME or frame > HIT_LAST_FRAME:
		return 0.0

	if frame < HIT_FADE_IN_DURATION:
		# Frames 0-7: 0% -> 100%
		return frame / (HIT_FADE_IN_DURATION - 1)

	if frame < HIT_FADE_IN_DURATION + HIT_OPAQUE_DURATION:
		# Frames 8-30: 100%
		return 1.0

	# Frames 31-66: 100% -> 0%
	t = (frame - (HIT_FADE_IN_DURATION + HIT_OPAQUE_DURATION)) / (HIT_FADE_OUT_DURATION - 1)
	return lerp(1.0, 0.0, t)


def effectAlphaScaleFromFrame(frame: int) -> float:
	# Effect is fully visible for frame range 0 -> EFFECT_DURATION-1
	return 1.0 if 0 <= frame < EFFECT_DURATION else 0.0


def scaleAlpha(image: Image.Image, factor: float) -> Image.Image:
	factor = max(0.0, min(1.0, factor))

	result = image.copy()
	r, g, b, a = result.split()
	scaledAlpha = a.point(lambda px: int(round(px * factor)))
	result.putalpha(scaledAlpha)
	return result


def composeCentered(baseSize: tuple[int, int], layers: list[Image.Image]) -> Image.Image:
	canvas = Image.new("RGBA", baseSize, (0, 0, 0, 0))
	for layer in layers:
		offset = (
			(baseSize[0] - layer.width) // 2,
			(baseSize[1] - layer.height) // 2,
		)
		canvas.alpha_composite(layer, offset)
	return canvas


def ensureOutputDirs() -> None:
	outputDirs = [
		Export.Location.HIT0,
		Export.Location.HIT50,
		Export.Location.HIT100,
		Export.Location.HIT100K,
		Export.Location.HIT300,
		Export.Location.HIT300K,
		Export.Location.HIT300G,
	]
	for outputDir in outputDirs:
		outputDir.mkdir(parents=True, exist_ok=True)


def frameConfigs() -> list[tuple[str, str, Path, str]]:
	return [
		("hit0", Texture.HIT0, Export.Location.HIT0, Export.Template.HIT0),
		("hit50", Texture.HIT50, Export.Location.HIT50, Export.Template.HIT50),
		("hit100", Texture.HIT100, Export.Location.HIT100, Export.Template.HIT100),
		("hit100k", Texture.HIT100K, Export.Location.HIT100K, Export.Template.HIT100K),
		("hit300", Texture.HIT300, Export.Location.HIT300, Export.Template.HIT300),
		("hit300k", Texture.HIT300K, Export.Location.HIT300K, Export.Template.HIT300K),
		("hit300g", Texture.HIT300G, Export.Location.HIT300G, Export.Template.HIT300G),
	]


def loadRgba(pathStr: str) -> Image.Image:
	image_path = Path(pathStr)
	if not image_path.exists():
		raise FileNotFoundError(f"Texture not found: {image_path}")
	with Image.open(image_path) as image:
		return image.convert("RGBA")


def generateFrames() -> None:
	ensureOutputDirs()

	effectImage = loadRgba(Texture.EFFECT)

	for hitName, hit_texture_path, outputDir, template in frameConfigs():
		hitImage = loadRgba(hit_texture_path)
		baseSize = (
			max(effectImage.width, hitImage.width),
			max(effectImage.height, hitImage.height),
		)

		for frame in range(HIT_FIRST_FRAME, HIT_LAST_FRAME + 1):
			effect_layer = scaleAlpha(effectImage, effectAlphaScaleFromFrame(frame))
			hit_layer = scaleAlpha(hitImage, alphaScaleFromFrame(frame))
			composite = composeCentered(baseSize, [effect_layer, hit_layer])

			fileName = template.format(frame=frame)
			composite.save(outputDir / fileName)

		print(f"Generated frames for {hitName} in {outputDir}")


if __name__ == "__main__":
	import setup
	
	generateFrames()
