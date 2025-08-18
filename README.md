
### Documentação em Português

```markdown
# Warframe Mods Bot

Um bot para Discord escrito em Python que busca e exibe os mods mais caros de vários sindicatos de Warframe usando a API do Warframe Market. O bot envia atualizações diárias e responde a comandos com preços de mods e links.

## Funcionalidades
- **Atualizações Diárias**: Envia os 5 mods mais caros de cada sindicato às 6:00 e 12:10 (horário de Brasília).
- **Comandos**: Usuários podem consultar preços de mods usando comandos com prefixo (ex.: `!cephalon_suda`).
- **Top Mods**: Exibe os 5 mods mais caros entre todos os sindicatos com `!top`.
- **Tratamento de Erros**: Fornece feedback se comandos falharem ou não houver dados disponíveis.

## Pré-requisitos
- Python 3.8+
- Token de bot do Discord (obtido no [Discord Developer Portal](https://discord.com/developers/applications))
- Pacotes Python necessários: `discord.py`, `aiohttp`, `apscheduler`, `pytz`, `python-dotenv`

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/lu0ck/WarframeModsBotDiscord.git
   cd WarframeModsBotDiscord
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
   (Crie um `requirements.txt` com `pip freeze > requirements.txt` após instalar as dependências.)
3. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto com:
     ```
     BOT_TOKEN=seu_token_do_discord_aqui
     ```
   - Adicione `.env` ao `.gitignore` para mantê-lo seguro.
4. Execute o bot:
   ```bash
   python main.py
   ```

## Uso
### Comandos
- `!ping`: Verifica se o bot está responsivo (retorna "Pong!").
- `!ajuda` ou `!socorro`: Lista os comandos disponíveis.
- `!top`: Mostra os 5 mods mais caros entre todos os sindicatos.
- `!<sindicato>`: Exibe os 3 mods mais caros de um sindicato específico (ex.: `!cephalon_suda`, `!steel_meridian`).
  - Nomes de sindicatos podem usar `_` ou `-` (ex.: `!cephalon_suda` ou `!cephalon-suda`).

### Exemplo
```
!cephalon_suda
```
Resposta: Um embed com os 3 mods mais caros, seus preços e links para o Warframe Market.

## Configuração
- `YOUR_CHANNEL_ID`: Defina como o ID do canal do Discord onde as mensagens diárias e respostas de comandos serão enviadas.
- `YOUR_GUILD_ID`: Opcional, para sincronização de comandos específica do servidor (atualmente não utilizado).
- `COMMAND_PREFIX`: Altere o prefixo (padrão é `!`) no código, se desejar.

## Contribuindo
Sinta-se à vontade para fazer um fork deste repositório, sugerir melhorias e enviar pull requests. Problemas e sugestões são bem-vindos!

## Licença
PRIVADO

## Aviso
Ainda nao contem todos os mods e sindicatos, caso alguem queira fazer sinta-se livre, farei com o passar do tempo e quando liberar tudo no jogo.

## Agradecimentos
- API do Warframe Market por fornecer os dados de preços dos mods.
- Comunidade Discord.py por suporte.
```

### Documentação em Inglês

```markdown
# Warframe Mods Bot

A Discord bot written in Python that fetches and displays the top-priced mods from various Warframe syndicates using the Warframe Market API. The bot sends daily updates and responds to commands with mod prices and links.

## Features
- **Daily Updates**: Sends the top 5 most expensive mods for each syndicate at 6:00 AM and 12:10 PM (Brasília time).
- **Commands**: Users can query mod prices using prefix commands (e.g., `!cephalon_suda`).
- **Top Mods**: Displays the top 5 mods across all syndicates with `!top`.
- **Error Handling**: Provides feedback if commands fail or no data is available.

## Prerequisites
- Python 3.8+
- Discord bot token (obtained from [Discord Developer Portal](https://discord.com/developers/applications))
- Required Python packages: `discord.py`, `aiohttp`, `apscheduler`, `pytz`, `python-dotenv`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/lu0ck/WarframeModsBotDiscord.git
   cd WarframeModsBotDiscord
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (Create a `requirements.txt` file with `pip freeze > requirements.txt` after installing dependencies.)
3. Set up environment variables:
   - Create a `.env` file in the project root with:
     ```
     BOT_TOKEN=your_discord_bot_token_here
     ```
   - Add `.env` to `.gitignore` to keep it secure.
4. Run the bot:
   ```bash
   python main.py
   ```

## Usage
### Commands
- `!ping`: Checks if the bot is responsive (returns "Pong!").
- `!ajuda` or `!socorro`: Lists available commands.
- `!top`: Shows the top 5 most expensive mods across all syndicates.
- `!<syndicate>`: Displays the top 3 mods for a specific syndicate (e.g., `!cephalon_suda`, `!steel_meridian`).
  - Syndicate names can use `_` or `-` (e.g., `!cephalon_suda` or `!cephalon-suda`).

### Example
```
!cephalon_suda
```
Response: An embed with the top 3 mods, their prices, and Warframe Market links.

## Configuration
- `YOUR_CHANNEL_ID`: Set to the Discord channel ID where daily messages and command responses will be sent.
- `YOUR_GUILD_ID`: Optional, for guild-specific command syncing (currently unused).
- `COMMAND_PREFIX`: Change the prefix (default is `!`) in the code if desired.

## Contributing
Feel free to fork this repository, make improvements, and submit pull requests. Issues and suggestions are welcome!

## License
PRIVATE

## Notice
It still doesn't contain all the mods and unions, if anyone wants to do it feel free, I will do it over time and when I release everything in the game.

## Acknowledgments
- Warframe Market API for providing mod price data.
- Discord.py community for support.
```
