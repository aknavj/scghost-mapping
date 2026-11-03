# SC Ghost mapping workspace

StarCraft: Ghost test maps for GtkRadiant and the OpenNOD SDK.

## Installation

The game folder is currently [nod/game](nod/game) in this repository.
Copy its **contents**, not the folder itself, into the Xbox build's game directory.

### Option 1: Use an existing installation

1. Close the game and back up:
   - `Misc\ghostsp.nsc`
   - `Strings\game.nls`
2. Copy the contents of `nod\game` into your local StarCraft: Ghost Xbox build,
   merging folders and replacing files.
3. Restart the game.

### Option 2: Keep a dedicated test installation

1. Make a separate copy of the StarCraft: Ghost Xbox build.
2. Remove unused campaign data to keep it tidy. Retain the executable and shared
   assets needed by the test maps.
3. Copy the contents of `nod\game` into that copy, merging folders and replacing files.
4. Use this installation and a separate profile for SDK maps and experiments.

## Maps

| Map | Purpose / goal |
|---|---|
| [1_0_0_TR_Defaults](nod/maps/sdk_068/1_0_0_TR_Defaults.map) | Baseline courtyard: depth, materials, lighting, movement, and audio. |
| [1_0_1_TR_Linear_Fog](nod/maps/sdk_068/1_0_1_TR_Linear_Fog.map) | Fog fading over distance. |
| [1_0_2_TR_Short_Far_Clip](nod/maps/sdk_068/1_0_2_TR_Short_Far_Clip.map) | Clipping of distant targets. |
| [1_0_3_TR_Sky_Audio_Reverb](nod/maps/sdk_068/1_0_3_TR_Sky_Audio_Reverb.map) | Sky, ambience, and reverb. |
| [1_0_4_TR_Explicit_Default](nod/maps/sdk_068/1_0_4_TR_Explicit_Default.map) | Explicit settings compared with native defaults. |
| [1_0_5_TR_Completed_Fog](nod/maps/sdk_068/1_0_5_TR_Completed_Fog.map) | Full linear-fog configuration. |
| [1_0_6_TR_Reverb_Max](nod/maps/sdk_068/1_0_6_TR_Reverb_Max.map) | Maximum native reverb. |
| [1_0_7_TR_Trigger_Arena](nod/maps/sdk_068/1_0_7_TR_Trigger_Arena.map) | Sound/spawn consoles and actor paths. |
| [1_0_8_TR_Sky_Audio_Music](nod/maps/sdk_068/1_0_8_TR_Sky_Audio_Music.map) | Imported scene with unmasked sky and stealth music. |
| [1_0_9_TR_Sky_Ambient](nod/maps/sdk_068/1_0_9_TR_Sky_Ambient.map) | Imported scene with sky and hall ambience. |
| [1_1_0_TR_Trigger_Stress](nod/maps/sdk_068/1_1_0_TR_Trigger_Stress.map) | Doors, spawn waves, lift, and ordered checkpoints. |
| [1_1_1_TR_Objective_Region](nod/maps/sdk_068/1_1_1_TR_Objective_Region.map) | Objective completion opening a gate. |
| [1_1_2_TR_Cutscene_Region](nod/maps/sdk_068/1_1_2_TR_Cutscene_Region.map) | Cutscene play/stop controls and linked gates. |
| [1_1_3_TR_Timer_Trigger](nod/maps/sdk_068/1_1_3_TR_Timer_Trigger.map) | Timed and alternating gates. |
| [1_1_4_TR_Sound_Regions](nod/maps/sdk_068/1_1_4_TR_Sound_Regions.map) | Room/hangar reverb and audio reset. |
| [1_1_5_TR_Save_Regions](nod/maps/sdk_068/1_1_5_TR_Save_Regions.map) | Enabled and toggleable save checkpoints. |
| [1_1_6_TR_Stealth_Regions](nod/maps/sdk_068/1_1_6_TR_Stealth_Regions.map) | Stealth-state entry, toggling, and reset. |
| [1_1_7_TR_Kill_Zerg](nod/maps/sdk_068/1_1_7_TR_Kill_Zerg.map) | Zerg-kill filtering and exempt actors. |
| [1_1_8_TR_Damage_Regions](nod/maps/sdk_068/1_1_8_TR_Damage_Regions.map) | Enabled, toggleable, and cyclic damage hazards. |
| [1_1_9_TR_Fog_Control](nod/maps/sdk_068/1_1_9_TR_Fog_Control.map) | Temporary, toggled, and persistent fog. |
| [1_2_0_TR_Sound_Loops](nod/maps/sdk_068/1_2_0_TR_Sound_Loops.map) | Independent sound loops and stop controls. |
| [1_2_1_TR_FX_Particles](nod/maps/sdk_068/1_2_1_TR_FX_Particles.map) | Emitters, steam, explosions, and rain. |
| [1_2_2_TR_Advanced_Movers](nod/maps/sdk_068/1_2_2_TR_Advanced_Movers.map) | Translation, rotation, and clearance. |
| [1_2_3_TR_Object_Control](nod/maps/sdk_068/1_2_3_TR_Object_Control.map) | Collision, visibility, shader frames, removal, and physics. |
| [1_2_4_TR_Player_Messaging](nod/maps/sdk_068/1_2_4_TR_Player_Messaging.map) | Localized help and briefing requests. |
| [1_2_5_TR_Mission_Change](nod/maps/sdk_068/1_2_5_TR_Mission_Change.map) | Next-mission and level-reload controls. |
| `1_2_6_TR_Material_Preview` | Debug grid, texture scale, UVs, and lighting. Runtime only. |
| `1_2_7_TR_Props_Preview` | Model overrides, scale, frames, and rotation. Runtime only. |
| [1_2_8_TR_Basic_Map](nod/maps/sdk_067/1_2_8_TR_Basic_Map.map) | Legacy room with actors, props, and pickups. |
| [1_2_9_TR_Large_Map](nod/maps/sdk_067/1_2_9_TR_Large_Map.map) | Vehicles, structures, scale, lighting, and long views. |
| [1_3_0_TR_Basic_Room](nod/maps/sdk_067/1_3_0_TR_Basic_Room.map) | Floor scale, wall/ceiling materials, and lighting. |
| `1_3_1_TR_Scaling` | Model scale and orientation. Source and runtime files currently missing. |
| [1_3_2_TR_Protoss_Court](nod/maps/prototypes/1_3_2_TR_Protoss_Court.map) | Protoss courtyard design, Pylon, and inspection bays. |

