# PortalGuessr 2

This is a major rewrite of the original [PortalGuessr bot](https://github.com/XnonXte/PortalGuessr-Bot-2) - Featuring a lot more commands, more robust storage system, etc.

## Installation

- Download the latest release if available.
- Run `install.bat` to install the required dependencies with Pipenv.
- Create a `config.env` file containing `TOKEN` and `IMGBB_API_KEY` variables (get your own imgbb's API key at: https://imgbb.com/).
- Fill in your own `OWNER_USER_ID` and `TESTING_SERVER_ID` in `./src/const.py` (must be a valid Discord IDs).
- Run the environment with `pipenv run python ./src/main.py`.
- Enjoy! Let me know of what you think of it!

## Possible FAQs

- Q: How does the bot calculate ELO in `/lb`?
  - A: It does so with this formula: 3 × easy + 5 × medium + 10 × hard + 15 × veryhard
- Q: What criteria do I need to follow in order for my submission to get accepted?
  - A: There aren't really a criteria just a constraint that needs to be followed in order to get accepted, the constraint is available on pinned messages at `#submissions` channel in the PortalGuessr's testing server.
- Q: Can I contribute to PortalGuessr?
  - A: Yes! Any contribution is welcome, although I would appreciate you if you join the testing server on Discord first.

## Discord Server

Join the testing server on Discord to get the latest news about PortalGuessr: https://discord.gg/3fZaCKMNPw
