import asyncio
import json
import os
import threading
from pathlib import Path

import dotenv
from duck_chat import ModelType
from nostr_sdk import Keys, Kind

from nostr_dvm.bot import Bot
from nostr_dvm.framework import DVMFramework
from nostr_dvm.tasks.generic_dvm import GenericDVM
from nostr_dvm.utils.admin_utils import AdminConfig
from nostr_dvm.utils.dvmconfig import DVMConfig, build_default_config
from nostr_dvm.utils.nip89_utils import NIP89Config, check_and_set_d_tag



def playground(announce = False):

    framework = DVMFramework()

    identifier = "bot_test"
    bot_config = build_default_config(identifier)
    bot_config.CHATBOT = False
    bot_config.DVM_KEY = "aa8ab5b774d47e7b29a985dd739cfdcccf93451678bf7977ba1b2e094ecd8b30"

    admin_config = AdminConfig()
    admin_config.REBROADCAST_NIP65_RELAY_LIST = False
    admin_config.UPDATE_PROFILE = False
    bot_config.RELAY_LIST = ["wss://relay.primal.net", "wss://relay.nostrdvm.com", "wss://nostr.oxtr.dev"]
    x = threading.Thread(target=Bot, args=([bot_config, admin_config]))
    x.start()


    kind = 5050
    admin_config = AdminConfig()
    admin_config.REBROADCAST_NIP89 = announce
    admin_config.REBROADCAST_NIP65_RELAY_LIST = announce
    admin_config.UPDATE_PROFILE = announce

    name = "DuckChat"
    identifier = "duckduckchat"  # Chose a unique identifier in order to get a lnaddress
    dvm_config = build_default_config(identifier)
    dvm_config.KIND = Kind(kind)  # Manually set the Kind Number (see data-vending-machines.org)
    dvm_config.SEND_FEEDBACK_EVENTS = False

    # Add NIP89
    nip89info = {
        "name": name,
        "picture": "https://image.nostr.build/28da676a19841dcfa7dcf7124be6816842d14b84f6046462d2a3f1268fe58d03.png",
        "about": "I'm briding DuckDuckAI'",
        "supportsEncryption": True,
        "acceptsNutZaps": dvm_config.ENABLE_NUTZAP,
        "nip90Params": {
        }
    }

    nip89config = NIP89Config()
    nip89config.KIND = Kind(kind)
    nip89config.DTAG = check_and_set_d_tag(identifier, name, dvm_config.PRIVATE_KEY, nip89info["picture"])
    nip89config.CONTENT = json.dumps(nip89info)

    options = {
        "input": "",
    }

    dvm = GenericDVM(name=name, dvm_config=dvm_config, nip89config=nip89config,
                     admin_config=admin_config, options=options)

    async def process(request_form):
        # pip install -U https://github.com/mrgick/duckduckgo-chat-ai/archive/master.zip

        from duck_chat import DuckChat
        options = dvm.set_options(request_form)
        async with DuckChat(model=ModelType.GPT4o) as chat:
            query = options["input"]
            result = await chat.ask_question(query)
            print(result)
        return result

    dvm.process = process  # overwrite the process function with the above one
    framework.add(dvm)
    #framework.run()



if __name__ == '__main__':
    env_path = Path('.env')
    if not env_path.is_file():
        with open('.env', 'w') as f:
            print("Writing new .env file")
            f.write('')
    if env_path.is_file():
        print(f'loading environment from {env_path.resolve()}')
        dotenv.load_dotenv(env_path, verbose=True, override=True)
    else:
        raise FileNotFoundError(f'.env file not found at {env_path} ')
    playground(False)