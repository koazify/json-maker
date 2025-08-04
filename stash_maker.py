import streamlit as st
import json
import colorsys

st.set_page_config(page_title="Stash Maker V0.1.2", page_icon="📦")

item_ids = [
    "item_anti_gravity_grenade", "item_apple", "item_arena_pistol", "item_arena_shotgun",
    "item_arrow", "item_arrow_bomb", "item_arrow_heart", "item_arrow_lightbulb",
    "item_arrow_teleport", "item_backpack", "item_backpack_black", "item_backpack_green",
    "item_backpack_large_base", "item_backpack_large_basketball", "item_backpack_large_clover",
    "item_backpack_pink", "item_backpack_small_base", "item_backpack_white",
    "item_backpack_with_flashlight", "item_balloon", "item_balloon_heart", "item_banana",
    "item_baseball_bat", "item_big_cup", "item_boombox", "item_boombox_neon", "item_box_fan",
    "item_brain_chunk", "item_broccoli_grenade", "item_broccoli_shrink_grenade", "item_calculator",
    "item_cardboard_box", "item_cash", "item_cash_mega_pile", "item_cash_pile", "item_ceo_plaque",
    "item_clapper", "item_cluster_grenade", "item_cola", "item_cola_large", "item_company_ration",
    "item_company_ration_heal", "item_cracker", "item_crate", "item_crossbow", "item_crossbow_heart",
    "item_crowbar", "item_d20", "item_disc", "item_disposable_camera", "item_drill", "item_dynamite",
    "item_dynamite_cube", "item_egg", "item_electrical_tape", "item_eraser", "item_finger_board",
    "item_flaregun", "item_flashbang", "item_flashlight", "item_flashlight_mega",
    "item_flashlight_red", "item_floppy3", "item_floppy5", "item_football", "item_friend_launcher",
    "item_frying_pan", "item_gameboy", "item_glowstick", "item_goldbar", "item_goldcoin",
    "item_grenade", "item_grenade_gold", "item_grenade_launcher", "item_harddrive",
    "item_hawaiian_drum", "item_heart_chunk", "item_heart_gun", "item_heartchocolatebox",
    "item_hh_key", "item_hookshot", "item_hookshot_sword", "item_hoverpad", "item_impulse_grenade",
    "item_jetpack", "item_keycard", "item_lance", "item_landmine", "item_large_banana",
    "item_mug", "item_nut", "item_nut_drop", "item_ogre_hands", "item_ore_copper_l",
    "item_ore_copper_m", "item_ore_copper_s", "item_ore_gold_l", "item_ore_gold_m",
    "item_ore_gold_s", "item_ore_hell", "item_ore_silver_l", "item_ore_silver_m",
    "item_ore_silver_s", "item_painting_canvas", "item_paperpack", "item_pelican_case",
    "item_pickaxe", "item_pickaxe_cny", "item_pickaxe_cube", "item_pinata_bat", "item_pipe",
    "item_plunger", "item_pogostick", "item_police_baton", "item_portable_teleporter",
    "item_pumpkin_pie", "item_pumpkinjack", "item_pumpkinjack_small", "item_quiver",
    "item_quiver_heart", "item_radioactive_broccoli", "item_randombox_mobloot_big",
    "item_randombox_mobloot_medium", "item_randombox_mobloot_small", "item_randombox_mobloot_weapons",
    "item_randombox_mobloot_zombie", "item_rare_card", "item_revolver", "item_revolver_ammo",
    "item_revolver_gold", "item_robo_monke", "item_rope", "item_rpg", "item_rpg_ammo",
    "item_rpg_ammo_egg", "item_rpg_ammo_spear", "item_rpg_cny", "item_rpg_easter", "item_rpg_spear",
    "item_rubberducky", "item_ruby", "item_saddle", "item_scanner", "item_scissors",
    "item_server_pad", "item_shield", "item_shield_bones", "item_shield_police",
    "item_shield_viking_1", "item_shield_viking_2", "item_shield_viking_3", "item_shield_viking_4",
    "item_shotgun", "item_shotgun_ammo", "item_shredder", "item_shrinking_broccoli",
    "item_snowball", "item_stapler", "item_stash_grenade", "item_stick_armbones",
    "item_stick_bone", "item_sticker_dispenser", "item_sticky_dynamite", "item_stinky_cheese",
    "item_tablet", "item_tapedispenser", "item_tele_grenade", "item_teleport_gun", "item_theremin",
    "item_timebomb", "item_toilet_paper", "item_toilet_paper_mega", "item_toilet_paper_roll_empty",
    "item_treestick", "item_tripwire_explosive", "item_trophy", "item_turkey_leg", "item_turkey_whole",
    "item_ukulele", "item_ukulele_gold", "item_umbrella", "item_umbrella_clover",
    "item_unidentified", "item_upsidedown_loot", "item_uranium_chunk_l", "item_uranium_chunk_m",
    "item_uranium_chunk_s", "item_viking_hammer", "item_viking_hammer_twilight", "item_whoopie",
    "item_zipline_gun", "item_zombie_meat",

    # NEW ITEMS for 1.33.4.1545
    "item_cutie_dead", "item_goopfish", "item_goop"
]

