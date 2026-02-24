from app import app, db, Game
from datetime import datetime

# Comprehensive game database with CORRECT cover URLs
GAMES_DATA = [
    # RPGs
    {"external_id": "g_elden_ring", "title": "Elden Ring", "studio": "FromSoftware", "release_year": 2022, "description": "Epic open-world action RPG from the creators of Dark Souls", "cover_url": "/uploads/covers/g_elden_ring.jpg"},
    {"external_id": "g_witcher3", "title": "The Witcher 3: Wild Hunt", "studio": "CD Projekt Red", "release_year": 2015, "description": "Open world RPG following Geralt of Rivia", "cover_url": "/uploads/covers/g_witcher3.jpg"},
    {"external_id": "g_skyrim", "title": "The Elder Scrolls V: Skyrim", "studio": "Bethesda Game Studios", "release_year": 2011, "description": "Open-world fantasy RPG set in the land of Skyrim", "cover_url": "/uploads/covers/g_skyrim.jpg"},
    {"external_id": "g_baldurs_gate3", "title": "Baldur's Gate 3", "studio": "Larian Studios", "release_year": 2023, "description": "Epic D&D-based RPG with deep choices", "cover_url": "/uploads/covers/g_baldurs_gate3.jpg"},
    {"external_id": "g_cyberpunk2077", "title": "Cyberpunk 2077", "studio": "CD Projekt Red", "release_year": 2020, "description": "Open-world sci-fi RPG set in Night City", "cover_url": "/uploads/covers/g_cyberpunk2077.jpg"},
    {"external_id": "g_ff7_remake", "title": "Final Fantasy VII Remake", "studio": "Square Enix", "release_year": 2020, "description": "Reimagining of the classic JRPG", "cover_url": "/uploads/covers/g_ff7_remake.jpg"},
    {"external_id": "g_persona5", "title": "Persona 5 Royal", "studio": "Atlus", "release_year": 2019, "description": "Stylish JRPG about phantom thieves", "cover_url": "/uploads/covers/g_persona5.jpg"},
    {"external_id": "g_dark_souls3", "title": "Dark Souls III", "studio": "FromSoftware", "release_year": 2016, "description": "Challenging action RPG", "cover_url": "/uploads/covers/g_dark_souls3.jpg"},
    {"external_id": "g_bloodborne", "title": "Bloodborne", "studio": "FromSoftware", "release_year": 2015, "description": "Gothic horror action RPG", "cover_url": "/uploads/covers/g_bloodborne.jpg"},
    {"external_id": "g_sekiro", "title": "Sekiro: Shadows Die Twice", "studio": "FromSoftware", "release_year": 2019, "description": "Challenging samurai action game", "cover_url": "/uploads/covers/g_sekiro.jpg"},
    
    # Action/Adventure
    {"external_id": "g_zelda_botw", "title": "The Legend of Zelda: Breath of the Wild", "studio": "Nintendo EPD", "release_year": 2017, "description": "Revolutionary open-world Zelda adventure", "cover_url": "/uploads/covers/g_zelda_botw.jpg"},
    {"external_id": "g_zelda_totk", "title": "The Legend of Zelda: Tears of the Kingdom", "studio": "Nintendo EPD", "release_year": 2023, "description": "Sequel to Breath of the Wild with new mechanics", "cover_url": "/uploads/covers/g_zelda_totk.jpg"},
    {"external_id": "g_god_of_war", "title": "God of War (2018)", "studio": "Santa Monica Studio", "release_year": 2018, "description": "Norse mythology action-adventure", "cover_url": "/uploads/covers/g_god_of_war.jpg"},
    {"external_id": "g_god_of_war_ragnarok", "title": "God of War Ragnarök", "studio": "Santa Monica Studio", "release_year": 2022, "description": "Epic conclusion to the Norse saga", "cover_url": "/uploads/covers/g_god_of_war_ragnarok.jpg"},
    {"external_id": "g_last_of_us", "title": "The Last of Us", "studio": "Naughty Dog", "release_year": 2013, "description": "Post-apocalyptic survival story", "cover_url": "/uploads/covers/g_last_of_us.jpg"},
    {"external_id": "g_last_of_us2", "title": "The Last of Us Part II", "studio": "Naughty Dog", "release_year": 2020, "description": "Emotionally intense sequel", "cover_url": "/uploads/covers/g_last_of_us2.jpg"},
    {"external_id": "g_rdr2", "title": "Red Dead Redemption 2", "studio": "Rockstar Studios", "release_year": 2018, "description": "Epic Western open-world adventure", "cover_url": "/uploads/covers/g_rdr2.jpg"},
    {"external_id": "g_gta5", "title": "Grand Theft Auto V", "studio": "Rockstar North", "release_year": 2013, "description": "Open-world crime adventure", "cover_url": "/uploads/covers/g_gta5.jpg"},
    {"external_id": "g_uncharted4", "title": "Uncharted 4: A Thief's End", "studio": "Naughty Dog", "release_year": 2016, "description": "Treasure hunting adventure", "cover_url": "/uploads/covers/g_uncharted4.jpg"},
    {"external_id": "g_horizon_zd", "title": "Horizon Zero Dawn", "studio": "Guerrilla Games", "release_year": 2017, "description": "Post-apocalyptic robot hunting", "cover_url": "/uploads/covers/g_horizon_zd.jpg"},
    {"external_id": "g_horizon_fw", "title": "Horizon Forbidden West", "studio": "Guerrilla Games", "release_year": 2022, "description": "Sequel with expanded world", "cover_url": "/uploads/covers/g_horizon_fw.jpg"},
    {"external_id": "g_ghost_tsushima", "title": "Ghost of Tsushima", "studio": "Sucker Punch Productions", "release_year": 2020, "description": "Samurai adventure in feudal Japan", "cover_url": "/uploads/covers/g_ghost_tsushima.jpg"},
    {"external_id": "g_spiderman", "title": "Marvel's Spider-Man", "studio": "Insomniac Games", "release_year": 2018, "description": "Open-world Spider-Man adventure", "cover_url": "/uploads/covers/g_spiderman.jpg"},
    {"external_id": "g_spiderman2", "title": "Marvel's Spider-Man 2", "studio": "Insomniac Games", "release_year": 2023, "description": "Dual protagonist Spider-Man sequel", "cover_url": "/uploads/covers/g_spiderman2.jpg"},
    
    # Shooters
    {"external_id": "g_halo_infinite", "title": "Halo Infinite", "studio": "343 Industries", "release_year": 2021, "description": "Latest entry in the Halo franchise", "cover_url": "/uploads/covers/g_halo_infinite.jpg"},
    {"external_id": "g_cod_mw2", "title": "Call of Duty: Modern Warfare II", "studio": "Infinity Ward", "release_year": 2022, "description": "Military FPS", "cover_url": "/uploads/covers/g_cod_mw2.jpg"},
    {"external_id": "g_apex", "title": "Apex Legends", "studio": "Respawn Entertainment", "release_year": 2019, "description": "Battle royale with hero abilities", "cover_url": "/uploads/covers/g_apex.jpg"},
    {"external_id": "g_valorant", "title": "Valorant", "studio": "Riot Games", "release_year": 2020, "description": "Tactical 5v5 hero shooter", "cover_url": "/uploads/covers/g_valorant.jpg"},
    {"external_id": "g_overwatch2", "title": "Overwatch 2", "studio": "Blizzard Entertainment", "release_year": 2022, "description": "Team-based hero shooter", "cover_url": "/uploads/covers/g_overwatch2.jpg"},
    {"external_id": "g_doom_eternal", "title": "DOOM Eternal", "studio": "id Software", "release_year": 2020, "description": "Fast-paced demon slaying FPS", "cover_url": "/uploads/covers/g_doom_eternal.jpg"},
    {"external_id": "g_csgo", "title": "Counter-Strike: Global Offensive", "studio": "Valve", "release_year": 2012, "description": "Competitive tactical shooter", "cover_url": "/uploads/covers/g_csgo.jpg"},
    {"external_id": "g_titanfall2", "title": "Titanfall 2", "studio": "Respawn Entertainment", "release_year": 2016, "description": "Mech-based FPS with parkour", "cover_url": "/uploads/covers/g_titanfall2.jpg"},
    
    # Multiplayer/Battle Royale
    {"external_id": "g_fortnite", "title": "Fortnite", "studio": "Epic Games", "release_year": 2017, "description": "Battle royale with building mechanics", "cover_url": "/uploads/covers/g_fortnite.jpg"},
    {"external_id": "g_pubg", "title": "PlayerUnknown's Battlegrounds", "studio": "PUBG Studios", "release_year": 2017, "description": "Realistic battle royale", "cover_url": "/uploads/covers/g_pubg.jpg"},
    {"external_id": "g_warzone", "title": "Call of Duty: Warzone", "studio": "Infinity Ward", "release_year": 2020, "description": "Free-to-play battle royale", "cover_url": "/uploads/covers/g_warzone.jpg"},
    
    # Indie Games
    {"external_id": "g_hollow_knight", "title": "Hollow Knight", "studio": "Team Cherry", "release_year": 2017, "description": "Metroidvania masterpiece", "cover_url": "/uploads/covers/g_hollow_knight.jpg"},
    {"external_id": "g_celeste", "title": "Celeste", "studio": "Maddy Makes Games", "release_year": 2018, "description": "Challenging precision platformer", "cover_url": "/uploads/covers/g_celeste.jpg"},
    {"external_id": "g_hades", "title": "Hades", "studio": "Supergiant Games", "release_year": 2020, "description": "Roguelike dungeon crawler", "cover_url": "/uploads/covers/g_hades.jpg"},
    {"external_id": "g_stardew", "title": "Stardew Valley", "studio": "ConcernedApe", "release_year": 2016, "description": "Farming and life simulation", "cover_url": "/uploads/covers/g_stardew.jpg"},
    {"external_id": "g_terraria", "title": "Terraria", "studio": "Re-Logic", "release_year": 2011, "description": "2D sandbox adventure", "cover_url": "/uploads/covers/g_terraria.jpg"},
    {"external_id": "g_undertale", "title": "Undertale", "studio": "Toby Fox", "release_year": 2015, "description": "Unique RPG with moral choices", "cover_url": "/uploads/covers/g_undertale.jpg"},
    {"external_id": "g_cuphead", "title": "Cuphead", "studio": "Studio MDHR", "release_year": 2017, "description": "Run and gun with 1930s animation style", "cover_url": "/uploads/covers/g_cuphead.jpg"},
    
    # Strategy
    {"external_id": "g_civ6", "title": "Civilization VI", "studio": "Firaxis Games", "release_year": 2016, "description": "Turn-based strategy empire builder", "cover_url": "/uploads/covers/g_civ6.jpg"},
    {"external_id": "g_starcraft2", "title": "StarCraft II", "studio": "Blizzard Entertainment", "release_year": 2010, "description": "Real-time strategy masterpiece", "cover_url": "/uploads/covers/g_starcraft2.jpg"},
    {"external_id": "g_xcom2", "title": "XCOM 2", "studio": "Firaxis Games", "release_year": 2016, "description": "Tactical turn-based strategy", "cover_url": "/uploads/covers/g_xcom2.jpg"},
    {"external_id": "g_total_war_wh3", "title": "Total War: Warhammer III", "studio": "Creative Assembly", "release_year": 2022, "description": "Epic fantasy strategy battles", "cover_url": "/uploads/covers/g_total_war_wh3.jpg"},
    
    # Simulation/Sandbox
    {"external_id": "g_minecraft", "title": "Minecraft", "studio": "Mojang Studios", "release_year": 2011, "description": "Blocky sandbox creativity", "cover_url": "/uploads/covers/g_minecraft.jpg"},
    {"external_id": "g_cities_skylines", "title": "Cities: Skylines", "studio": "Colossal Order", "release_year": 2015, "description": "City-building simulation", "cover_url": "/uploads/covers/g_cities_skylines.jpg"},
    {"external_id": "g_sims4", "title": "The Sims 4", "studio": "Maxis", "release_year": 2014, "description": "Life simulation", "cover_url": "/uploads/covers/g_sims4.jpg"},
    {"external_id": "g_kerbal", "title": "Kerbal Space Program", "studio": "Squad", "release_year": 2015, "description": "Space program simulation", "cover_url": "/uploads/covers/g_kerbal.jpg"},
    
    # Horror
    {"external_id": "g_re_village", "title": "Resident Evil Village", "studio": "Capcom", "release_year": 2021, "description": "Survival horror in a mysterious village", "cover_url": "/uploads/covers/g_re_village.jpg"},
    {"external_id": "g_re2_remake", "title": "Resident Evil 2 Remake", "studio": "Capcom", "release_year": 2019, "description": "Reimagined survival horror classic", "cover_url": "/uploads/covers/g_re2_remake.jpg"},
    {"external_id": "g_silent_hill2", "title": "Silent Hill 2", "studio": "Konami", "release_year": 2001, "description": "Psychological horror masterpiece", "cover_url": "/uploads/covers/g_silent_hill2.jpg"},
    {"external_id": "g_alan_wake2", "title": "Alan Wake 2", "studio": "Remedy Entertainment", "release_year": 2023, "description": "Horror thriller sequel", "cover_url": "/uploads/covers/g_alan_wake2.jpg"},
    
    # Sports/Racing
    {"external_id": "g_fifa23", "title": "FIFA 23", "studio": "EA Sports", "release_year": 2022, "description": "Soccer simulation", "cover_url": "/uploads/covers/g_fifa23.jpg"},
    {"external_id": "g_nba2k23", "title": "NBA 2K23", "studio": "Visual Concepts", "release_year": 2022, "description": "Basketball simulation", "cover_url": "/uploads/covers/g_nba2k23.jpg"},
    {"external_id": "g_forza_horizon5", "title": "Forza Horizon 5", "studio": "Playground Games", "release_year": 2021, "description": "Open-world racing in Mexico", "cover_url": "/uploads/covers/g_forza_horizon5.jpg"},
    {"external_id": "g_gran_turismo7", "title": "Gran Turismo 7", "studio": "Polyphony Digital", "release_year": 2022, "description": "Realistic racing simulator", "cover_url": "/uploads/covers/g_gran_turismo7.jpg"},
    
    # Nintendo Classics
    {"external_id": "g_mario_odyssey", "title": "Super Mario Odyssey", "studio": "Nintendo EPD", "release_year": 2017, "description": "3D Mario platforming adventure", "cover_url": "/uploads/covers/g_mario_odyssey.jpg"},
    {"external_id": "g_mario_kart8", "title": "Mario Kart 8 Deluxe", "studio": "Nintendo EPD", "release_year": 2017, "description": "Kart racing with Nintendo characters", "cover_url": "/uploads/covers/g_mario_kart8.jpg"},
    {"external_id": "g_smash_ultimate", "title": "Super Smash Bros. Ultimate", "studio": "Bandai Namco", "release_year": 2018, "description": "Platform fighter with 80+ characters", "cover_url": "/uploads/covers/g_smash_ultimate.jpg"},
    {"external_id": "g_animal_crossing", "title": "Animal Crossing: New Horizons", "studio": "Nintendo EPD", "release_year": 2020, "description": "Life simulation on a deserted island", "cover_url": "/uploads/covers/g_animal_crossing.jpg"},
    {"external_id": "g_metroid_dread", "title": "Metroid Dread", "studio": "MercurySteam", "release_year": 2021, "description": "2D action-adventure Metroidvania", "cover_url": "/uploads/covers/g_metroid_dread.jpg"},
    {"external_id": "g_pokemon_sv", "title": "Pokémon Scarlet and Violet", "studio": "Game Freak", "release_year": 2022, "description": "Open-world Pokémon adventure", "cover_url": "/uploads/covers/g_pokemon_sv.jpg"},
    
    # MMOs/Online
    {"external_id": "g_ff14", "title": "Final Fantasy XIV", "studio": "Square Enix", "release_year": 2013, "description": "Story-driven MMORPG", "cover_url": "/uploads/covers/g_ff14.jpg"},
    {"external_id": "g_wow", "title": "World of Warcraft", "studio": "Blizzard Entertainment", "release_year": 2004, "description": "Legendary MMORPG", "cover_url": "/uploads/covers/g_wow.jpg"},
    {"external_id": "g_destiny2", "title": "Destiny 2", "studio": "Bungie", "release_year": 2017, "description": "Sci-fi looter shooter", "cover_url": "/uploads/covers/g_destiny2.jpg"},
    {"external_id": "g_lol", "title": "League of Legends", "studio": "Riot Games", "release_year": 2009, "description": "MOBA with competitive scene", "cover_url": "/uploads/covers/g_lol.jpg"},
    {"external_id": "g_dota2", "title": "Dota 2", "studio": "Valve", "release_year": 2013, "description": "Complex competitive MOBA", "cover_url": "/uploads/covers/g_dota2.jpg"},
    
    # Platformers
    {"external_id": "g_it_takes_two", "title": "It Takes Two", "studio": "Hazelight Studios", "release_year": 2021, "description": "Co-op adventure platformer", "cover_url": "/uploads/covers/g_it_takes_two.jpg"},
    {"external_id": "g_psychonauts2", "title": "Psychonauts 2", "studio": "Double Fine", "release_year": 2021, "description": "Creative platformer adventure", "cover_url": "/uploads/covers/g_psychonauts2.jpg"},
    {"external_id": "g_ratchet_clank", "title": "Ratchet & Clank: Rift Apart", "studio": "Insomniac Games", "release_year": 2021, "description": "Dimension-hopping platformer", "cover_url": "/uploads/covers/g_ratchet_clank.jpg"},
    
    # Fighting
    {"external_id": "g_street_fighter6", "title": "Street Fighter 6", "studio": "Capcom", "release_year": 2023, "description": "Latest fighting game evolution", "cover_url": "/uploads/covers/g_street_fighter6.jpg"},
    {"external_id": "g_tekken8", "title": "Tekken 8", "studio": "Bandai Namco", "release_year": 2024, "description": "3D fighting game", "cover_url": "/uploads/covers/g_tekken8.jpg"},
    {"external_id": "g_mk11", "title": "Mortal Kombat 11", "studio": "NetherRealm Studios", "release_year": 2019, "description": "Brutal fighting game", "cover_url": "/uploads/covers/g_mk11.jpg"},
]

