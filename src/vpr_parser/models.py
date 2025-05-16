from pydantic import BaseModel, Field, Extra, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List, Optional, Dict


class AliasedBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda x: (
            to_camel(x).replace("Id", "ID")  # this shit is so ass i hate you yamaha 😭
            if x != "global_config"
            else "global"
        ),  # i love pyright randomly giving me 1mil errors ❤️
        populate_by_name=True,
        extra="forbid",
    )


class Version(AliasedBaseModel):
    major: int
    minor: int
    revision: int


class MasterTrackLoop(AliasedBaseModel):
    is_enabled: bool
    begin: int
    end: int


class MasterTrackTempoGlobal(AliasedBaseModel):
    is_enabled: bool
    value: int


class MasterTrackTempoEvent(AliasedBaseModel):
    pos: int
    value: int


class MasterTrackTempo(AliasedBaseModel):
    is_folded: bool
    height: float
    global_config: MasterTrackTempoGlobal
    events: List[MasterTrackTempoEvent]


class MasterTrackTimeSigEvent(AliasedBaseModel):
    bar: int
    numer: int
    denom: int


class MasterTrackTimeSig(AliasedBaseModel):
    is_folded: bool
    events: List[MasterTrackTimeSigEvent]


class MasterTrackVolumeEvent(AliasedBaseModel):
    pos: int
    value: int


class MasterTrackVolume(AliasedBaseModel):
    is_folded: bool
    height: float
    events: List[MasterTrackVolumeEvent]


class MasterTrackPanpotEvent(AliasedBaseModel):
    pos: int
    value: int


class MasterTrackPanpot(AliasedBaseModel):
    is_folded: bool
    height: float
    events: List[MasterTrackPanpotEvent]


class MasterTrack(AliasedBaseModel):
    sampling_rate: int
    loop: MasterTrackLoop
    tempo: MasterTrackTempo
    time_sig: MasterTrackTimeSig
    volume: MasterTrackVolume


class Voice(AliasedBaseModel):
    comp_id: str
    name: str


class Parameter(AliasedBaseModel):
    name: str
    value: str | int | float


class MidiEffect(AliasedBaseModel):
    id: str
    is_bypassed: bool
    is_folded: bool
    parameters: List[Parameter]


class Expression(AliasedBaseModel):
    opening: int


class SingingSkillWeight(AliasedBaseModel):
    pre: int
    post: int


class SingingSkill(AliasedBaseModel):
    duration: int
    weight: SingingSkillWeight


class Vibrato(AliasedBaseModel):
    type: int
    duration: int


class Note(AliasedBaseModel):
    lyric: str
    phoneme: str
    is_protected: bool
    pos: int
    duration: int
    number: int
    velocity: int
    exp: Expression
    singing_skill: SingingSkill
    vibrato: Vibrato


class ControllerEvent(AliasedBaseModel):
    pos: int
    value: int


class Controller(AliasedBaseModel):
    name: str
    events: List[ControllerEvent]


class VoiceInfo(AliasedBaseModel):
    comp_id: str
    lang_id: int


class Part(AliasedBaseModel):
    pos: int
    duration: int
    style_name: str
    voice: VoiceInfo
    midi_effects: List[MidiEffect]
    notes: Optional[List[Note]] = None
    controllers: Optional[List[Controller]] = None


class TrackVolume(AliasedBaseModel):
    is_folded: bool
    height: float
    events: List[MasterTrackVolumeEvent]


class TrackPanpot(AliasedBaseModel):
    is_folded: bool
    height: float
    events: List[MasterTrackPanpotEvent]


class Track(AliasedBaseModel):
    type: int
    name: str
    color: int
    bus_no: int
    is_folded: bool
    height: float
    volume: TrackVolume
    panpot: TrackPanpot
    is_muted: bool
    is_solo_mode: bool
    parts: List[Part]


class VPRFile(AliasedBaseModel):
    version: Version
    vender: str
    title: str
    master_track: MasterTrack
    voices: List[Voice]
    tracks: List[Track]
