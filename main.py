import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import aiohttp
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from datetime import datetime
from collections import defaultdict
import uuid
from datetime import timezone

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

# ========== CONFIG ==========
BOT_TOKEN =  os.getenv("BOT_TOKEN")  # Obtém o token da variável de ambiente
COMMAND_PREFIX = "!"
YOUR_CHANNEL_ID = 1404116804158361653  # ID do canal (int)
YOUR_GUILD_ID = os.getenv("YOUR_GUILD_ID")    
API_BASE_URL = "https://api.warframe.market/v1"

# ===== INTENTS / BOT =====
intents = discord.Intents.default()
intents.message_content = True  # necessário para ler mensagens no chat
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# ===== MAPA DOS SINDICATOS (INCOMPLETO) =====
SYNDICATE_MODS = {
    "vilcor_nekralisck": [
        "bhisaj_bal", "damzav_vati", "hata_satya", "zazvat_kar"
    ],
    "kermerros_nekralisck": [
        "contagious_bond", "duplex_bond", "tenacious_bond", "martyr_symbiosis",
        "seismic_bond", "vicious_bond", "volatile_parasite"
    ],
    "master_teasonai_cetus": [
        "covert_bond", "manifold_bond", "mystic_bond", "restorative_bond", "dandem_bond"
    ],
    "cephalon_simaris": [
        "ambush", "astral_autopsy", "batnist", "detect_vulnerability", "energy_conversion",
        "energy_generator", "health_conversion", "looter", "madurai_transmute_core",
        "naramon_transmute_core", "negate", "reawaken", "sacrificial_pressure",
        "sacrificial_steel", "umbral_fiber", "umbral_intensify", "umbral_vitality",
        "vazarin_transmute_core"
    ],
    "arbitration_honors": [
        "adaptation", "aerial_ace", "aerodynamic", "cautious_shot", "combat_discipline",
        "energizing_shot", "galvanized_acceleration", "galvanized_aptitude",
        "galvanized_chamber", "galvanized_crosshairs", "galvanized_diffusion",
        "galvanized_elementalist", "galvanized_hell", "galvanized_reclex",
        "galvanized_savvy", "galvanized_scope", "galvanized_shot", "galvanized_steel",
        "melee_guidance", "mending_shot", "power_donation", "preparation",
        "rolling_guard", "sharpshooter", "shepherd", "swift_momentum", "vigorous_swap"
    ],
    "steel_meridian": [
        "scattered_justice", "justice_blades", "neutralizing_justice", "shattering_justice",
        "path_of_statues", "tectonic_fracture", "ore_gaze", "titanic_rumbler",
        "rubble_heap", "prismatic_companion", "recrystalize", "fireball_frenzy",
        "immolated_radiance", "healing_flame", "exothermic", "surging_dash",
        "radiant_finish", "furious_javelin", "chromatic_blade", "freeze_force",
        "ice_wave_impedance", "chilling_globe", "icy_avalanche", "biting_frost",
        "dread_ward", "blood_forge", "blending_talons", "gourmand", "hearty_nourishment",
        "catapult", "gastro", "accumulating_whipclaw", "venari_bodyguard",
        "pilfering_strangledome", "volatile_recompense", "wrath_of_ukko",
        "ballistic_bullseye", "staggering_shield", "muzzle_flash", "mesa's_waltz",
        "pyroclastic_flow", "reaping_chakram", "safeguard", "divine_retribution",
        "controlled_slide", "teeming_virulence", "larva_burst", "parasitic_vitality",
        "insatiable", "abundant_mutation", "neutron_star", "antimatter_absorb",
        "escape_velocity", "molecular_fission", "smite_infusion", "hallowed_eruption",
        "phoenix_renewal", "hallowed_reckoning", "wrecking_wall", "fused_crucible",
        "ironclad_charge", "iron_shrapnel", "piercing_roar", "reinforcing_stomp",
        "venom_dose", "revealing_spores", "regenerative_molt", "contagion_cloud",
        "prey_of_dynar", "ulfrun's_endurance", "vampiric_grasp", "the_relentless_lost"
    ],
    "arbiters_of_hexis": [
        "gilded_truth", "blade_of_truth", "avenging_truth", "stinging_truth",
        "seeking_shuriken", "smoke_shadow", "teleport_rush", "rising_storm",
        "elusive_retribution", "endless_lullaby", "reactive_storm", "duality",
        "calm_and_frenzy", "peaceful_provocation", "energy_transfer", "surging_dash",
        "radiant_finish", "furious_javelin", "chromatic_blade", "warrior's_rest",
        "shattered_storm", "mending_splinters", "spectrosiphon", "mach_crash",
        "thermal_transfer", "conductive_sphere", "coil_recharge", "cathode_current",
        "tribunal", "warding_thurible", "lasting_covenant", "desiccation's_curse",
        "elemental_sandstorm", "negation_armor", "jade's_judgment", "omikuji's_fortune",
        "rift_haven", "rift_torrent", "cataclysmic_continuum", "savior_decoy",
        "damage_decoy", "hushed_invisibility", "safeguard_switch", "irradiating_disarm",
        "hall_of_malevolence", "explosive_legerdemain", "total_eclipse", "mind_freak",
        "pacifying_bolts", "chaos_sphere", "assimilate", "repair_dispensary",
        "temporal_artillery", "temporal_erosion", "axios_javelineers", "intrepid_stand",
        "shock_trooper", "shocking_speed", "transistor_shield", "capacitance",
        "celestial_stomp", "enveloping_cloud", "primal_rage"
    ],
    "cephalon_suda": [
        "entropy_spike", "entropy_flight", "entropy_detonation", "entropy_burst",
        "sonic_fracture", "resonance", "savage_silence", "resonating_quake",
        "razor_mortar", "afterburn", "everlasting_ward", "vexing_retaliation",
        "guardian_armor", "guided_effigy", "freeze_force", "ice_wave_impedance",
        "chilling_globe", "icy_avalanche", "biting_frost", "balefire_surge",
        "blazing_pillage", "aegis_gale", "viral_tempest", "tidal_impunity",
        "rousing_plunder", "pilfering_swarm", "empowered_quiver", "piercing_navigator",
        "infiltrate", "concentrated_arrow", "rift_haven", "rift_torrent",
        "cataclysmic_continuum", "hall_of_malevolence", "explosive_legerdemain",
        "total_eclipse", "pyroclastic_flow", "reaping_chakram", "safeguard",
        "divine_retribution", "controlled_slide", "neutron_star", "antimatter_absorb",
        "escape_velocity", "molecular_fission", "partitioned_mallet", "conductor",
        "wrecking_wall", "fused_crucible", "thrall_pact", "mesmer_shield",
        "blinding_reave", "shadow_haze", "dark_propagation", "tesla_bank",
        "repelling_bastille", "photon_repeater", "fused_reservoir", "critical_surge",
        "cataclysmic_gate", "vampiric_grasp", "the_relentless_lost",
        "merulina_guardian", "loyal_merulina", "surging_blades"
    ],
    "new_loka": [
        "abating_link","airbust_rounds","anchored_glide","assimilate","axios_javelineers",
        "beguiling_lantern","bright_purit","calm_and_frenzy","cataclysmic_gate","celestial_stomp",
        "champions_blessing","chaos_sphere","conductor","counter_pulse",
        "critical_surge","disarming_purity","duality","elusive_retribution","endless_lullaby",
        "ernergy_transfer","enraged","enveloping_cloud","eternal_war","fracturing_crush",
        "funnel_clouds","fused_reservoir","greed_pull","hallowed_eruption","hallowed_reckoning",
        "hysterical_assault","intrepid_stand","ironclad_flight","jet_stream","lasting_purity",
        "loyal_merulina","magnetized_discharge","mending_splinters","merulinia_guardian",
        "mind_freak","omikujis_fortune","pacifying_bolts","partitioned_mallet","peaceful_provocation",
        "phoenix_renewal","pilfering_swarm","pool_of_life","primal_rage","prolonged_paralysis",
        "razorwing_blitz","reactive_stormi","rousing_plunder","shattered_storm","smite_infusion",
        "spectrosiphon","spectrosiphon","spellbound_harvest","sunging_blades","swift_bite",
        "swift_line","target_fixation","tidal_impunity","valence_formation","vampire_leech",
        "viral_tempest","volatile_recompense","winds_of_purity","wrath_of_ukko"
        ]
    
}

