from renderer.shader import Shader
from renderer.texture import Texture

class AssetPool:

    _shaders = {}
    _textures = {}
    _spritesheets = {}

    @classmethod
    def get_shader(cls, resource_path: str, shader_name: str):
        if (resource_path + "/" + shader_name) in AssetPool._shaders.keys():
            return AssetPool._shaders[resource_path + "/" + shader_name]
        else:
            shader = Shader(resource_path, shader_name)
            shader.compile()
            AssetPool._shaders[resource_path + "/" + shader_name] = shader
            return shader

    @classmethod
    def get_texture(cls, resource_path: str):
        if resource_path in AssetPool._textures.keys():
            return AssetPool._textures[resource_path]
        else:
            texture = Texture(resource_path)
            AssetPool._textures[resource_path] = texture
            return texture

    @classmethod
    def add_sprite_sheet(cls, resource_path, spritesheet):
        if resource_path not in AssetPool._spritesheets.keys():
            AssetPool._spritesheets[resource_path] = spritesheet

    @classmethod
    def get_spritesheet(cls, resource_path):
        if resource_path not in AssetPool._spritesheets.keys():
            raise LookupError(f"Tried to access spritesheet '{resource_path}' and it has not been added to asset pool.")
        return AssetPool._spritesheets[resource_path]
