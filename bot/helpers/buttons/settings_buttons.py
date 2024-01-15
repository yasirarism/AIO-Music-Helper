from bot.helpers.translations import lang
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

exit_button = [
    [
        InlineKeyboardButton(text=lang.select.MAIN_MENU_BUTTON, callback_data="main_menu"),
        InlineKeyboardButton(text=lang.select.CLOSE_BUTTON, callback_data="close")
    ]
]


def main_menu_set():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.select.TG_AUTH_BUTTON,
                callback_data="tgPanel"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.TIDAL_BUTTON,
                callback_data="tidalPanel"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.KKBOX_BUTTON,
                callback_data="kkboxPanel"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.QOBUZ_BUTTON,
                callback_data="qobuzPanel"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.DEEZER_BUTTON,
                callback_data="deezerPanel"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.SOUNDCLOUD_BUTTON,
                callback_data="scPanel"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.CLOSE_BUTTON,
                callback_data="close"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def tidal_menu_set():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.select.AUTH_BUTTON,
                callback_data="ADA_tidal_panel"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.QUALITY_BUTTON,
                callback_data="QA_tidal"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.API_BUTTON,
                callback_data="apiTidal_panel"
            )
        ]
    ]
    inline_keyboard += exit_button
    return InlineKeyboardMarkup(inline_keyboard)

def tidal_api_set(api, platform):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=f"{i} - {platform[i]}", callback_data=f"apiTidal_{i}"
            )
        ]
        for i in api
    ]
    inline_keyboard += exit_button
    return InlineKeyboardMarkup(inline_keyboard)


def common_auth_set(provider):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.select.ADD_AUTH_BUTTON,
                callback_data=f"ADA_{provider}_add"
            ),
            InlineKeyboardButton(
                text=lang.select.REMOVE_AUTH_BUTTON,
                callback_data=f"RMA_{provider}_warn"
            )
        ]
    ]
    inline_keyboard += exit_button
    return InlineKeyboardMarkup(inline_keyboard)

def confirm_RMA_button():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.select.YES_BUTTON,
                callback_data="RMA_tidal_yes"
            ),
            InlineKeyboardButton(
                text=lang.select.NO_BUTTON,
                callback_data="RMA_tidal_no"
            )
        ]
    ]
    inline_keyboard += exit_button
    return InlineKeyboardMarkup(inline_keyboard)

def quality_buttons(provider, data=None):
    if provider == "tidal":
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text=lang.select.MASTER_QUALITY,
                    callback_data="SQA_tidal_Master"
                )
            ],
            [
                InlineKeyboardButton(
                    text=lang.select.HIFI_QUALITY,
                    callback_data="SQA_tidal_HiFi"
                )
            ],
            [
                InlineKeyboardButton(
                    text=lang.select.HIGH_QUALITY,
                    callback_data="SQA_tidal_High"
                )
            ],
            [
                InlineKeyboardButton(
                    text=lang.select.NORMAL_QUALITY,
                    callback_data="SQA_tidal_Normal"
                )
            ]
        ]
    elif provider == 'kkbox':
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text=quality.upper(), callback_data=f"SQA_kkbox_{quality}"
                )
            ]
            for quality in data
        ]
    inline_keyboard = inline_keyboard + exit_button
    return InlineKeyboardMarkup(inline_keyboard)

def kkbox_menu_set():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.select.QUALITY_BUTTON,
                callback_data="QA_kkbox"
            )
        ]
    ]
    inline_keyboard += exit_button
    return InlineKeyboardMarkup(inline_keyboard)
