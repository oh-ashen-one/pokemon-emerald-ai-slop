OldaleTown_House2_MapScripts::
	.byte 0

OldaleTown_House2_EventScript_Woman::
	msgbox OldaleTown_House2_Text_PokemonLevelUp, MSGBOX_NPC
	end

OldaleTown_House2_EventScript_Man::
	msgbox OldaleTown_House2_Text_YoullGoFurtherWithStrongPokemon, MSGBOX_NPC
	end

OldaleTown_House2_Text_PokemonLevelUp:
	.string "When POKéMON battle, they level up.\p"
	.string "When vibe coders battle, they invent\n"
	.string "three new bugs and call it velocity.$"

OldaleTown_House2_Text_YoullGoFurtherWithStrongPokemon:
	.string "If your POKéMON get stronger, you can\n"
	.string "go farther from here.\p"
	.string "If your build gets stronger, you can\n"
	.string "maybe leave the README untouched.$"
