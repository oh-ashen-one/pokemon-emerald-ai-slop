OldaleTown_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, OldaleTown_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

OldaleTown_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_OLDALE_TOWN
	call Common_EventScript_UpdateBrineyLocation
	end

OldaleTown_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_OLDALE_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

OldaleTown_PokemonCenter_1F_EventScript_Gentleman::
	msgbox OldaleTown_PokemonCenter_1F_Text_TrainersCanUsePC, MSGBOX_NPC
	end

OldaleTown_PokemonCenter_1F_EventScript_Boy::
	msgbox OldaleTown_PokemonCenter_1F_Text_PokemonCentersAreGreat, MSGBOX_NPC
	end

OldaleTown_PokemonCenter_1F_EventScript_Girl::
	lock
	faceplayer
	goto_if_set FLAG_SYS_POKEDEX_GET, OldaleTown_PokemonCenter_1F_EventScript_WirelessClubAvailable
	msgbox OldaleTown_PokemonCenter_1F_Text_WirelessClubNotAvailable, MSGBOX_DEFAULT
	release
	end

OldaleTown_PokemonCenter_1F_EventScript_WirelessClubAvailable::
	msgbox OldaleTown_PokemonCenter_1F_Text_TradedInWirelessClub, MSGBOX_DEFAULT
	release
	end

OldaleTown_PokemonCenter_1F_Text_TrainersCanUsePC:
	.string "I'm in management. I don't code.\p"
	.string "I align the team around a vision of\n"
	.string "synergistic POKéMON outcomes.\p"
	.string "Mostly I move the deadline and let\n"
	.string "the kid in the beanie panic.$"

OldaleTown_PokemonCenter_1F_Text_PokemonCentersAreGreat:
	.string "I have not slept since the starter\n"
	.string "demo shipped. Love the beanie though?\p"
	.string "I'm the only engineer left. The suit\n"
	.string "promised this would be “a quick MVP.”\p"
	.string "POKéMON CENTERS heal for free, which\n"
	.string "is the only sustainable thing here.$"

OldaleTown_PokemonCenter_1F_Text_WirelessClubNotAvailable:
	.string "The WIRELESS CLUB upstairs is still\n"
	.string "making adjustments.\p"
	.string "That is corporate speak for “do not\n"
	.string "press that button on camera.”$"

OldaleTown_PokemonCenter_1F_Text_TradedInWirelessClub:
	.string "I traded POKéMON upstairs once.\p"
	.string "The other trainer received a mascot\n"
	.string "with my browser history in its eyes.$"
