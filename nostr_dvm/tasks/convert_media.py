import json
import os
from nostr_dvm.interfaces.dvmtaskinterface import DVMTaskInterface
from nostr_dvm.utils.admin_utils import AdminConfig
from nostr_dvm.utils.definitions import EventDefinitions
from nostr_dvm.utils.dvmconfig import DVMConfig, build_default_config
from nostr_dvm.utils.nip89_utils import NIP89Config, check_and_set_d_tag
from nostr_dvm.utils.mediasource_utils import organize_input_media_data
from nostr_dvm.utils.output_utils import upload_media_to_hoster


"""
This File contains a Module convert media locally

Accepted Inputs: Text, Events, Jobs (Text Extraction, Summary, Translation)
Outputs: Text containing the TranslationGoogle in the desired language.
Params:  -language The target language
"""


class MediaConverter(DVMTaskInterface):
    KIND = EventDefinitions.KIND_NIP90_CONVERT_VIDEO
    TASK = "convert"
    FIX_COST = 20
    PER_UNIT_COST = 0.1

    def __init__(self, name, dvm_config: DVMConfig, nip89config: NIP89Config,
                 admin_config: AdminConfig = None, options=None):
        dvm_config.SCRIPT = os.path.abspath(__file__)
        super().__init__(name, dvm_config, nip89config, admin_config, options)

    def is_input_supported(self, tags):
        for tag in tags:
            if tag.as_vec()[0] == 'i':
                input_value = tag.as_vec()[1]
                input_type = tag.as_vec()[2]
                if input_type != "url":
                    return False
        return True

    def create_request_from_nostr_event(self, event, client=None, dvm_config=None):
        request_form = {"jobID": event.id().to_hex()}
        url = ""
        media_format = "video/mp4"
        input_type = "text"
        start_time = 0
        end_time = 0
        # TODO parse start/end parameters

        for tag in event.tags():
            if tag.as_vec()[0] == 'i':
                input_type = tag.as_vec()[2]
                if input_type == "url":
                    url = tag.as_vec()[1]


            elif tag.as_vec()[0] == 'param':
                param = tag.as_vec()[1]
                if param == "format":  # check for param type
                    media_format = tag.as_vec()[2]

        filepath = organize_input_media_data(url, input_type, start_time, end_time, dvm_config, client, True,
                                             media_format)
        options = {
            "filepath": filepath
        }

        request_form['options'] = json.dumps(options)
        return request_form

    def process(self, request_form):
        options = DVMTaskInterface.set_options(request_form)
        url = upload_media_to_hoster(options["filepath"])

        return url


# We build an example here that we can call by either calling this file directly from the main directory,
# or by adding it to our playground. You can call the example and adjust it to your needs or redefine it in the
# playground or elsewhere
def build_example(name, identifier, admin_config):
    dvm_config = build_default_config(identifier)
    admin_config.LUD16 = dvm_config.LN_ADDRESS
    # Add NIP89
    nip89info = {
        "name": name,
        "image": "https://image.nostr.build/c33ca6fc4cc038ca4adb46fdfdfda34951656f87ee364ef59095bae1495ce669.jpg",
        "about": "I convert videos from urls to given output format.",
        "encryptionSupported": True,
        "cashuAccepted": True,
        "nip90Params": {
            "format": {
                "required": False,
                "values": ["video/mp4", "audio/mp3"]
            }
        }
    }

    nip89config = NIP89Config()


    return MediaConverter(name=name, dvm_config=dvm_config, nip89config=nip89config,
                          admin_config=admin_config)

def process_venv():
    args = DVMTaskInterface.process_args()
    dvm_config = build_default_config(args.identifier)
    dvm = MediaConverter(name="", dvm_config=dvm_config, nip89config=NIP89Config(), admin_config=None)
    result = dvm.process(json.loads(args.request))
    DVMTaskInterface.write_output(result, args.output)


if __name__ == '__main__':
    process_venv()