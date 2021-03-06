import logging
from SaitamaRobot.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler
from telegram.ext.filters import BaseFilter
from SaitamaRobot import dispatcher as d
from typing import Optional, Union, List

log = logging.getLogger('[Enterprise]')

class VoiletTelegramHandler:
    def __init__(self, d):
        self._dispatcher = d

    def command(
            self, command: str, filters: Optional[BaseFilter] = None, admin_ok: bool = False, pass_args: bool = False,
            pass_chat_data: bool = False, run_async: bool = True, can_disable: bool = True,
            group: Optional[int] = 40
    ):

        def _command(func):
            try:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleCommandHandler(command, func, filters=filters,
                                                  pass_args=pass_args, admin_ok=admin_ok), group
                    )
                else:
                    self._dispatcher.add_handler(
                        CommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args), group
                    )
                log.debug(f"[KIGCMD] Loaded handler {command} for function {func.__name__} in group {group}")
            except TypeError:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleCommandHandler(command, func, filters=filters,
                                                  pass_args=pass_args, admin_ok=admin_ok, pass_chat_data=pass_chat_data)
                    )
                else:
                    self._dispatcher.add_handler(
                        CommandHandler(command, func, filters=filters, pass_args=pass_args,
                                       pass_chat_data=pass_chat_data)
                    )
                log.debug(f"[KIGCMD] Loaded handler {command} for function {func.__name__}")

            return func

        return _command

    def message(self, pattern: Optional[BaseFilter] = None, can_disable: bool = True, run_async: bool = True,
                group: Optional[int] = 60, friendly=None):
        def _message(func):
            try:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleMessageHandler(pattern, func, friendly=friendly), group
                    )
                else:
                    self._dispatcher.add_handler(
                        MessageHandler(pattern, func), group
                    )
                log.debug(f"[KIGMSG] Loaded filter pattern {pattern} for function {func.__name__} in group {group}")
            except TypeError:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleMessageHandler(pattern, func, friendly=friendly)
                    )
                else:
                    self._dispatcher.add_handler(
                        MessageHandler(pattern, func)
                    )
                log.debug(f"[KIGMSG] Loaded filter pattern {pattern} for function {func.__name__}")

            return func

        return _message

    def callbackquery(self, pattern: str = None, run_async: bool = True):
        def _callbackquery(func):
            self._dispatcher.add_handler(CallbackQueryHandler(pattern=pattern, callback=func, run_async=run_async))
            log.debug(f'[KIGCALLBACK] Loaded callbackquery handler with pattern {pattern} for function {func.__name__}')
            return func

        return _callbackquery

    def inlinequery(self, pattern: Optional[str] = None, run_async: bool = True, pass_user_data: bool = True,
                    pass_chat_data: bool = True, chat_types: List[str] = None):
        def _inlinequery(func):
            self._dispatcher.add_handler(
                InlineQueryHandler(pattern=pattern, callback=func, run_async=run_async, pass_user_data=pass_user_data,
                                   pass_chat_data=pass_chat_data, chat_types=chat_types))
            log.debug(
                f'[KIGINLINE] Loaded inlinequery handler with pattern {pattern} for function {func.__name__} | PASSES '
                f'USER DATA: {pass_user_data} | PASSES CHAT DATA: {pass_chat_data} | CHAT TYPES: {chat_types}')
            return func

        return _inlinequery


vilcmd = VoiletTelegramHandler(d).command
vilmsg = VoiletTelegramHandler(d).message
vilcallback = VoiletTelegramHandler(d).callbackquery
vilinline = VoiletTelegramHandler(d).inlinequery