if "stash" not in st.session_state:
    st.session_state.stash = {
        "itemID": "",
        "colorHue": 0,
        "colorSaturation": 0,
        "scaleModifier": 0,
        "state": 0,
        "children": []
    }

if "selected_path" not in st.session_state:
    st.session_state.selected_path = []

if "selected_option_idx" not in st.session_state:
    st.session_state.selected_option_idx = 0

if "remove_idx" not in st.session_state:
    st.session_state.remove_idx = 0

def get_item_by_path(stash, path):
    item = stash
    for idx in path:
        if "children" in item and len(item["children"]) > idx:
            item = item["children"][idx]
        else:
            return None
    return item

def set_item_by_path(stash, path, new_item):
    if not path:
        st.session_state.stash = new_item
        return
    parent = get_item_by_path(stash, path[:-1])
    if parent and "children" in parent and len(parent["children"]) > path[-1]:
        parent["children"][path[-1]] = new_item

def display_path_names(stash, path):
    names = [stash["itemID"] or "(root)"]
    item = stash
    for idx in path:
        item = item["children"][idx]
        names.append(item["itemID"] or f"(child {idx})")
    return " > ".join(names)

def build_select_options(stash, path=[]):
    options = [(list(path), display_path_names(stash, path))]
    item = get_item_by_path(stash, path)
    if item and "children" in item:
        for i, _ in enumerate(item["children"]):
            options.extend(build_select_options(stash, path + [i]))
    return options

tab_main, tab_tutorial = st.tabs(["📦 Main", "❓ Tutorial"])

