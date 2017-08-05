from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

from tg_bot import sql, dispatcher

lock_types = ["sticker", "audio", "voice", "document", "video", "contact", "photo"]


def locktypes(bot, update):
    update.effective_message.reply_text(lock_types)


def can_delete(bot, update):
    return update.effective_chat.get_member(bot.id).can_delete_messages


def lock(bot, update, args):
    chat_id = update.effective_chat.id
    lock_type = args[0]
    if len(args) >= 1 and lock_type in lock_types:
        sql.update_lock(chat_id, lock_type, locked=True)
    else:
        update.effective_message.reply_text("What are you trying to lock...?")

    if not can_delete(bot, update):
        update.effective_message.reply_text("I'm not an administrator, so can't do anything.")


def unlock(bot, update, args):
    chat_id = update.effective_chat.id
    lock_type = args[0]
    if len(args) >= 1 and lock_type in lock_types:
        sql.update_lock(chat_id, lock_type, locked=False)
    else:
        bot.sendMessage(chat_id, "What are you trying to unlock...?", "HTML")

    if not can_delete(bot, update):
        update.effective_message.reply_text("I'm not an administrator, so can't do anything.")


@run_async
def del_message(bot, update):
    if can_delete(bot, update) and update.effective_message.reply_to_message:
        update.effective_message.reply_to_message.delete()
        update.effective_message.delete()


@run_async
def del_sticker(bot, update):
    chat_id = update.effective_chat.id
    if sql.is_locked(chat_id, "sticker") and can_delete(bot, update):
        update.effective_message.delete()


@run_async
def del_audio(bot, update):
    chat_id = update.effective_chat.id
    if sql.is_locked(chat_id, "audio") and can_delete(bot, update):
        update.effective_message.delete()


@run_async
def del_voice(bot, update):
    chat_id = update.effective_chat.id
    if sql.is_locked(chat_id, "voice") and can_delete(bot, update):
        update.effective_message.delete()


@run_async
def del_document(bot, update):
    chat_id = update.effective_chat.id
    if sql.is_locked(chat_id, "document") and can_delete(bot, update):
        update.effective_message.delete()


@run_async
def del_video(bot, update):
    chat_id = update.effective_chat.id
    if sql.is_locked(chat_id, "video") and can_delete(bot, update):
        update.effective_message.delete()


@run_async
def del_contact(bot, update):
    chat_id = update.effective_chat.id
    if sql.is_locked(chat_id, "contact") and can_delete(bot, update):
        update.effective_message.delete()


@run_async
def del_photo(bot, update):
    chat_id = update.effective_chat.id
    if sql.is_locked(chat_id, "photo") and can_delete(bot, update):
        update.effective_message.delete()


locktypes_handler = CommandHandler("locktypes", locktypes)
lock_handler = CommandHandler("lock", lock, pass_args=True)
unlock_handler = CommandHandler("unlock", unlock, pass_args=True)
delete_handler = CommandHandler("delete", del_message)
sticker_handler = MessageHandler((~ Filters.private) & Filters.sticker, del_sticker)
audio_handler = MessageHandler((~ Filters.private) & Filters.audio, del_audio)
voice_handler = MessageHandler((~ Filters.private) & Filters.voice, del_voice)
document_handler = MessageHandler((~ Filters.private) & Filters.document, del_document)
video_handler = MessageHandler((~ Filters.private) & Filters.video, del_video)
contact_handler = MessageHandler((~ Filters.private) & Filters.contact, del_contact)
photo_handler = MessageHandler((~ Filters.private) & Filters.photo, del_photo)  # TODO: gif detection -> mime_type?


dispatcher.add_handler(lock_handler)
dispatcher.add_handler(unlock_handler)
dispatcher.add_handler(delete_handler)
dispatcher.add_handler(locktypes_handler)
dispatcher.add_handler(sticker_handler)
dispatcher.add_handler(audio_handler)
dispatcher.add_handler(voice_handler)
dispatcher.add_handler(document_handler)
dispatcher.add_handler(video_handler)
dispatcher.add_handler(contact_handler)
dispatcher.add_handler(photo_handler)