Scaling remains in the chronicle; supply its runtime files before progressing
from Basic Room to Protoss Court.

## Game data layout

```text
game\
  Levels\                  <map>.nil, .nsd, .npd
  Misc\
    ghostsp.nsc            Mission order and setup
    <map>.nlt              Loading-screen text
    <map>.nls              Authored mission/objective strings
    <map>.nco              Conversation resources
    Templates\*.not        Native object templates
  Strings\game.nls         Merged runtime strings
  Sounds\1_X_X.xsb, .xwb    Sound-bank pairs
  Cutscenes\*.ncs, .nce    Cutscene scripts and events
  3D\
    Models\*.nod, *.nmb    Models and bundles
    Anims\*.nnb            Animation bundles
    Motions\*.nms          Motion mappings
    Terrains\              Terrain resources
  Materials\*.nsa, *.xpr   Materials and textures
```

NIL contains level geometry and lighting, NSD contains placements and scripts,
and NPD contains navigation. Original shared game assets are still required.

## Text and mission setup

[Misc/ghostsp.nsc](nod/game/Misc/ghostsp.nsc) connects each mission to its map,
strings, and loading screen. Example fields:

```text
MISSION        1_0_0_TR_DEF  1_0_0_TR_Defaults
OBJECTIVE      1_0_0_O00 1
LOADTEXT       1_0_0_TR_Defaults.nlt
LOADSCREEN     111a_MenuImage
```

- `MISSION`: first value is the menu-label key; second is the map stem in `Levels`.
- `OBJECTIVE`: key used by both the map's objective trigger and its displayed text.
- `LOADTEXT`: loading text file under `Misc`.
- `LOADSCREEN`: loading-image resource.

Edit the per-map `Misc\<map>.nls` fragments:

```text
1_0_0_TR_DEF                      Default
1_0_0_O00                        1. Check courtyard depth.
```

The builder merges them into **`Strings\game.nls`**, which the game reads for
menu labels and objectives. It does not read the individual fragments or
`Misc\game.nls`. The extension is `.nls`, not `.nsl`.

Edit `.nlt` loading text and `ghostsp.nsc` directly; builds leave them unchanged.
After text changes, copy the updated files into the game and restart it.

### Inspection objectives and progression

Follow the markers in order and try the controls at each stop. Objectives track
visits, not test results. Return to the start to request the next chronicle
mission after three seconds. Transition-test controls can leave the map early.

## Build and deploy

From the repository root, using Python 3.10 or newer:

```powershell
python .\build.py --list
python .\build.py --asset-root "C:\path\to\game_files"
python .\build.py --asset-root "C:\path\to\game_files" --case 1_1_0_TR_Trigger_Stress
```

Repeat `--case` to select several maps; omit it to build all available sources.
SDK tools default to `..\nodsdk-scghost\.build\cmake\Release`; use `--sdk-dir`
to select another build.

**Build output goes to `nod\game\Maps`. Copy the updated NIL/NSD/NPD files into
`nod\game\Levels` before installing the game folder.** The game reads `Levels`,
not `Maps`. Install only after a successful build.

Source maps live under `nod\maps`. Use `1_X_X_TR_Purpose`, keep the full stem
within **25 ASCII characters**, and use the same stem for all three exports.
Keep the matching `.nodsrc` sidecars beside the two imported sky maps.

## Project scope and license

This is not a game remake or a distribution of proprietary game assets.
It is intended for educational and preservation work, not commercial use.
Respect the rights of the original authors.

StarCraft: Ghost is a trademark of Blizzard Entertainment. This is an unofficial fan project, not affiliated with or endorsed by Blizzard.

Licensed under GNU GPL v3. See individual source files for copyright notices.

This project uses AI-assisted development with collaborative human/AI oversight
and human review of output.
