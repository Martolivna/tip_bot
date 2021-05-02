import io

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from make_img import make_image

TOKEN = ""
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='tip')
async def tip_handler(message: types.Message):
    if not message.reply_to_message:
        return
    l_name, l_photo = await get_name_n_photo(message.from_user)
    r_name, r_photo = await get_name_n_photo(message.reply_to_message.from_user)
    await message.answer_sticker(make_image(l_name, l_photo, r_name, r_photo))


async def get_name_n_photo(user: types.User):
    name = user.first_name
    photos = await user.get_profile_photos(limit=1)
    if not photos.photos:
        return name, None
    photo = await photos.photos[0][0].download(io.BytesIO())
    return name, photo


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
