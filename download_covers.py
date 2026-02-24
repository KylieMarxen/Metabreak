import requests
import os
from time import sleep

# Create covers directory
os.makedirs('uploads/covers', exist_ok=True)

# Direct URLs to game covers (from public CDNs)
COVER_URLS = {
    "g_elden_ring.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co4jni.jpg",
    "g_witcher3.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1wyy.jpg",
    "g_skyrim.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1roa.jpg",
    "g_baldurs_gate3.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co5w2l.jpg",
    "g_cyberpunk2077.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co2lbd.jpg",
    "g_ff7_remake.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co20q5.jpg",
    "g_persona5.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1r5v.jpg",
    "g_dark_souls3.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1x7u.jpg",
    "g_bloodborne.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1vcf.jpg",
    "g_sekiro.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1mqh.jpg",
    "g_zelda_botw.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1tqv.jpg",
    "g_zelda_totk.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co5vmg.jpg",
    "g_god_of_war.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1tmu.jpg",
    "g_god_of_war_ragnarok.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co4cn0.jpg",
    "g_last_of_us.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1r7h.jpg",
    "g_last_of_us2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1xbg.jpg",
    "g_rdr2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1q1f.jpg",
    "g_gta5.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1r7k.jpg",
    "g_uncharted4.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1tdn.jpg",
    "g_horizon_zd.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1tff.jpg",
    "g_horizon_fw.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co3pxg.jpg",
    "g_ghost_tsushima.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co23py.jpg",
    "g_spiderman.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1r77.jpg",
    "g_spiderman2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co6qmr.jpg",
    "g_halo_infinite.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co4p64.jpg",
    "g_cod_mw2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co5s4g.jpg",
    "g_apex.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1z0r.jpg",
    "g_valorant.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co2mvt.jpg",
    "g_overwatch2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co5vk0.jpg",
    "g_doom_eternal.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1sd7.jpg",
    "g_csgo.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1wzf.jpg",
    "g_titanfall2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1x7z.jpg",
    "g_fortnite.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co6r3z.jpg",
    "g_pubg.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co20qd.jpg",
    "g_warzone.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co200i.jpg",
    "g_hollow_knight.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1rgi.jpg",
    "g_celeste.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1tdo.jpg",
    "g_hades.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co2l7k.jpg",
    "g_stardew.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co5gij.jpg",
    "g_terraria.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co3n8m.jpg",
    "g_undertale.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1tph.jpg",
    "g_cuphead.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1irg.jpg",
    "g_civ6.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1w6a.jpg",
    "g_starcraft2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co49y5.jpg",
    "g_xcom2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1x7v.jpg",
    "g_total_war_wh3.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co4jnh.jpg",
    "g_minecraft.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co49wj.jpg",
    "g_cities_skylines.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co20qb.jpg",
    "g_sims4.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1rs6.jpg",
    "g_kerbal.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co23t9.jpg",
    "g_re_village.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co2lcw.jpg",
    "g_re2_remake.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1irg.jpg",
    "g_silent_hill2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co87wf.jpg",
    "g_alan_wake2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co6rkz.jpg",
    "g_fifa23.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co5nxd.jpg",
    "g_nba2k23.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co5odf.jpg",
    "g_forza_horizon5.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co2xr6.jpg",
    "g_gran_turismo7.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co3p5w.jpg",
    "g_mario_odyssey.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1w54.jpg",
    "g_mario_kart8.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co3p2d.jpg",
    "g_smash_ultimate.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1rme.jpg",
    "g_animal_crossing.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1yai.jpg",
    "g_metroid_dread.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co3mg8.jpg",
    "g_pokemon_sv.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co5fzi.jpg",
    "g_ff14.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co3p12.jpg",
    "g_wow.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co6mzu.jpg",
    "g_destiny2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1rdt.jpg",
    "g_lol.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co49yi.jpg",
    "g_dota2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co20md.jpg",
    "g_it_takes_two.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co2r2k.jpg",
    "g_psychonauts2.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co2ldb.jpg",
    "g_ratchet_clank.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co2lcz.jpg",
    "g_street_fighter6.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co5q5l.jpg",
    "g_tekken8.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co7u4i.jpg",
    "g_mk11.jpg": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1rfu.jpg",
}

def download_cover(filename, url):
    """Download a single cover image"""
    filepath = os.path.join('uploads/covers', filename)
    
    # Skip if already exists
    if os.path.exists(filepath):
        return 'skipped'
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return 'success'
        else:
            return 'failed'
    except Exception as e:
        print(f"      Error: {e}")
        return 'failed'

def download_all():
    """Download all covers"""
    print("\n🎮 Game Cover Downloader")
    print("=" * 60)
    print(f"📦 Total covers to download: {len(COVER_URLS)}")
    print("=" * 60 + "\n")
    
    success = 0
    failed = 0
    skipped = 0
    
    for i, (filename, url) in enumerate(COVER_URLS.items(), 1):
        game_name = filename.replace('g_', '').replace('.jpg', '').replace('_', ' ').title()
        print(f"[{i}/{len(COVER_URLS)}] {game_name}")
        
        result = download_cover(filename, url)
        
        if result == 'success':
            print(f"      ✅ Downloaded: {filename}")
            success += 1
        elif result == 'skipped':
            print(f"      ⏭️  Already exists: {filename}")
            skipped += 1
        else:
            print(f"      ❌ Failed: {filename}")
            failed += 1
        
        # Be nice to the server
        if result == 'success':
            sleep(0.2)
    
    print("\n" + "=" * 60)
    print("📊 Download Summary:")
    print(f"   ✅ Successfully downloaded: {success}")
    print(f"   ⏭️  Skipped (already exist): {skipped}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📁 Total covers in folder: {len([f for f in os.listdir('uploads/covers') if f.endswith('.jpg')])}")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    download_all()