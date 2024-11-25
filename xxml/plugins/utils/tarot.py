import PIL.Image
from nonebot import on_command
from nonebot.adapters import Message

from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent

matcher = on_command(
    "tarot",
    priority=10, 
    block=True
)

from pathlib import Path
import random
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
from io import BytesIO

imgDir = Path("./xxml/resources/tarot/").resolve()

def get_random_image():
    path = imgDir
    images = list(path.glob("*"))
    random_image = random.choice(images)
    return random_image.resolve()

def compress(image):
    if image.mode == "RGBA":
        # Separate the RGB and alpha channels
        rgb_image = image.convert("RGB")
        alpha_channel = image.getchannel("A")

        # Compress the RGB part in memory as if it were a JPEG
        with BytesIO() as buffer:
            rgb_image.save(buffer, format="JPEG", quality=10)  # Adjust quality as needed
            buffer.seek(0)

            # Load the compressed RGB image
            compressed_rgb_image = PIL.Image.open(buffer)

            # Reattach the alpha channel to the compressed RGB image
            compressed_image_with_alpha = PIL.Image.merge("RGBA", (
                compressed_rgb_image.getchannel("R"),
                compressed_rgb_image.getchannel("G"),
                compressed_rgb_image.getchannel("B"),
                alpha_channel,
            ))

            return compressed_image_with_alpha  # Returns an RGBA Image object in PNG format

    else:
        # If the image doesn't have an alpha channel, compress it as RGB
        with BytesIO() as buffer:
            image.convert("RGB").save(buffer, format="JPEG", quality=10)  # Adjust quality as needed
            buffer.seek(0)

            # Load the compressed JPEG image and save as PNG to maintain format
            compressed_image = PIL.Image.open(buffer).convert("RGB")
            return compressed_image  # Returns an RGB Image object in PNG format]
        
def rescale(image: PIL.Image.Image, max_size = 1000):
    """
    Rescale an image to ensure the longest edge is under `max_size` pixels, maintaining aspect ratio.
    
    Parameters:
        image (Image.Image): The original PIL Image object.
        max_size (int): Maximum size of the longest edge (default is 2000px).
    
    Returns:
        Image.Image: The resized PIL Image object.
    """
    width, height = image.size
    # Determine the scaling factor needed to resize the longest edge to max_size
    scaling_factor = min(max_size / width, max_size / height)
    
    # If scaling is needed, resize the image
    if scaling_factor < 1:
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        image = image.resize(new_size, PIL.Image.Resampling.LANCZOS)
    
    # Return the resized image as a new Image object
    return image


def add_rounded_corners(image, radius=100):
    # Convert the image to RGBA if it's not already
    image = image.convert("RGBA")
    
    # Create a mask for the rounded corners with the same size as the image
    mask = PIL.Image.new("L", image.size, 0)
    draw = PIL.ImageDraw.Draw(mask)
    
    # Draw a white rounded rectangle on the mask
    draw.rounded_rectangle(
        (0, 0, image.size[0], image.size[1]), radius=radius, fill=255
    )
    
    # Apply the mask to the image
    rounded_image = PIL.Image.new("RGBA", image.size)
    rounded_image.paste(image, (0, 0), mask=mask)
    
    return rounded_image

def add_shadow(image: PIL.Image.Image, shadow_offset=(0, 5), shadow_color=(0, 0, 0, 20), blur_radius=10, corner_radius=100):
    # Calculate the size of the new image with shadow
    width, height = image.size
    padding = int(blur_radius * 2.5)

    total_width = width + padding * 2 + abs(shadow_offset[0])
    total_height = height + padding * 2 + abs(shadow_offset[1])

    # Create a new image with transparent background for shadow effect
    shadow = PIL.Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))

    # Create a rounded rectangle shape for the shadow
    shadow_draw = PIL.ImageDraw.Draw(shadow)
    shadow_box = (
        padding + shadow_offset[0], 
        padding + shadow_offset[1], 
        padding + shadow_offset[0] + width, 
        padding + shadow_offset[1] + height
    )

    # Draw a rounded rectangle for the shadow
    rounded_rect = PIL.Image.new("L", (width, height), 0)
    draw = PIL.ImageDraw.Draw(rounded_rect)
    draw.rounded_rectangle((0, 0, width, height), radius=corner_radius, fill=255)

    # Create the shadow by pasting the rounded rectangle with the shadow color
    shadow_layer = PIL.Image.new("RGBA", (width, height), shadow_color)
    shadow_layer.putalpha(rounded_rect)
    shadow.paste(shadow_layer, (padding + shadow_offset[0], padding + shadow_offset[1]), rounded_rect)

    # Blur the shadow to give it a soft card-like effect
    shadow = shadow.filter(PIL.ImageFilter.GaussianBlur(blur_radius))

    # Paste the original image onto the shadow image
    shadow.paste(image, (padding, padding), image)

    return shadow

from xxml.external.chatgpt import tarot_read

@matcher.handle()
async def handle(event: MessageEvent):
    selected = get_random_image()
    selected_id = int(selected.stem)

    tarot_card_dict = {
        0: "愚者",
        1: "魔术师",
        2: "女祭司",
        3: "皇后",
        4: "皇帝",
        5: "教皇",
        6: "恋人",
        7: "战车",
        8: "力量",
        9: "隐士",
        10: "命运之轮",
        11: "正义",
        12: "倒吊人",
        13: "死亡",
        14: "节制",
        15: "恶魔",
        16: "塔",
        17: "星星",
        18: "月亮",
        19: "太阳",
        20: "审判",
        21: "世界"
    }

    data = BytesIO()

    if (random.randint(0, 1) == 0):
        im = PIL.Image.open(selected)
        im = add_rounded_corners(im)
        im = add_shadow(im)
        im = rescale(im)
        im.rotate(random.randint(-100, 100)/10, expand=True, resample=PIL.Image.Resampling.BICUBIC).save(data, format="PNG")
        data.seek(0)

        reading = await tarot_read(event.sender.nickname, event.get_user_id, tarot_card_dict[selected_id], event.get_plaintext())
        if reading is None:
            reading = ""

        await matcher.send(message = Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.image(data),
            MessageSegment.text(f"\n{event.sender.nickname}抽到了... {tarot_card_dict[selected_id]}"),
            MessageSegment.text("\n\n"+reading)
        ]))
    else:
        im = PIL.Image.open(selected).rotate(180)
        im = add_rounded_corners(im)
        im = add_shadow(im)
        im = rescale(im)
        im.rotate(random.randint(-100, 100)/10, expand=True, resample=PIL.Image.Resampling.BICUBIC).save(data, format="PNG")
        data.seek(0)

        reading = await tarot_read(event.sender.nickname, event.get_user_id, tarot_card_dict[selected_id]+"（逆位）", event.get_plaintext())
        if reading is None:
            reading = ""

        await matcher.send(message = Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.image(data),
            MessageSegment.text(f"\n{event.sender.nickname}抽到了... {tarot_card_dict[selected_id]}-逆位"),
            MessageSegment.text("\n\n"+reading),
        ]))
    