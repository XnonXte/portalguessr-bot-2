# PortalGuessr 2

This is a major rewrite of the original [PortalGuessr bot](https://github.com/XnonXte/PortalGuessr-Bot) - Featuring a lot more commands, more robust storage system, etc.

## Installation

- Download the latest release if available.
- Create and fill in yourself the required environment variables listed [here](#required-environment-variables) in `.env`.
- Install the required dependencies with `pip install -r requirements.txt`.
- Run the bot with running `run.bat`.

## Installation Using Docker

- Install latest docker.
- Create and fill in yourself the required environment variables listed [here](#required-environment-variables) in `.env`.
- Run `docker build -t XnonXte/portalguessr-bot-2 .` to build the container image. Keep in mind that your configuration will be baked into the container image!
- To start the container use `docker run -d XnonXte/portalguessr-bot-2`.

### Required Environment Variables

- `SUBMISSION_CHANNEL_ID`: Dedicated channel for submitting new guesses.
- `OWNER_USER_ID`: This bot owner's Discord ID for maintenance purposes.
- `TESTING_SERVER_ID`: Dedicated server for testing this bot.
- `P1SR_GUILD_ID`: P1SR server ID if it wants to be run in P1SR as well.
- `P1SR_SPAM_CHANNEL_ID`: The bot spam channel ID in P1SR.
- `SERVER_URL`: The backend server URL; see [here](https://github.com/PortalGuessr/portalguessr-backend) for more information.
- `IMGBB_SERVER_URL`: The IMGBB API endpoint should be easily available on the internet.
- `DISCORD_INVITE`: The invite to the testing server.
- `INVITE_URL`: The invite for this bot.
- `API_KEY`: Backend server API key; see [here](https://github.com/PortalGuessr/portalguessr-backend/blob/main/README.md#installation) for more information on creating one.
- `IMGBB_API_KEY`: IMGBB API key that you have acquired through the site itself.
- `TOKEN`: The bot's token.

## FAQs

- Q: How does the bot calculate ELO in `/lb`?
  - A: It does so with this formula: (3 × easy) + (5 × medium) + (10 × hard) + (15 × veryhard)
- Q: What criteria do I need to follow in order for my submission to get accepted?
  - A: There aren't really a criteria just a constraint that needs to be followed in order to get accepted, the constraint is available on pinned messages at `#submissions` channel in the PortalGuessr's testing server.
- Q: Can I contribute to PortalGuessr?
  - A: Yes! Any contribution is welcome, although I would appreciate you if you join the testing server on Discord first.
- Q: What is `API_KEY`?
  - A: It's an auth key that needs to match with same key you use in your own [PortalGuessr's backend server.](https://github.com/PortalGuessr/PortalGuessr-Backend)

## Discord Server

Join the testing server on Discord to get the latest news about PortalGuessr: <https://discord.gg/dDbgtFb2KC>

## Invite

Invite this bot to your server: <https://discord.com/oauth2/authorize?client_id=1117773586522968105&permissions=2147601472&scope=bot%20applications.commands>
