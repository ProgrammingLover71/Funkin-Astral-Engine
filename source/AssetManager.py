# Friday Night Funkin' Astral Engine

### Asset Manager Module
# This module handles the loading and management of game assets such as images, sounds, and fonts.
# It uses different classes to organize assets based on their types.

import arcade as arc
from xml.etree import ElementTree as ET
from PIL import Image, ImageEnhance



###============ XML Atlas Utility ============###
def load_xml_atlas(xml_file: str, image_file: str):
    # Load the XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Load image sheet
    atlas_img = Image.open(image_file)
    
    textures = []

    for sub in root.findall("SubTexture"):
        name = sub.attrib["name"]
        x = int(sub.attrib["x"])
        y = int(sub.attrib["y"])
        w = int(sub.attrib["width"])
        h = int(sub.attrib["height"])

        # Crop the corresponding region
        frame = atlas_img.crop((x, y, x + w, y + h))

        # Convert to arcade texture
        tex = arc.Texture(
            name=name,
            image=frame
        )

        textures.append(tex)

    return textures



###============ Image Asset Class ============###

class ImageAsset:
    """
    Represents an image asset, which can be either a static image or a dynamic texture atlas.
    Attributes:
        `image_path` (str): The file path to the image.
        `atlas_path` (str | None): The file path to the accompanying XML atlas, if applicable.
        `texture` (arc.Texture | list[arc.Texture] | None): The loaded texture or list of textures.
    """
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.atlas_path = None
        self.texture: arc.Texture | list[arc.Texture] = None
    
    def __init__(self, texture: arc.Texture | list[arc.Texture], image_path: str = None, atlas_path: str = None):
        self.image_path = image_path
        self.atlas_path = atlas_path
        self.texture = texture

    @staticmethod
    def load(image_path: str):
        """
        Loads an image asset. If the image is static (no accompanying XML), it loads it as a single texture. \n
        If the image is dynamic (has accompanying XML), it loads it as a texture atlas.

        Args:
            `image_path` (str): The file path to the image.
        
        Returns:
            `ImageAsset`: The loaded image asset.
        """
        # If the image is static, load it as a texture:
        if ImageAsset.is_static_image(image_path):
            asset = ImageAsset(image_path)
            asset.texture = arc.load_texture(image_path)
            return asset
        # If the image is dynamic, load it as a texture atlas (load the spritesheet as a PIL image and slice it with the XML data):
        else:
            asset = ImageAsset(image_path)
            asset.atlas_path = image_path.rsplit('.', 1)[0] + '.xml'
            asset.texture = load_xml_atlas(asset.atlas_path, image_path)
            return asset
    
    @staticmethod
    def is_static_image(image_path: str) -> bool:
        """
        Determines if the given image is a static image (i.e., does not have an accompanying XML atlas).

        Args:
            `image_path` (str): The file path to the image.
        Returns:
            `bool`: True if the image is static, False if it has an accompanying XML atlas
        """
        # If an image 'image.png' is *not* static, then there will exist a file named 'image.xml' in the same directory.
        xml_path = image_path.rsplit('.', 1)[0] + '.xml'
        try:
            with open(xml_path, 'r'): return False
        except FileNotFoundError:
            return True
        
    @staticmethod
    def scale_texture(texture: arc.Texture, scale: float) -> arc.Texture:
        """
        Scales a given texture by a specified scaling factor.

        Args:
            `texture` (arc.Texture): The texture to scale.
            `scale` (float): The scaling factor.
        Returns:
            `arc.Texture`: The scaled texture.
        """
        # Use PIL to scale the texture's image
        pil_image = texture.image
        new_size = (int(pil_image.width * scale), int(pil_image.height * scale))
        scaled_image = pil_image.resize(new_size)

        # Create a new arcade texture with the scaled image
        scaled_texture = arc.Texture(image=scaled_image)
        return scaled_texture
    

    #======== Non-Static Members ========#
    

    def apply_brightness(self, factor: float):
        """
        Apply the brightness to the image asset's texture(s).
        Args:
            `factor` (float): The brightness factor to apply.
        """
        brightened_texture: list[arc.Texture] | arc.Texture = None
        # If it's a static image, adjust the brightness of the single texture
        if isinstance(self.texture, arc.Texture):
            pil_image = self.texture.image
            enhancer = ImageEnhance.Brightness(pil_image)
            brightened_image = enhancer.enhance(factor)

            brightened_texture = arc.Texture(image=brightened_image)
        
        # If it's a dynamic image (texture atlas), adjust the brightness of each texture in the list
        else:
            brightened_texture = []   # To prevent appending to None :}
            for tex in self.texture:
                pil_image = tex.image
                enhancer = ImageEnhance.Brightness(pil_image)
                brightened_image = enhancer.enhance(factor)
                brightened_texture.append(arc.Texture(image=brightened_image))
        
        return ImageAsset(brightened_texture, image_path=self.image_path, atlas_path=self.atlas_path)
    

    def apply_scale(self, scale: float):
        """
        Applies a scaling factor to the image asset's texture(s). \n
        *Warning*: Scales applied with this method are stackable, so be careful not to over-scale or under-scale.

        Args:
            `scale` (float): The scaling factor to apply.
        """
        # If it's a static image, scale the single texture
        if isinstance(self.texture, arc.Texture):
            self.texture = ImageAsset.scale_texture(self.texture, scale)
        # If it's a dynamic image (texture atlas), scale each texture in the list
        elif isinstance(self.texture, list):
            self.texture = [ImageAsset.scale_texture(tex, scale) for tex in self.texture]

        return self



