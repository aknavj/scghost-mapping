"""Compile named Test Room MAPs into nod\\game\\Maps; prepare sibling game resources."""

import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT / "nod"
MAPS = WORKSPACE / "maps"
GAME = WORKSPACE / "game"
OUTPUT = GAME / "Maps"
MAX_LEVEL_STEM = 25

COMMON_LIGHTING = [
    "--world-only", "--lighting", "on", "--light-shadows", "on",
    "--light-phong", "60", "--sun-light", ".85", ".92", "1", ".9", "-.3", ".4", "-1",
    "--ambient-light", ".75", ".85", "1", ".7",
]

COURTYARD_LIGHTING = [
    "--world-only", "--lighting", "on", "--light-shadows", "on",
    "--light-phong", "40", "--sun-light", "1", ".92", ".78", "1.1", "-.2", ".35", "-1",
    "--ambient-light", ".8", ".88", "1", ".7",
]

ARENA_LIGHTING = [
    "--world-only", "--lighting", "on", "--light-samples", "4",
    "--light-shadows", "on", "--light-phong", "89",
    "--ambient-light", ".75", ".85", "1", ".65",
]


def run_tool(command):
    command = [str(argument) for argument in command]
    print(subprocess.list2cmdline(command), flush=True)
    subprocess.run(command, check=True)


def lighting(source):
    purpose = source.stem.split("_TR_", 1)[1]
    if purpose in ("Defaults", "Linear_Fog", "Short_Far_Clip", "Sky_Audio_Reverb",
                   "Explicit_Default", "Completed_Fog", "Reverb_Max", "Protoss_Court"):
        return COURTYARD_LIGHTING
    return ARENA_LIGHTING if purpose == "Trigger_Arena" else COMMON_LIGHTING


def build_case(source, sidecar, sdk, assets):
    with tempfile.TemporaryDirectory(prefix=".build-", dir=WORKSPACE) as directory:
        outputs = [Path(directory) / (source.stem + suffix) for suffix in (".nil", ".nsd", ".npd")]
        if sidecar:
            run_tool([sdk / "NODscene.exe", "compile", source, sidecar, *outputs, WORKSPACE, assets])
        else:
            for tool, target in zip(("MAPtoNIL", "MAPtoNSD", "MAPtoNPD"), outputs):
                options = lighting(source) if tool == "MAPtoNIL" else []
                run_tool([sdk / (tool + ".exe"), *options, "--workspace", WORKSPACE,
                          "--asset-root", assets, source, target])
        for path in outputs:
            if not path.is_file() or path.stat().st_size < 8:
                raise RuntimeError(f"Missing or truncated compiler output: {path}")
        for path in outputs:
            path.replace(OUTPUT / path.name)


def merge_localization(original, tables, missions):
    rows, keys, level_keys = [], set(), {}
    for path in tables:
        local_keys = set()
        for number, line in enumerate(path.read_bytes().splitlines(), 1):
            line = line.strip()
            if not line or line.startswith((b"#", b"//")):
                continue
            entry = line.split(None, 1)
            if len(entry) != 2:
                raise RuntimeError(f"Missing localization text in {path}:{number}")
            key, text = entry
            if not key.isascii():
                raise RuntimeError(f"Localization keys must be ASCII in {path}:{number}")
            if key.lower() in keys:
                raise RuntimeError(f"Duplicate localization key {key!r} in {path}:{number}")
            keys.add(key.lower())
            local_keys.add(key.lower())
            rows.append(key.ljust(32) + b" " + text)
        level_keys[path.stem.lower()] = local_keys
    for label, level in missions:
        if not label.isascii() or label.encode("ascii").lower() not in level_keys.get(level.lower(), set()):
            raise RuntimeError(f"Mission {label!r} for {level!r} requires a matching key in {level}.nls")

    header = re.search(rb"(?m)^//[ \t]*MISSIONS[ \t]*//[ \t]*\r?\n//\*+//[ \t]*\r?\n", original)
    if header is None:
        raise RuntimeError("Original game.nls is missing its native MISSIONS section header.")
    following = re.search(rb"(?m)^//\*+//[ \t]*\r?\n//[ \t]*[A-Z]", original[header.end():])
    if following is None:
        raise RuntimeError("Original game.nls is missing the section following MISSIONS.")
    end = header.end() + following.start()
    return original[:header.end()] + b"\r\n" + b"\r\n".join(rows) + b"\r\n\r\n" + original[end:]


