<a id="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Evenius Bot</h3>
  <p align="center">A multilingual Telegram bot for live stock prices, charts and price alerts</p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Evenius is a Telegram bot that looks up live stock prices via Yahoo Finance. Send it a ticker and it replies with the current price plus a chart of the last 30 days. You can also set a price alert, and the bot will message you once the asset reaches your target.

Built as a personal learning project to explore the Telegram Bot API, async Python and working with market data.

Features:
* Live price lookup for any ticker available on Yahoo Finance
* 30-day closing-price chart generated with Matplotlib and sent as an image
* Price alerts, checked every minute and automatically expiring after 31 days
* Interface in English, German and Russian
* Works in private chats and in groups (mention the bot by its handle)

### Built With

* Python 3
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (with JobQueue)
* [yfinance](https://github.com/ranaroussi/yfinance)
* Matplotlib

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites
* Python 3
* A Telegram bot token from [@BotFather](https://t.me/BotFather)

### Installation

1. Create a bot with [@BotFather](https://t.me/BotFather) on Telegram and copy the API token it gives you.
2. Clone the repo
   ```sh
   git clone https://github.com/DV155/eveniusBot.git
   cd eveniusBot
   ```
3. Create a virtual environment and install the dependencies
   ```sh
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install matplotlib "python-telegram-bot[job-queue]"
   ```
4. Create a `.env` file in the project root (it is already git-ignored)
   ```env
   API_TOKEN=your_telegram_bot_token
   BOT_HANDLE=@your_bot_username
   ```
5. Start the bot
   ```sh
   python main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE -->
## Usage

| Command | What it does |
| --- | --- |
| `/start` | Greets you and lets you choose English, German or Russian |
| `/stock` | Asks for a ticker (e.g. `AAPL`) and replies with the live price and a 30-day chart |
| `/alert` | Asks for a ticker and target price in the form `TSLA 200`; you get a message when the price is reached |
| `/help` | Short explanation of how to use the bot |

Tip: use ticker symbols rather than company names for reliable results.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/DV155/eveniusBot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=DV155/eveniusBot" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT license. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Daniil Vasilcovschii - [LinkedIn](https://www.linkedin.com/in/daniil-vasilcovschii-903543358) - [GitHub](https://github.com/DV155)

Project Link: [https://github.com/DV155/eveniusBot](https://github.com/DV155/eveniusBot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>