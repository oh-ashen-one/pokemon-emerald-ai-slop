OldaleTown_Mart_MapScripts::
	.byte 0

OldaleTown_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	goto_if_set FLAG_ADVENTURE_STARTED, OldaleTown_Mart_ExpandedItems
	pokemart OldaleTown_Mart_Pokemart_Basic
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
OldaleTown_Mart_Pokemart_Basic:
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

OldaleTown_Mart_ExpandedItems::
	pokemart OldaleTown_Mart_Pokemart_Expanded
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
OldaleTown_Mart_Pokemart_Expanded:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

OldaleTown_Mart_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_ADVENTURE_STARTED, OldaleTown_Mart_EventScript_PokeBallsInStock
	msgbox OldaleTown_Mart_Text_PokeBallsAreSoldOut, MSGBOX_DEFAULT
	release
	end

OldaleTown_Mart_EventScript_PokeBallsInStock::
	msgbox OldaleTown_Mart_Text_ImGoingToBuyPokeBalls, MSGBOX_DEFAULT
	release
	end

OldaleTown_Mart_EventScript_Boy::
	lock
	faceplayer
	msgbox OldaleTown_Mart_Text_RareCandyHandout, MSGBOX_DEFAULT
	giveitem ITEM_RARE_CANDY, 99
	release
	end

OldaleTown_Mart_Text_RareCandyHandout:
	.string "Oh hey. My model hallucinated a whole\n"
	.string "pallet of RARE CANDY into the\l"
	.string "stockroom overnight.\p"
	.string "Inventory's a disaster, so just take\n"
	.string "them. Come back whenever you want to\l"
	.string "grind a little less.$"

OldaleTown_Mart_Text_PokeBallsAreSoldOut:
	.string "The clerk says POKé BALLS are sold\n"
	.string "out until the prototype gets approved.\p"
	.string "So, never. Probably never.$"

OldaleTown_Mart_Text_ImGoingToBuyPokeBalls:
	.string "I'm going to buy POKé BALLS and catch\n"
	.string "whatever survived the prompt queue.$"

OldaleTown_Mart_Text_RestoreHPWithPotion:
	.string "Oh, the glasses? I vibe-code the\n"
	.string "MART inventory system.\p"
	.string "It's 12,000 lines and none of us\n"
	.string "know which 40 actually run.\p"
	.string "A POTION still works though. Some\n"
	.string "things the AI couldn't break yet.$"