def main(argv=None):
    sources = sorted(MAPS.rglob("1_*.map"), key=lambda path: path.stem)
    maps = {path.stem: path for path in sources}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List available MAPs without building.")
    parser.add_argument("--case", action="append", choices=maps, metavar="ID",
                        help="Build only this MAP; repeat to select several. Default: all MAPs.")
    parser.add_argument("--asset-root", type=Path, help="Original game_files asset root (read-only).")
    parser.add_argument("--sdk-dir", type=Path,
                        default=ROOT.parent / "nodsdk-scghost" / ".build" / "cmake" / "Release")
    options = parser.parse_args(argv)
    if not maps:
        parser.error(f"No named Test Room MAPs found in {MAPS}")
    if len(maps) != len(sources) or len({name[:5] for name in maps}) != len(maps):
        parser.error("MAP names and their numeric prefixes must be unique.")
    if any(not re.fullmatch(r"1_[0-9]_[0-9]_TR_[A-Za-z0-9_]+", name) for name in maps):
        parser.error("Expected MAP filenames: 1_X_X_TR_Purpose.map (single-digit numeric slots).")
    oversized = [name for name in maps if len(name) > MAX_LEVEL_STEM]
    if oversized:
        parser.error(f"Runtime-safe MAP stems must be at most {MAX_LEVEL_STEM} ASCII characters: "
                     + ", ".join(oversized))
    if options.list:
        print("\n".join(maps))
        return

    if options.asset_root is None:
        parser.error("Provide --asset-root (or use --list).")
    selected = options.case or list(maps)
    assets, sdk = options.asset_root.resolve(), options.sdk_dir.resolve()
    if GAME.resolve().is_relative_to(assets) or assets.is_relative_to(GAME.resolve()):
        parser.error("The original asset root must not overlap the generated game resources.")
    if OUTPUT.exists() and any(not path.is_file() or path.suffix.lower() not in (".nil", ".nsd", ".npd")
                               for path in OUTPUT.iterdir()):
        parser.error(f"{OUTPUT} may contain only NIL, NSD and NPD files; move other contents out first.")
    cases, tools, resources = [], set(), set()
    objective_references = {}
    level_references = set()
    for name in selected:
        source = maps[name]
        text = source.read_text(encoding="utf-8")
        sidecar = source.with_suffix(".nodsrc") if '"nod_sources"' in text else None
        if sidecar and not sidecar.is_file():
            raise FileNotFoundError(f"Source-backed MAP requires its matching sidecar: {sidecar}")
        cases.append((source, sidecar))
        tools.update(("NODscene",) if sidecar else ("MAPtoNIL", "MAPtoNSD", "MAPtoNPD"))
        for entity in re.findall(r"\{([^{}]*)\}", text, flags=re.S):
            handler = re.search(r'"nod_prop_15"\s+"(c(?:RegionCutScene|CutscenePlay|LevelChange|ObjectiveUpdate))"', entity)
            if handler is None:
                continue
            if handler.group(1) == "cObjectiveUpdate":
                keys = re.findall(r'"nod_script_param_[12]"\s+"([^"]+)"', entity)
                objective_references.setdefault(name, set()).update(key.lower() for key in keys)
                continue
            reference = re.search(r'"nod_script_param_0"\s+"([^"]+)"', entity)
            if reference is None:
                parser.error(f"{handler.group(1)} resource name is missing in {source.name}")
            resource = reference.group(1)
            if handler.group(1) == "cLevelChange":
                level_references.add(resource)
                continue
            if not resource.lower().endswith(".ncs"):
                resource += ".ncs"
            if Path(resource).name != resource:
                parser.error(f"Cutscene references must be basenames: {resource}")
            resources.add(GAME / "Cutscenes" / resource)
    misc = GAME / "Misc"
    tables = sorted(misc.glob("1_*_TR_*.nls"))
    dependencies = [(assets / "Sounds" / ("2_2_2" + suffix),
                     GAME / "Sounds" / (name[:5] + suffix))
                    for name in selected for suffix in (".xsb", ".xwb")]
    required = ([sdk / (tool + ".exe") for tool in sorted(tools)]
                + [src for src, dst in dependencies] + sorted(resources)
                + [assets / "Misc" / "game.nls", misc / "ghostsp.nsc"]
                + [misc / (name + suffix) for name in selected for suffix in (".nls", ".nlt")])
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            raise FileNotFoundError(f"Required file is missing or empty: {path}")
    chronicle = (misc / "ghostsp.nsc").read_text(encoding="utf-8")
    missions = re.findall(r"^MISSION[ \t]+(\S+)[ \t]+(\S+)", chronicle, flags=re.M)
    if not missions:
        raise RuntimeError(f"No MISSION entries found in {misc / 'ghostsp.nsc'}")
    mission_objectives = {}
    for level, body in re.findall(r"^MISSION[ \t]+\S+[ \t]+(\S+)[^\r\n]*\r?\n(.*?)^ENDMISSION",
                                  chronicle, flags=re.M | re.S):
        keys = re.findall(r"^OBJECTIVE[ \t]+(\S+)", body, flags=re.M)
        if len(keys) > 32:
            raise RuntimeError(f"{level} exceeds the native 32-objective completion bitmask.")
        lowered = {key.lower() for key in keys}
        if len(lowered) != len(keys):
            raise RuntimeError(f"Duplicate OBJECTIVE keys in mission {level}")
        mission_objectives[level] = lowered
    for name, keys in objective_references.items():
        missing = keys - mission_objectives.get(name, set())
        if missing:
            raise RuntimeError(f"{name} updates objectives not declared in its mission: {', '.join(sorted(missing))}")
    level_references.update(level for label, level in missions)
    for level in sorted(level_references):
        if not level.isascii() or len(level) > MAX_LEVEL_STEM:
            parser.error(f"Runtime level references must be at most {MAX_LEVEL_STEM} ASCII characters: {level}")
    localization = merge_localization((assets / "Misc" / "game.nls").read_bytes(), tables, missions)
    localization_keys = {line.split(None, 1)[0].lower()
                         for line in localization.splitlines() if line.strip()}
    for key in re.findall(r"^OBJECTIVE[ \t]+(\S+)", chronicle, flags=re.M):
        if not key.isascii() or key.encode("ascii").lower() not in localization_keys:
            raise RuntimeError(f"Objective key {key!r} is missing from the generated Strings/game.nls")
    localization_path = GAME / "Strings" / "game.nls"

    OUTPUT.mkdir(parents=True, exist_ok=True)
    for index, (source, sidecar) in enumerate(cases, 1):
        print(f"[{index}/{len(cases)}] Building {source.stem}", flush=True)
        build_case(source, sidecar, sdk, assets)
    for original, target in dependencies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original, target)
    localization_path.parent.mkdir(parents=True, exist_ok=True)
    localization_path.write_bytes(localization)
    for folder in ("Models", "Anims", "Motions", "Terrains"):
        (GAME / "3D" / folder).mkdir(parents=True, exist_ok=True)
    (GAME / "Materials").mkdir(exist_ok=True)
    print(f"Built {len(cases)} maps: {OUTPUT}", flush=True)
    print(f"Runtime localization: {localization_path}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
