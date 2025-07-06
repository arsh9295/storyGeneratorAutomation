import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import globalVariables as gv


FOOOCUS_HOST = os.getenv("FOOOCUS_HOST", "story1-fooocus")
FOOOCUS_PORT = int(os.getenv("FOOOCUS_PORT", "8888"))
KOKORO_HOST = os.getenv("KOKORO_HOST", "story1-kokoro")
KOKORO_PORT = int(os.getenv("KOKORO_PORT", "8880"))



def GenerateImage(prompt, outputPath, outputFile, apiUrl=None, 
                   negativePrompts=None, seed=None, sampler=None, 
                   performance_selection=None, aspect_ratios_selection=None, guidance_scale=None, imageModel=None, subModel=None, fooocusPath=None, imageExtension=None):

	# Initialize parameters with defaults or from global variables
	apiUrl = apiUrl if apiUrl is not None else getattr(gv, 'apiUrl', f"http://{FOOOCUS_HOST}:{FOOOCUS_PORT}/v1/generation/text-to-image")
	negativePrompts = negativePrompts if negativePrompts is not None else getattr(
		gv, 'negativePrompts',
		"bad hands, deformed, blurry, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands and fingers, poorly drawn hands and fingers, missing fingers, extra digit, fewer digits, cropped, worst quality, nsfw, lowres, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, fused fingers, too many fingers, long neck, cgi, 3d, cartoon, anime, sketch, drawing, painting, illustration, low quality, out of focus, bad lighting, overexposed, underexposed, grainy, pixelated, noisy, artifacts, compression artifacts, watermarks, text, logo, signature, copyright, label, brand, product name"
	)
	seed = seed if seed is not None else getattr(gv, 'seed', -1)
	sampler = sampler if sampler is not None else getattr(gv, 'sampler', "DPM++ 2M Karras")
	performance_selection = performance_selection if performance_selection is not None else getattr(gv, 'performance_selection', "Speed")
	aspect_ratios_selection = aspect_ratios_selection if aspect_ratios_selection is not None else getattr(gv, 'aspect_ratios_selection', "1080*1920")
	guidance_scale = guidance_scale if guidance_scale is not None else getattr(gv, 'guidance_scale', 7.5)
	imageModel = imageModel if imageModel is not None else getattr(gv, 'imageModel', "fooocus")
	subModel = subModel if subModel is not None else getattr(gv, 'subModel', "juggernautXL_version6Rundiffusion.safetensors")
	fooocusPath = fooocusPath if fooocusPath is not None else getattr(gv, 'fooocusPath', "C:/AI/Fooocus-API/")
	imageExtension = imageExtension if imageExtension is not None else getattr(gv, 'imageExtension', "png")
        
	if not os.path.exists(outputPath):
		os.makedirs(outputPath, exist_ok=True)

	if imageModel.lower() == "fooocus":
		from lib.imageLib.imageGeneratorFooocus import GenerateImageFooocus
		ImageGeneratorResult = GenerateImageFooocus(
			prompt, outputPath, outputFile, fooocusPath, negativePrompts, seed, sampler, performance_selection, aspect_ratios_selection, guidance_scale, imageModel, imageExtension
		)
	else:
		raise ValueError(f"Unsupported image model: {imageModel}")