# ========== MAIN TAB ==========
with tab_main:
    st.title("📦 ACUT STASH MAKER")
    st.markdown("[Join Discord](https://discord.gg/RRSxhrG6Sk) | [Add ACUT Bot](https://discord.com/oauth2/authorize?client_id=1392914439266767009&permissions=68608&scope=bot+applications.commands)")

    st.sidebar.title("🎒 Insert Item")
    selected_item = st.sidebar.selectbox("Select item to insert", sorted(item_ids))
    insert_target = st.sidebar.radio("Insert into:", ["Main Item", "Child Item"], index=0)

    if st.sidebar.button("➕ Insert Item"):
        new_insert = {
            "itemID": selected_item,
            "colorHue": 0,
            "colorSaturation": 0,
            "scaleModifier": 0,
            "state": 0,
            "children": []
        }
        if insert_target == "Main Item":
            st.session_state.stash = new_insert
        else:
            current = get_item_by_path(st.session_state.stash, st.session_state.selected_path)
            if current:
                current.setdefault("children", []).append(new_insert)

    st.sidebar.markdown("### New Items in `1.33.4.1545`")
    for i in ["item_cutie_dead", "item_goopfish", "item_goop"]:
        st.sidebar.markdown(f"- `{i}`")

    options = build_select_options(st.session_state.stash)
    selected_idx = st.selectbox("Select item to edit/add child", range(len(options)),
                                format_func=lambda i: options[i][1],
                                index=st.session_state.selected_option_idx)
    st.session_state.selected_option_idx = selected_idx
    st.session_state.selected_path = options[selected_idx][0]

    item = get_item_by_path(st.session_state.stash, st.session_state.selected_path)

    st.markdown("---")
    st.subheader(f"🛠 Editing: {display_path_names(st.session_state.stash, st.session_state.selected_path)}")

    if item:
        changed = False
        itemID = st.text_input("itemID", item.get("itemID", ""))
        if itemID != item.get("itemID", ""):
            item["itemID"] = itemID
            changed = True

        colorHue = st.slider("colorHue", 0, 270, item.get("colorHue", 0))
        colorSaturation = st.slider("colorSaturation", 0, 124, item.get("colorSaturation", 0))

        h, s, l = colorHue / 270, colorSaturation / 124, 0.5
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        hex_color = '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
        st.markdown(f"<div style='width:100%;height:40px;background-color:{hex_color};border-radius:5px;border:1px solid #aaa;'></div>", unsafe_allow_html=True)
        st.caption(f"Color preview: `{hex_color}`")

        scaleModifier = st.number_input("scaleModifier", -128, 127, item.get("scaleModifier", 0))
        state = st.number_input("state", value=item.get("state", 0))

        item.update({
            "colorHue": colorHue,
            "colorSaturation": colorSaturation,
            "scaleModifier": scaleModifier,
            "state": state
        })

        if changed:
            set_item_by_path(st.session_state.stash, st.session_state.selected_path, item)

        st.subheader("➕ Add Child Item")
        new_child_id = st.text_input("Child itemID")
        if st.button("Add child"):
            if new_child_id.strip():
                item.setdefault("children", []).append({
                    "itemID": new_child_id.strip(),
                    "colorHue": 0,
                    "colorSaturation": 0,
                    "scaleModifier": 0,
                    "state": 0,
                    "children": []
                })
                st.success("Child added.")

        if item.get("children"):
            st.subheader("🗑️ Remove Child Item")
            idx = st.number_input("Child index to remove", 0, len(item["children"]) - 1, value=st.session_state.remove_idx)
            st.session_state.remove_idx = idx
            if st.button("Remove child"):
                removed = item["children"].pop(idx)
                st.success(f"Removed child: `{removed.get('itemID', 'unknown')}`")

    else:
        st.error("Couldn't find the selected item.")

    st.markdown("---")
    st.subheader("📤 Export Stash JSON")
    st.json(st.session_state.stash)
    json_str = json.dumps(st.session_state.stash, indent=2)
    st.download_button("💾 Download JSON", json_str, file_name="stash.json", mime="application/json")


# ========== TUTORIAL TAB ==========
with tab_tutorial:
    st.title("📘 How To Use - Quick Tutorial")
    st.markdown("""
Welcome to the **ACUT Stash Maker**! Here's a simple guide:

### 1. Insert an Item
- Use the **sidebar** to pick your item.
- Choose whether to insert it as the **main item** or add it under another item.

### 2. Edit Your Item
- Select an item from the dropdown.
- You can **change its color**, **scale**, and **state**.

### 3. Add or Remove Children
- You can attach other items to your selected item.
- Scroll down to "Add Child Item" to put a new item inside.

### 4. Export
- When you're done, scroll to the bottom.
- Hit "Download JSON" to get your finished stash.

That's it! No setup, no coding. Just click around and you're good.
""")
