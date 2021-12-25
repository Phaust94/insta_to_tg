import time
import os

from helpers import StoryArchive
from secrets import ACCOUNT_USERNAME, ACCOUNT_PASSWORD, TARGETS

STORAGE = os.path.join(__file__, "..", "stories")


def main() -> None:
    while True:
        arch = StoryArchive.from_folder(
            ACCOUNT_USERNAME, ACCOUNT_PASSWORD,
            TARGETS, STORAGE,
        )

        messages = arch.update_from_remote()
        for msg in messages:
            msg.send()
        time.sleep(12 * 60 * 60)

    return None


if __name__ == '__main__':
    main()