def seed_games():
    """Seed database with comprehensive game list"""
    with app.app_context():
        added_count = 0
        updated_count = 0
        
        for game_data in GAMES_DATA:
            # Check if game already exists
            existing_game = Game.query.filter_by(external_id=game_data['external_id']).first()
            
            if existing_game:
                # Update existing game
                existing_game.title = game_data['title']
                existing_game.studio = game_data['studio']
                existing_game.release_year = game_data['release_year']
                existing_game.description = game_data.get('description', '')
                existing_game.cover_url = game_data.get('cover_url', f"/uploads/covers/{game_data['external_id']}.jpg")
                updated_count += 1
            else:
                # Create new game
                game = Game(
                    external_id=game_data['external_id'],
                    title=game_data['title'],
                    studio=game_data['studio'],
                    release_year=game_data['release_year'],
                    description=game_data.get('description', ''),
                    cover_url=game_data.get('cover_url', f"/uploads/covers/{game_data['external_id']}.jpg")
                )
                db.session.add(game)
                added_count += 1
        
        try:
            db.session.commit()
            print(f"\n✅ Game seeding complete!")
            print(f"   Added: {added_count} new games")
            print(f"   Updated: {updated_count} existing games")
            print(f"   Total games in database: {Game.query.count()}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error seeding games: {e}")

if __name__ == '__main__':
    print("Starting game database seeding...")
    seed_games()