# ===== Funções de consulta =====
async def fetch_mod_data(mod_url_name):
    """Busca orders do mod na API e retorna menor preço entre vendedores ingame."""
    async with aiohttp.ClientSession() as session:
        url = f"{API_BASE_URL}/items/{mod_url_name}/orders"
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    orders = data.get("payload", {}).get("orders", [])
                    online_orders = [
                        order for order in orders
                        if order.get("user", {}).get("status") == "ingame"
                        and order.get("order_type") == "sell"
                    ]
                    if online_orders:
                        min_price = min(order.get("platinum", float("inf")) for order in online_orders)
                        return {
                            "mod_name": mod_url_name.replace("_", " ").title(),
                            "price": min_price,
                            "image_url": f"https://warframe.market/static/assets/{mod_url_name}.png"
                        }
                return None
        except Exception as e:
            print(f"[fetch_mod_data] Erro ao buscar {mod_url_name}: {e}")
            return None

async def get_top_mods(syndicate, limit=5):
    mods = SYNDICATE_MODS.get(syndicate, [])
    mod_data = []
    for mod in mods:
        data = await fetch_mod_data(mod)
        if data:
            mod_data.append(data)
        await asyncio.sleep(0.08)  # pequeno delay para não acelerar demais as requests
    mod_data.sort(key=lambda x: x["price"], reverse=True)
    return mod_data[:limit]