###============ Sound Asset Class ============###

class SoundAsset:
    """
    Represents a sound asset.
    Attributes:
        `sound_path` (str): The file path to the sound.
        `sound` (arc.Sound | None): The loaded sound object.
    """
    def __init__(self, sound_path: str):
        self.sound_path = sound_path
        self.sound: arc.Sound = None

    @staticmethod
    def load(sound_path: str):
        """
        Loads a sound asset.

        Args:
            `sound_path` (str): The file path to the sound.
        Returns:
            `SoundAsset`: The loaded sound asset.
        """
        # Simply load the sound using Arcade's built-in loader
        asset = SoundAsset(sound_path)
        asset.sound = arc.load_sound(sound_path)
        return asset



###============ Font Asset Class ============###

class FontAsset:
    """
    Represents a font asset.
    Attributes:
        `font_path` (str): The file path to the font.
        `image` (ImageAsset | None): The loaded font image asset (as a TTF).
    """
    def __init__(self, font_path: str):
        self.font_path = font_path

    @staticmethod
    def load(font_path: str):
        """
        Loads a font asset.

        Args:
            `font_path` (str): The file path to the font.
        Returns:
            `FontAsset`: The loaded font asset.
        """
        asset = FontAsset(font_path)
        arc.load_font(font_path)     # Load the font into Arcade's font registry
        return asset



###=========== Text file Asset Class ===========###

class TextFileAsset:
    """
    Represents a text file asset.
    Attributes:
        `file_path` (str): The file path to the text file.
        `content` (str | None): The loaded text content.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content: str = None

    @staticmethod
    def load(file_path: str):
        """
        Loads a text file asset.

        Args:
            `file_path` (str): The file path to the text file.
        Returns:
            `TextFileAsset`: The loaded text file asset.
        """
        asset = TextFileAsset(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            asset.content = f.read()
        return asset



###============ Asset Manager Class ============###

class AssetManager:
    """
    Manages the loading and storage of various game assets including images, sounds, and fonts.
    Attributes:
        `images` (dict[str, ImageAsset]): A dictionary mapping image names to their corresponding ImageAsset objects.
        `sounds` (dict[str, SoundAsset]): A dictionary mapping sound names to their corresponding SoundAsset objects.
        `fonts` (dict[str, FontAsset]): A dictionary mapping font names to their corresponding FontAsset objects.
    
    The AssetManager class is responsible for loading assets on demand and caching them for future use to optimize performance.
    Not only that, but this class shall only be instantiated once, and used globally across the entire engine.
    """

    def __init__(self):
        # Make ourselves some little caches because we care about our sweet delicious RAM and performance :D
        self.images: dict[str, ImageAsset] = {}
        self.sounds: dict[str, SoundAsset] = {}
        self.fonts: dict[str, FontAsset] = {}
        self.text_files: dict[str, TextFileAsset] = {}


    def load_image(self, name: str, image_path: str):
        """
        Loads an image asset and stores it in the asset manager.

        Args:
            `name` (str): The name to associate with the image asset.
            `image_path` (str): The file path to the image.
        
        Returns:
            `ImageAsset`: The loaded image asset.
        """
        # Load the image using the ImageAsset class bcz that's why we added load functions (duhhh)
        # Oh, and only load it if it hasn't been loaded before
        if self.images.get(name) == None:
            self.images[name] = ImageAsset.load(image_path)
        return self.images[name]


    def load_sound(self, name: str, sound_path: str):
        """
        Loads a sound asset and stores it in the asset manager.

        Args:
            `name` (str): The name to associate with the sound asset.
            `sound_path` (str): The file path to the sound.
        """
        # Do the same for sounds...
        if self.sounds.get(name) == None:
            self.sounds[name] = SoundAsset.load(sound_path)
        return self.sounds[name]


    def load_font(self, name: str, font_path: str):
        """
        Loads a font asset and stores it in the asset manager.

        Args:
            `name` (str): The name to associate with the font asset.
            `font_path` (str): The file path to the font.
        """
        # ...And for fonts too ;)
        if self.fonts.get(name) == None:
            self.fonts[name] = FontAsset.load(font_path)
        return self.fonts[name]
    
    def load_text_file(self, name: str, file_path: str):
        """
        Loads a text file asset and stores it in the asset manager.

        Args:
            `name` (str): The name to associate with the text file asset.
            `file_path` (str): The file path to the text file.
        Returns:
            `TextFileAsset`: The loaded text file asset.
        """
        # And for text files as well
        if self.text_files.get(name) == None:
            self.text_files[name] = TextFileAsset.load(file_path)
        return self.text_files[name]