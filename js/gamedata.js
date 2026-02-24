/* js/gamedata.js */
// Comprehensive game database seed
window.MB_GAMES_SEED = [
  // RPGs
  { id: "g_elden_ring", title: "Elden Ring", studio: "FromSoftware", releaseYear: 2022, cover: "covers/g_elden_ring.jpg", description: "Epic open-world action RPG from the creators of Dark Souls" },
  { id: "g_witcher3", title: "The Witcher 3: Wild Hunt", studio: "CD Projekt Red", releaseYear: 2015, cover: "covers/g_witcher3.jpg", description: "Open world RPG following Geralt of Rivia" },
  { id: "g_skyrim", title: "The Elder Scrolls V: Skyrim", studio: "Bethesda Game Studios", releaseYear: 2011, cover: "covers/g_skyrim.jpg", description: "Open-world fantasy RPG set in the land of Skyrim" },
  { id: "g_baldurs_gate3", title: "Baldur's Gate 3", studio: "Larian Studios", releaseYear: 2023, cover: "covers/g_baldurs_gate3.jpg", description: "Epic D&D-based RPG with deep choices" },
  { id: "g_cyberpunk2077", title: "Cyberpunk 2077", studio: "CD Projekt Red", releaseYear: 2020, cover: "covers/g_cyberpunk2077.jpg", description: "Open-world sci-fi RPG set in Night City" },
  { id: "g_ff7_remake", title: "Final Fantasy VII Remake", studio: "Square Enix", releaseYear: 2020, cover: "covers/g_ff7_remake.jpg", description: "Reimagining of the classic JRPG" },
  { id: "g_persona5", title: "Persona 5 Royal", studio: "Atlus", releaseYear: 2019, cover: "covers/g_persona5.jpg", description: "Stylish JRPG about phantom thieves" },
  { id: "g_dark_souls3", title: "Dark Souls III", studio: "FromSoftware", releaseYear: 2016, cover: "covers/g_dark_souls3.jpg", description: "Challenging action RPG" },
  { id: "g_bloodborne", title: "Bloodborne", studio: "FromSoftware", releaseYear: 2015, cover: "covers/g_bloodborne.jpg", description: "Gothic horror action RPG" },
  { id: "g_sekiro", title: "Sekiro: Shadows Die Twice", studio: "FromSoftware", releaseYear: 2019, cover: "covers/g_sekiro.jpg", description: "Challenging samurai action game" },

  // Action/Adventure
  { id: "g_zelda_botw", title: "The Legend of Zelda: Breath of the Wild", studio: "Nintendo EPD", releaseYear: 2017, cover: "covers/g_zelda_botw.jpg", description: "Revolutionary open-world Zelda adventure" },
  { id: "g_zelda_totk", title: "The Legend of Zelda: Tears of the Kingdom", studio: "Nintendo EPD", releaseYear: 2023, cover: "covers/g_zelda_totk.jpg", description: "Sequel to Breath of the Wild with new mechanics" },
  { id: "g_god_of_war", title: "God of War (2018)", studio: "Santa Monica Studio", releaseYear: 2018, cover: "covers/g_god_of_war.jpg", description: "Norse mythology action-adventure" },
  { id: "g_god_of_war_ragnarok", title: "God of War Ragnarök", studio: "Santa Monica Studio", releaseYear: 2022, cover: "covers/g_god_of_war_ragnarok.jpg", description: "Epic conclusion to the Norse saga" },
  { id: "g_last_of_us", title: "The Last of Us", studio: "Naughty Dog", releaseYear: 2013, cover: "covers/g_last_of_us.jpg", description: "Post-apocalyptic survival story" },
  { id: "g_last_of_us2", title: "The Last of Us Part II", studio: "Naughty Dog", releaseYear: 2020, cover: "covers/g_last_of_us2.jpg", description: "Emotionally intense sequel" },
  { id: "g_rdr2", title: "Red Dead Redemption 2", studio: "Rockstar Studios", releaseYear: 2018, cover: "covers/g_rdr2.jpg", description: "Epic Western open-world adventure" },
  { id: "g_gta5", title: "Grand Theft Auto V", studio: "Rockstar North", releaseYear: 2013, cover: "covers/g_gta5.jpg", description: "Open-world crime adventure" },
  { id: "g_uncharted4", title: "Uncharted 4: A Thief's End", studio: "Naughty Dog", releaseYear: 2016, cover: "covers/g_uncharted4.jpg", description: "Treasure hunting adventure" },
  { id: "g_horizon_zd", title: "Horizon Zero Dawn", studio: "Guerrilla Games", releaseYear: 2017, cover: "covers/g_horizon_zd.jpg", description: "Post-apocalyptic robot hunting" },
  { id: "g_horizon_fw", title: "Horizon Forbidden West", studio: "Guerrilla Games", releaseYear: 2022, cover: "covers/g_horizon_fw.jpg", description: "Sequel with expanded world" },
  { id: "g_ghost_tsushima", title: "Ghost of Tsushima", studio: "Sucker Punch Productions", releaseYear: 2020, cover: "covers/g_ghost_tsushima.jpg", description: "Samurai adventure in feudal Japan" },
  { id: "g_spiderman", title: "Marvel's Spider-Man", studio: "Insomniac Games", releaseYear: 2018, cover: "covers/g_spiderman.jpg", description: "Open-world Spider-Man adventure" },
  { id: "g_spiderman2", title: "Marvel's Spider-Man 2", studio: "Insomniac Games", releaseYear: 2023, cover: "covers/g_spiderman2.jpg", description: "Dual protagonist Spider-Man sequel" },

  // Shooters
  { id: "g_halo_infinite", title: "Halo Infinite", studio: "343 Industries", releaseYear: 2021, cover: "covers/g_halo_infinite.jpg", description: "Latest entry in the Halo franchise" },
  { id: "g_cod_mw2", title: "Call of Duty: Modern Warfare II", studio: "Infinity Ward", releaseYear: 2022, cover: "covers/g_cod_mw2.jpg", description: "Military FPS" },
  { id: "g_apex", title: "Apex Legends", studio: "Respawn Entertainment", releaseYear: 2019, cover: "covers/g_apex.jpg", description: "Battle royale with hero abilities" },
  { id: "g_valorant", title: "Valorant", studio: "Riot Games", releaseYear: 2020, cover: "covers/g_valorant.jpg", description: "Tactical 5v5 hero shooter" },
  { id: "g_overwatch2", title: "Overwatch 2", studio: "Blizzard Entertainment", releaseYear: 2022, cover: "covers/g_overwatch2.jpg", description: "Team-based hero shooter" },
  { id: "g_doom_eternal", title: "DOOM Eternal", studio: "id Software", releaseYear: 2020, cover: "covers/g_doom_eternal.jpg", description: "Fast-paced demon slaying FPS" },
  { id: "g_csgo", title: "Counter-Strike: Global Offensive", studio: "Valve", releaseYear: 2012, cover: "covers/g_csgo.jpg", description: "Competitive tactical shooter" },
  { id: "g_titanfall2", title: "Titanfall 2", studio: "Respawn Entertainment", releaseYear: 2016, cover: "covers/g_titanfall2.jpg", description: "Mech-based FPS with parkour" },

  // Multiplayer/Battle Royale
  { id: "g_fortnite", title: "Fortnite", studio: "Epic Games", releaseYear: 2017, cover: "covers/g_fortnite.jpg", description: "Battle royale with building mechanics" },
  { id: "g_pubg", title: "PlayerUnknown's Battlegrounds", studio: "PUBG Studios", releaseYear: 2017, cover: "covers/g_pubg.jpg", description: "Realistic battle royale" },
  { id: "g_warzone", title: "Call of Duty: Warzone", studio: "Infinity Ward", releaseYear: 2020, cover: "covers/g_warzone.jpg", description: "Free-to-play battle royale" },

  // Indie Games
  { id: "g_hollow_knight", title: "Hollow Knight", studio: "Team Cherry", releaseYear: 2017, cover: "covers/g_hollow_knight.jpg", description: "Metroidvania masterpiece" },
  { id: "g_celeste", title: "Celeste", studio: "Maddy Makes Games", releaseYear: 2018, cover: "covers/g_celeste.jpg", description: "Challenging precision platformer" },
  { id: "g_hades", title: "Hades", studio: "Supergiant Games", releaseYear: 2020, cover: "covers/g_hades.jpg", description: "Roguelike dungeon crawler" },
  { id: "g_stardew", title: "Stardew Valley", studio: "ConcernedApe", releaseYear: 2016, cover: "covers/g_stardew.jpg", description: "Farming and life simulation" },
  { id: "g_terraria", title: "Terraria", studio: "Re-Logic", releaseYear: 2011, cover: "covers/g_terraria.jpg", description: "2D sandbox adventure" },
  { id: "g_undertale", title: "Undertale", studio: "Toby Fox", releaseYear: 2015, cover: "covers/g_undertale.jpg", description: "Unique RPG with moral choices" },
  { id: "g_cuphead", title: "Cuphead", studio: "Studio MDHR", releaseYear: 2017, cover: "covers/g_cuphead.jpg", description: "Run and gun with 1930s animation style" },

  // Strategy
  { id: "g_civ6", title: "Civilization VI", studio: "Firaxis Games", releaseYear: 2016, cover: "covers/g_civ6.jpg", description: "Turn-based strategy empire builder" },
  { id: "g_starcraft2", title: "StarCraft II", studio: "Blizzard Entertainment", releaseYear: 2010, cover: "covers/g_starcraft2.jpg", description: "Real-time strategy masterpiece" },
  { id: "g_xcom2", title: "XCOM 2", studio: "Firaxis Games", releaseYear: 2016, cover: "covers/g_xcom2.jpg", description: "Tactical turn-based strategy" },
  { id: "g_total_war_wh3", title: "Total War: Warhammer III", studio: "Creative Assembly", releaseYear: 2022, cover: "covers/g_total_war_wh3.jpg", description: "Epic fantasy strategy battles" },

  // Simulation/Sandbox
  { id: "g_minecraft", title: "Minecraft", studio: "Mojang Studios", releaseYear: 2011, cover: "covers/g_minecraft.jpg", description: "Blocky sandbox creativity" },
  { id: "g_cities_skylines", title: "Cities: Skylines", studio: "Colossal Order", releaseYear: 2015, cover: "covers/g_cities_skylines.jpg", description: "City-building simulation" },
  { id: "g_sims4", title: "The Sims 4", studio: "Maxis", releaseYear: 2014, cover: "covers/g_sims4.jpg", description: "Life simulation" },
  { id: "g_kerbal", title: "Kerbal Space Program", studio: "Squad", releaseYear: 2015, cover: "covers/g_kerbal.jpg", description: "Space program simulation" },

  // Horror
  { id: "g_re_village", title: "Resident Evil Village", studio: "Capcom", releaseYear: 2021, cover: "covers/g_re_village.jpg", description: "Survival horror in a mysterious village" },
  { id: "g_re2_remake", title: "Resident Evil 2 Remake", studio: "Capcom", releaseYear: 2019, cover: "covers/g_re2_remake.jpg", description: "Reimagined survival horror classic" },
  { id: "g_silent_hill2", title: "Silent Hill 2", studio: "Konami", releaseYear: 2001, cover: "covers/g_silent_hill2.jpg", description: "Psychological horror masterpiece" },
  { id: "g_alan_wake2", title: "Alan Wake 2", studio: "Remedy Entertainment", releaseYear: 2023, cover: "covers/g_alan_wake2.jpg", description: "Horror thriller sequel" },

  // Sports/Racing
  { id: "g_fifa23", title: "FIFA 23", studio: "EA Sports", releaseYear: 2022, cover: "covers/g_fifa23.jpg", description: "Soccer simulation" },
  { id: "g_nba2k23", title: "NBA 2K23", studio: "Visual Concepts", releaseYear: 2022, cover: "covers/g_nba2k23.jpg", description: "Basketball simulation" },
  { id: "g_forza_horizon5", title: "Forza Horizon 5", studio: "Playground Games", releaseYear: 2021, cover: "covers/g_forza_horizon5.jpg", description: "Open-world racing in Mexico" },
  { id: "g_gran_turismo7", title: "Gran Turismo 7", studio: "Polyphony Digital", releaseYear: 2022, cover: "covers/g_gran_turismo7.jpg", description: "Realistic racing simulator" },

  // Nintendo Classics
  { id: "g_mario_odyssey", title: "Super Mario Odyssey", studio: "Nintendo EPD", releaseYear: 2017, cover: "covers/g_mario_odyssey.jpg", description: "3D Mario platforming adventure" },
  { id: "g_mario_kart8", title: "Mario Kart 8 Deluxe", studio: "Nintendo EPD", releaseYear: 2017, cover: "covers/g_mario_kart8.jpg", description: "Kart racing with Nintendo characters" },
  { id: "g_smash_ultimate", title: "Super Smash Bros. Ultimate", studio: "Bandai Namco", releaseYear: 2018, cover: "covers/g_smash_ultimate.jpg", description: "Platform fighter with 80+ characters" },
  { id: "g_animal_crossing", title: "Animal Crossing: New Horizons", studio: "Nintendo EPD", releaseYear: 2020, cover: "covers/g_animal_crossing.jpg", description: "Life simulation on a deserted island" },
  { id: "g_metroid_dread", title: "Metroid Dread", studio: "MercurySteam", releaseYear: 2021, cover: "covers/g_metroid_dread.jpg", description: "2D action-adventure Metroidvania" },
  { id: "g_pokemon_sv", title: "Pokémon Scarlet and Violet", studio: "Game Freak", releaseYear: 2022, cover: "covers/g_pokemon_sv.jpg", description: "Open-world Pokémon adventure" },

  // MMOs/Online
  { id: "g_ff14", title: "Final Fantasy XIV", studio: "Square Enix", releaseYear: 2013, cover: "covers/g_ff14.jpg", description: "Story-driven MMORPG" },
  { id: "g_wow", title: "World of Warcraft", studio: "Blizzard Entertainment", releaseYear: 2004, cover: "covers/g_wow.jpg", description: "Legendary MMORPG" },
  { id: "g_destiny2", title: "Destiny 2", studio: "Bungie", releaseYear: 2017, cover: "covers/g_destiny2.jpg", description: "Sci-fi looter shooter" },
  { id: "g_lol", title: "League of Legends", studio: "Riot Games", releaseYear: 2009, cover: "covers/g_lol.jpg", description: "MOBA with competitive scene" },
  { id: "g_dota2", title: "Dota 2", studio: "Valve", releaseYear: 2013, cover: "covers/g_dota2.jpg", description: "Complex competitive MOBA" },

  // Platformers
  { id: "g_it_takes_two", title: "It Takes Two", studio: "Hazelight Studios", releaseYear: 2021, cover: "covers/g_it_takes_two.jpg", description: "Co-op adventure platformer" },
  { id: "g_psychonauts2", title: "Psychonauts 2", studio: "Double Fine", releaseYear: 2021, cover: "covers/g_psychonauts2.jpg", description: "Creative platformer adventure" },
  { id: "g_ratchet_clank", title: "Ratchet & Clank: Rift Apart", studio: "Insomniac Games", releaseYear: 2021, cover: "covers/g_ratchet_clank.jpg", description: "Dimension-hopping platformer" },

  // Fighting
  { id: "g_street_fighter6", title: "Street Fighter 6", studio: "Capcom", releaseYear: 2023, cover: "covers/g_street_fighter6.jpg", description: "Latest fighting game evolution" },
  { id: "g_tekken8", title: "Tekken 8", studio: "Bandai Namco", releaseYear: 2024, cover: "covers/g_tekken8.jpg", description: "3D fighting game" },
  { id: "g_mk11", title: "Mortal Kombat 11", studio: "NetherRealm Studios", releaseYear: 2019, cover: "covers/g_mk11.jpg", description: "Brutal fighting game" }
];