def format_mods_embed(syndicate, mods, title):
    embed = discord.Embed(title=title, color=0x00ff00, timestamp=datetime.utcnow())
    embed.set_footer(text="Dados de warframe.market")
    if mods:
        # usa a imagem do primeiro mod como thumbnail
        embed.set_thumbnail(url=mods[0]["image_url"])
    for mod in mods:
        price = mod["price"]
        price_str = f"{price:.0f}" if isinstance(price, (int, float)) and price == int(price) else f"{price}"
        embed.add_field(
            name=mod["mod_name"],
            value=f"Preço: {price_str} Platina\n[Ver no Warframe Market](https://warframe.market/items/{mod['mod_name'].lower().replace(' ', '_')})",
            inline=False
        )
    return embed

# ===== Scheduler (mantive o seu) =====
scheduler = AsyncIOScheduler(timezone=pytz.timezone("America/Sao_Paulo"))

async def send_daily_message():
    channel = bot.get_channel(YOUR_CHANNEL_ID)
    if not channel:
        print("[send_daily_message] Canal não encontrado")
        return

    for syndicate in SYNDICATE_MODS.keys():
        try:
            mods = await get_top_mods(syndicate, limit=5)
            if mods:
                title = f"Top 5 Mods Mais Caros para {syndicate.replace('_', ' ').title()} - Atualizado"
                embed = format_mods_embed(syndicate, mods, title)
                await channel.send(embed=embed)
            await asyncio.sleep(1)  # evita burst
        except Exception as e:
            print(f"[send_daily_message] Erro ao processar {syndicate}: {e}")

# adiciona jobs (dois horários como no seu original)
scheduler.add_job(send_daily_message, "cron", hour=6, minute=0)
scheduler.add_job(send_daily_message, "cron", hour=12, minute=0)
scheduler.add_job(send_daily_message, "cron", hour=18, minute=0)



# ===== LOGS / EVENTOS =====
@bot.event
async def on_ready():
    print(f"Logado como {bot.user} (ID: {bot.user.id})")
    print("Comandos carregados:")
    for cmd in bot.commands:
        print(f" - {cmd.name} (aliases: {cmd.aliases})")
    # Inicia o scheduler só depois do bot estar pronto
    scheduler.start()
    print("Scheduler iniciado")

@bot.event
async def on_message(message):
    # ignora bots
    if message.author.bot:
        return
    print(f"[MSG] {message.author} em {message.channel}: {message.content}")
    await bot.process_commands(message)  # muito importante para executar comandos

@bot.event
async def on_command(ctx):
    # log quando um comando é executado
    print(f"[CMD] {ctx.command} invocado por {ctx.author} em {ctx.channel}")

@bot.event
async def on_command_error(ctx, error):
    print(f"[ERR] erro no comando {ctx.command} por {ctx.author}: {error}")
    # opcional: avisar o usuário
    try:
        await ctx.send("❌ Ocorreu um erro ao executar o comando.")
    except Exception:
        pass

# ===== COMANDOS BÁSICOS =====
@bot.command(name="ping")
async def ping(ctx):
    print(f"[CMD] /ping chamado por {ctx.author}")
    await ctx.send("Pong!")

@bot.command(name="ajuda", aliases=["socorro"])
async def ajuda(ctx):
    cmds = [f"`{COMMAND_PREFIX}{c.name}`" for c in bot.commands]
    texto = "📌 Comandos disponíveis:\n" + "\n".join(cmds)
    await ctx.send(texto)

@bot.command(name="top")
async def top_mods(ctx):
    await ctx.send("🔎 Buscando os 5 mods mais caros entre todos os sindicatos... (aguarde)")

    all_mods = []

    # Para cada sindicato e seus mods
    for syndicate, mods in SYNDICATE_MODS.items():
        for mod in mods:
            data = await fetch_mod_data(mod)
            if data:
                # Acrescenta o nome do sindicato na info
                data["syndicate"] = syndicate.replace("_", " ").title()
                all_mods.append(data)
            await asyncio.sleep(0.08)  # respeitando delay

    # Ordena do maior para o menor preço
    all_mods.sort(key=lambda x: x["price"], reverse=True)

    top_5 = all_mods[:5]
    if not top_5:
        await ctx.send("❌ Não foi possível obter dados para os mods.")
        return

    # Monta embed para mostrar a lista
    embed = discord.Embed(
        title="🏆 Top 5 Mods Mais Caros entre Todos os Sindicatos",
        color=0xffd700,
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text="Dados de warframe.market")

    for mod in top_5:
        price_str = f"{mod['price']:.0f}" if isinstance(mod['price'], (int, float)) and mod['price'] == int(mod['price']) else f"{mod['price']}"
        embed.add_field(
            name=mod["mod_name"],
            value=f"Preço: {price_str} Platina\nSindicato: {mod['syndicate']}\n[Ver no Warframe Market](https://warframe.market/items/{mod['mod_name'].lower().replace(' ', '_')})",
            inline=False
        )

    embed.set_thumbnail(url=top_5[0]["image_url"])  # thumbnail com mod mais caro
    await ctx.send(embed=embed)


# ===== CRIA COMANDOS DINAMICAMENTE PARA CADA SINDICATO =====
# Permite !cephalon_suda e também !cephalon-suda (alias)
for syndicate in SYNDICATE_MODS.keys():
    cmd_name = syndicate  # exemplo: "cephalon_suda"
    hyphen_alias = syndicate.replace("_", "-")

    async def _make_command(ctx, synd=syndicate):
        print(f"[CMD] !{synd} solicitado por {ctx.author}")
        await ctx.send(f"🔎 Buscando top mods para **{synd.replace('_', ' ').title()}**... (pode levar alguns segundos)")
        mods = await get_top_mods(synd, limit=3)
        if mods:
            title = f"Top 3 Mods Mais Caros para {synd.replace('_',' ').title()}"
            embed = format_mods_embed(synd, mods, title)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Nenhum dado disponível para os mods de {synd.replace('_',' ').title()}.")

    # registra o comando no bot com alias
    _make_command.__name__ = f"cmd_{cmd_name}"  # nome único para a função
    bot.command(name=cmd_name, aliases=[hyphen_alias])(_make_command)

# ===== INICIAÇÃO =====
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
